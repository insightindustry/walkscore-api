# -*- coding: utf-8 -*-

"""
#########################################
walkscore.http_client
#########################################

Implements a standardized interface for requesting URLs from the internet and
returning the response.

"""
import sys
import warnings
import email
import time
import threading
import json
import io

# - Requests is the preferred HTTP library
# - Google App Engine has urlfetch
# - Use Pycurl if it's there (at least it verifies SSL certs)
# - Fall back to urllib2 with a warning if needed
try:
    import urllib2 as urllib
except ImportError:
    # Try to load in urllib2, but don't sweat it if it's not available.
    pass

try:
    import pycurl
except ImportError:
    pycurl = None

try:
    import requests
except ImportError:
    requests = None
else:
    try:
        # Require version 0.8.8, but don't want to depend on distutils
        version = requests.__version__
        major, minor, patch = [int(i) for i in version.split(".")]
    except Exception:                                                                     # pylint: disable=W0703
        # Probably some new-fangled version, so it should support verify
        pass
    else:
        if (major, minor, patch) < (0, 8, 8):
            sys.stderr.write(
                "Warning: the WalkScore library requires that your Python "
                '"requests" library be newer than version 0.8.8, but your '
                '"requests" library is version %s. WalkScore will fall back to '
                "an alternate HTTP library so everything should work. We "
                'recommend upgrading your "requests" library. If you have any '
                "questions, please contact software@insightindustry.com. (HINT: running "
                '"pip install -U requests" should upgrade your requests '
                "library to the latest version.)" % (version,)
            )
            requests = None

try:
    from google.appengine.api import urlfetch
except ImportError:
    urlfetch = None

# proxy support for the pycurl client
import six
from six.moves.urllib.parse import urlparse

from backoff_utils import backoff
from backoff_utils import strategies as backoff_strategies
from validator_collection import validators

from walkscore.utilities import CA_BUNDLE_PATH, to_utf8
from walkscore.errors import check_for_errors, HTTPTimeoutError, SSLError, \
    WalkScoreError, BindingError, HTTPConnectionError


HTTP_METHODS = ['GET',
                'HEAD',
                'OPTIONS',
                'POST',
                'PUT',
                'PATCH',
                'DELETE']


def _now_ms():
    """Returns the current time expressed in milliseconds.

    :rtype: :class:`int <python:int>`
    """
    return int(round(time.time() * 1000))


def default_http_client(*args, **kwargs):
    """Return a default HTTP Client.

    :rtype: :class:`HTTPClient`
    """
    if urlfetch:
        impl = UrlFetchClient
    elif requests:
        impl = RequestsClient
    elif pycurl:
        impl = PycurlClient
    else:
        impl = Urllib2Client
        warnings.warn(
            "Warning: the WalkScore library is falling back to urllib2/urllib "
            "because neither requests nor pycurl are installed. "
            "urllib2's SSL implementation doesn't verify server "
            "certificates. For improved security, we suggest installing "
            "requests."
        )

    return impl(*args, **kwargs)


class HTTPClient(object):                                                                 # pylint: disable=R0205
    """Base class that provides HTTP connectivity."""

    MAX_DELAY = 2
    INITIAL_DELAY = 0.5

    def __init__(self,
                 verify_ssl_certs = True,
                 proxy = None):
        self._verify_ssl_certs = verify_ssl_certs

        if proxy:
            if isinstance(proxy, str):
                proxy = {
                    "http": proxy,
                    "https": proxy
                }

            if not isinstance(proxy, dict):
                raise ValueError(
                    "Proxy(ies) must be specified as either a string "
                    "URL or a dict() with string URL under the"
                    " "
                    "https"
                    " and/or "
                    "http"
                    " keys."
                )

        if proxy:
            self._proxy = proxy.copy()
        else:
            self._proxy = None

        self._thread_local = threading.local()

    def request_with_retries(self,
                             method,
                             url,
                             parameters = None,
                             headers = None,
                             request_body = None):
        """Execute a standard HTTP request with automatic retries on failure.

        :param method: The HTTP method to use for the request. Accepts `GET`, `HEAD`,
          `POST`, `PATCH`, `PUT`, or `DELETE`.
        :type method: :class:`str <python:str>`

        :param url: The URL to execute the request against.
        :type url: :class:`str <python:str>`

        :param parameters: URL parameters to submit with the request. Defaults to
          :obj:`None <python:None>`.
        :type parameters: :class:`dict <python:dict>` / :obj:`None <python:None>`

        :param headers: HTTP headers to submit with the request. Defaults to
          :obj:`None <python:None>`.
        :type headers: :class:`dict <python:dict>` / :obj:`None <python:None>`

        :param request_body: The data to supply in the body of the request. Defaults to
          :obj:`None <python:None>`.
        :type request_body: :obj:`None <python:None>` / :class:`dict <python:dict>` /
          :class:`str <python:str>` / :class:`bytes <python:bytes>`

        .. note::

          This method will apply an
          `exponential backoff strategy <https://en.wikipedia.org/wiki/Exponential_backoff>`_
          to retry the API request if it times out. By default:

          * requests that can be retried will be retried up to ``3`` times, but this can
            be overridden by setting a ``BACKOFF_DEFAULT_TRIES`` environment variable with
            the maximum number of attempts to make
          * there is no maximum delay to wait before final failure, but this can be
            overridden by setting a ``BACKOFF_DEFAULT_DELAY`` environment variable with
            the maximum number of seconds to wait (across all attempts) before failing.

        :raises ValueError: if ``method`` is not either ``GET``, ``HEAD``, ``POST``,
          ``PATCH``, ``PUT`` or ``DELETE``
        :raises ValueError: if ``url`` is not a valid URL
        :raises HTTPTimeoutError: if the request times out after repeated attempts
        :raises SSLError: if the request fails SSL certificate verification
        :raises WalkScoreError: *or sub-classes* for other errors returned by the API

        """
        response = backoff(self.request,
                           args = [method, url, parameters, headers, request_body],
                           catch_exceptions = [type(HTTPTimeoutError)],
                           strategy = backoff_strategies.Exponential)

        return response

    def _request(self,
                 method,
                 url,
                 parameters = None,
                 headers = None,
                 request_body = None):
        """Execute a standard HTTP request.

        :param method: The HTTP method to use for the request. Accepts `GET`, `HEAD`,
          `POST`, `PATCH`, `PUT`, or `DELETE`.
        :type method: :class:`str <python:str>`

        :param url: The URL to execute the request against.
        :type url: :class:`str <python:str>`

        :param parameters: URL parameters to submit with the request. Defaults to
          :obj:`None <python:None>`.
        :type parameters: :class:`dict <python:dict>` / :obj:`None <python:None>`

        :param headers: HTTP headers to submit with the request. Defaults to
          :obj:`None <python:None>`.
        :type headers: :class:`dict <python:dict>` / :obj:`None <python:None>`

        :param request_body: The data to supply in the body of the request. Defaults to
          :obj:`None <python:None>`.
        :type request_body: :obj:`None <python:None>` / :class:`dict <python:dict>` /
          :class:`str <python:str>` / :class:`bytes <python:bytes>`

        :returns: The content of the HTTP response, the status code of the HTTP response,
          and the headers of the HTTP response.
        :rtype: :class:`tuple <python:tuple>` of :class:`bytes <python:bytes>`,
          :class:`int <python:int>`, and :class:`dict <python:dict>`

        :raises ValueError: if ``method`` is not either ``GET``, ``HEAD``, ``POST``,
          ``PATCH``, ``PUT`` or ``DELETE``
        :raises ValueError: if ``url`` is not a valid URL
        :raises HTTPTimeoutError: if the request times out
        :raises SSLError: if the request fails SSL certificate verification
        :raises WalkScoreError: *or sub-classes* for other errors returned by the API

        """
        raise NotImplementedError(
            "HTTPClient subclasses must implement `_request`"
        )


    def request(self,
                method,
                url,
                parameters = None,
                headers = None,
                request_body = None):
        """Execute a standard HTTP request.

        :param method: The HTTP method to use for the request. Accepts `GET`, `HEAD`,
          `POST`, `PATCH`, `PUT`, or `DELETE`.
        :type method: :class:`str <python:str>`

        :param url: The URL to execute the request against.
        :type url: :class:`str <python:str>`

        :param parameters: URL parameters to submit with the request. Defaults to
          :obj:`None <python:None>`.
        :type parameters: :class:`dict <python:dict>` / :obj:`None <python:None>`

        :param headers: HTTP headers to submit with the request. Defaults to
          :obj:`None <python:None>`.
        :type headers: :class:`dict <python:dict>` / :obj:`None <python:None>`

        :param request_body: The data to supply in the body of the request. Defaults to
          :obj:`None <python:None>`.
        :type request_body: :obj:`None <python:None>` / :class:`dict <python:dict>` /
          :class:`str <python:str>` / :class:`bytes <python:bytes>`

        :returns: The content of the HTTP response, the status code of the HTTP response,
          and the headers of the HTTP response.
        :rtype: :class:`tuple <python:tuple>` of :class:`bytes <python:bytes>`,
          :class:`int <python:int>`, and :class:`dict <python:dict>`

        :raises ValueError: if ``method`` is not either ``GET``, ``HEAD``, ``POST``,
          ``PATCH``, ``PUT`` or ``DELETE``
        :raises ValueError: if ``url`` is not a valid URL
        :raises ValueError: if ``headers`` is not empty and is not a
          :class:`dict <python:dict>`

        :raises HTTPTimeoutError: if the request times out
        :raises SSLError: if the request fails SSL certificate verification
        :raises WalkScoreError: *or sub-classes* for other errors returned by the API

        """
        method = validators.string(method, allow_empty = False)
        method = method.upper()
        if method not in HTTP_METHODS:
            raise ValueError('method (%s) not a recognized HTTP method' % method)

        url = validators.url(url, allow_empty = False)

        parameters = validators.dict(parameters, allow_empty = True)
        headers = validators.dict(headers, allow_empty = True)


        content, status_code, headers = self._request(method,
                                                      url,
                                                      parameters,
                                                      headers,
                                                      request_body)

        check_for_errors(status_code, content)

        return content, status_code, headers

    def close(self):
        """Closes an existing HTTP connection/session."""

        raise NotImplementedError(
            "HTTPClient subclasses must implement `close`"
        )


class RequestsClient(HTTPClient):
    """:class:`HTTPClient` for the :doc:`requests <requests:index>` library."""

    name = "requests"

    def __init__(self,
                 timeout = 80,
                 session = None,
                 **kwargs):
        super(RequestsClient, self).__init__(**kwargs)

        self._session = session
        self._timeout = timeout

    def _request(self,
                 method,
                 url,
                 parameters = None,
                 headers = None,
                 request_body = None):
        """Execute a standard HTTP request.

        :param method: The HTTP method to use for the request. Accepts `GET`, `HEAD`,
          `POST`, `PATCH`, `PUT`, or `DELETE`.
        :type method: :class:`str <python:str>`

        :param url: The URL to execute the request against.
        :type url: :class:`str <python:str>`

        :param parameters: URL parameters to submit with the request. Defaults to
          :obj:`None <python:None>`.
        :type parameters: :class:`dict <python:dict>` / :obj:`None <python:None>`

        :param headers: HTTP headers to submit with the request. Defaults to
          :obj:`None <python:None>`.
        :type headers: :class:`dict <python:dict>` / :obj:`None <python:None>`

        :param request_body: The data to supply in the body of the request. Defaults to
          :obj:`None <python:None>`.
        :type request_body: :obj:`None <python:None>` / :class:`dict <python:dict>` /
          :class:`str <python:str>` / :class:`bytes <python:bytes>`

        :returns: The content of the HTTP response, the status code of the HTTP response,
          and the headers of the HTTP response.
        :rtype: :class:`tuple <python:tuple>` of :class:`bytes <python:bytes>`,
          :class:`int <python:int>`, and :class:`dict <python:dict>`

        :raises ValueError: if ``method`` is not either ``GET``, ``HEAD``, ``POST``,
          ``PATCH``, ``PUT`` or ``DELETE``
        :raises ValueError: if ``url`` is not a valid URL
        :raises HTTPTimeoutError: if the request times out
        :raises SSLError: if the request fails SSL certificate verification
        :raises WalkScoreError: *or sub-classes* for other errors returned by the API

        """
        kwargs = {}
        if self._verify_ssl_certs:
            kwargs["verify"] = CA_BUNDLE_PATH
        else:
            kwargs["verify"] = False

        if self._proxy:
            kwargs["proxies"] = self._proxy

        if getattr(self._thread_local, "session", None) is None:
            self._thread_local.session = self._session or requests.Session()

        try:
            try:
                result = self._thread_local.session.request(method,
                                                            url,
                                                            params = parameters,
                                                            headers = headers,
                                                            data = request_body,
                                                            timeout = self._timeout,
                                                            **kwargs)
            except TypeError as error:
                raise TypeError(
                    "Warning: It looks like your installed version of the "
                    '"requests" library is not compatible with WalkScore\'s '
                    "usage thereof. (HINT: The most likely cause is that "
                    'your "requests" library is out of date. You can fix '
                    'that by running "pip install -U requests".) The '
                    "underlying error was: %s" % (error,)
                )

            # This causes the content to actually be read, which could cause
            # e.g. a socket timeout. TODO: The other fetch methods probably
            # are susceptible to the same and should be updated.
            content = result.content
            status_code = result.status_code
        except Exception as error:                                                        # pylint: disable=W0703
            # Would catch just requests.exceptions.RequestException, but can
            # also raise ValueError, RuntimeError, etc.
            WalkScoreError.from_exception(error)

        return content, status_code, result.headers

    def close(self):
        """Closes an existing HTTP connection/session."""

        if getattr(self._thread_local, "session", None) is not None:
            self._thread_local.session.close()


class UrlFetchClient(HTTPClient):
    """class:`HTTPClient` for the :doc:`urlfetch <urlfetch:index>` library."""

    name = "urlfetch"

    def __init__(self,
                 verify_ssl_certs = True,
                 proxy = None,
                 deadline = 55):
        super(UrlFetchClient, self).__init__(verify_ssl_certs = verify_ssl_certs,
                                             proxy = proxy)

        # no proxy support in urlfetch. for a patch, see:
        # https://code.google.com/p/googleappengine/issues/detail?id=544
        if proxy:
            raise ValueError(
                "No proxy support in urlfetch library. "
                "Set walkscore.default_http_client to either RequestsClient, "
                "PycurlClient, or Urllib2Client instance to use a proxy."
            )

        self._verify_ssl_certs = verify_ssl_certs

        # GAE requests time out after 60 seconds, so make sure to default
        # to 55 seconds to allow for a slow WalkScore API
        self._deadline = deadline

    def _request(self,
                 method,
                 url,
                 parameters = None,
                 headers = None,
                 request_body = None):
        try:
            result = urlfetch.request(
                url = url,
                method = method,
                params = parameters,
                headers = headers,
                # Google App Engine doesn't let us specify our own cert bundle.
                # However, that's ok because the CA bundle they use recognizes
                # api.stripe.com.
                validate_certificate = self._verify_ssl_certs,
                deadline = self._deadline,
                data = request_body,
            )
        except urlfetch.Error as error:
            if isinstance(error, urlfetch.InvalidURLError):
                raise BindingError(
                    "The WalkScore library attempted to fetch an "
                    "invalid URL (%r). This is likely due to a bug "
                    "in the WalkScore Python bindings. Please let us know "
                    "at software@insightindustry.com." % (url,)
                )
            elif isinstance(error, urlfetch.DownloadError):
                message = "There was a problem retrieving data from WalkScore."
            elif isinstance(error, urlfetch.ResponseTooLargeError):
                message = (
                    "There was a problem receiving all of your data from "
                    "WalkScore.  This is likely due to a bug in WalkScore. "
                )
            else:
                message = (
                    "Unexpected error communicating with WalkScore. If this "
                    "problem persists, let us know at software@insightindustry.com."
                )

            raise InternalAPIError(message)

        return result.content, result.status_code, result.headers

    def close(self):
        pass


class PycurlClient(HTTPClient):
    """class:`HTTPClient` for the `pycurl <http://pycurl.io/docs/latest/index.html>`_
    library.
    """

    name = "pycurl"

    def __init__(self,
                 verify_ssl_certs = True,
                 proxy = None):
        super(PycurlClient, self).__init__(verify_ssl_certs = verify_ssl_certs,
                                           proxy = proxy)

        # Initialize this within the object so that we can reuse connections.
        self._curl = pycurl.Curl()

        # need to urlparse the proxy, since PyCurl
        # consumes the proxy url in small pieces
        if self._proxy:
            # now that we have the parser, get the proxy url pieces
            for scheme in self._proxy:
                self._proxy[scheme] = urlparse(self._proxy[scheme])

    def parse_headers(self, data):                                                        # pylint: disable=R0201
        """Parse headers into a :class:`dict <python:dict>`

        :param data: A string-like object with header data.
        :type data: :class:`bytes <python:bytes>` / :class:`str <python:str>`

        :returns: Dictionary of HTTP headers.
        :rtype: :class:`dict <python:dict>`
        """
        if "\r\n" not in data:
            return {}
        raw_headers = data.split("\r\n", 1)[1]
        headers = email.message_from_string(raw_headers)

        return dict((k.lower(), v) for k, v in six.iteritems(dict(headers)))

    def _request(self,
                 method,
                 url,
                 parameters = None,
                 headers = None,
                 request_body = None):
        if isinstance(request_body, dict):
            request_body = json.dumps(request_body)

        b = io.BytesIO()
        rheaders = io.BytesIO()

        # Pycurl's design is a little weird: although we set per-request
        # options on this object, it's also capable of maintaining established
        # connections. Here we call reset() between uses to make sure it's in a
        # pristine state, but notably reset() doesn't reset connections, so we
        # still get to take advantage of those by virtue of re-using the same
        # object.
        self._curl.reset()

        proxy = self._get_proxy(url)
        if proxy:
            if proxy.hostname:
                self._curl.setopt(pycurl.PROXY, proxy.hostname)
            if proxy.port:
                self._curl.setopt(pycurl.PROXYPORT, proxy.port)
            if proxy.username or proxy.password:
                self._curl.setopt(
                    pycurl.PROXYUSERPWD,
                    "%s:%s" % (proxy.username, proxy.password),
                )

        if method == "GET":
            self._curl.setopt(pycurl.HTTPGET, 1)
        elif method == 'HEAD':
            self._curl.setopt(pycurl.NOBODY, 1)
        elif method == "POST":
            self._curl.setopt(pycurl.POST, 1)
            self._curl.setopt(pycurl.POSTFIELDS, request_body)
        elif method == 'PUT':
            self._curl.setopt(pycurl.CUSTOMREQUEST, 'PUT')
            self._curl.setopt(pycurl.POSTFIELDS, request_body)
        elif method == 'PATCH':
            self._curl.setopt(pycurl.CUSTOMREQUEST, 'PATCH')
            self._curl.setopt(pycurl.POSTFIELDS, request_body)
        else:
            self._curl.setopt(pycurl.CUSTOMREQUEST, method.upper())

        # pycurl doesn't like unicode URLs
        if parameters:
            parameter_string = base_urllib.urlencode(parameters)

            url += '?' + parameter_string

        url = to_utf8(url)
        self._curl.setopt(pycurl.URL, url)

        self._curl.setopt(pycurl.WRITEFUNCTION, b.write)
        self._curl.setopt(pycurl.HEADERFUNCTION, rheaders.write)
        self._curl.setopt(pycurl.NOSIGNAL, 1)
        self._curl.setopt(pycurl.CONNECTTIMEOUT, 30)
        self._curl.setopt(pycurl.TIMEOUT, 80)

        if headers:
            self._curl.setopt(
                pycurl.HTTPHEADER,
                ["%s: %s" % (k, v) for k, v in six.iteritems(dict(headers))],
            )

        if self._verify_ssl_certs:
            self._curl.setopt(pycurl.CAINFO, CA_BUNDLE_PATH)
        else:
            self._curl.setopt(pycurl.SSL_VERIFYHOST, False)

        try:
            self._curl.perform()
        except pycurl.error as error:
            self._handle_request_error(error)

        rbody = b.getvalue().decode("utf-8")
        rcode = self._curl.getinfo(pycurl.RESPONSE_CODE)
        headers = self.parse_headers(rheaders.getvalue().decode("utf-8"))

        return rbody, rcode, headers

    @classmethod
    def _handle_request_error(cls, error):
        if error.args[0] == pycurl.E_OPERATION_TIMEOUTED:
            raise HTTPTimeoutError('Could not connect to the WalkScore API. '
                                   'Please check your internet connection and try again. ')
        elif error.args[0] == [pycurl.E_COULDNT_CONNECT,
                               pycurl.E_COULDNT_RESOLVE_HOST]:
            raise HTTPConnectionError("Could not connect to WalkScore.  Please check "
                                      "your internet connection and try again.")
        elif error.args[0] in [pycurl.E_SSL_CACERT,
                               pycurl.E_SSL_PEER_CERTIFICATE]:
            raise SSLError("Could not verify WalkScore's SSL certificate.  Please make "
                           "sure that your network is not intercepting certificates.")
        else:
            raise HTTPConnectionError(
                "Unexpected error communicating with the WalkScore API. If this "
                "problem persists, let us know at software@insightindustry.com."
            )

    def _get_proxy(self, url):
        if self._proxy:
            proxy = self._proxy
            scheme = url.split(":")[0] if url else None
            if scheme:
                if scheme in proxy:
                    return proxy[scheme]

                scheme = scheme[0:-1]

                if scheme in proxy:
                    return proxy[scheme]

        return None

    def close(self):
        pass


class Urllib2Client(HTTPClient):
    """class:`HTTPClient` for the :doc:`urllib2` package.
    """

    name = "urllib.request"

    def __init__(self,
                 verify_ssl_certs = True,
                 proxy = None):
        super(Urllib2Client, self).__init__(verify_ssl_certs = verify_ssl_certs,
                                            proxy = proxy)

        # prepare and cache proxy tied opener here
        self._opener = None
        if self._proxy:
            proxy = urllib.request.ProxyHandler(self._proxy)
            self._opener = urllib.request.build_opener(proxy)

    def _request(self,
                 method,
                 url,
                 parameters = None,
                 headers = None,
                 request_body = None):
        request_body = to_utf8(request_body)

        if parameters:
            parameter_string = base_urllib.urlencode(parameters)
            url += '?' + parameter_string

        request = urllib.request.Request(url, request_body, headers)

        if method not in ("GET", "POST"):
            request.get_method = method

        try:
            # use the custom proxy tied opener, if any.
            # otherwise, fall to the default urllib opener.
            if self._opener:
                response = self._opener.open(request)
            else:
                response = urllib.request.urlopen(request)

            rbody = response.read()
            rcode = response.code
            response_headers = dict(response.info())
        except urllib.error.HTTPError as error:
            rcode = error.code
            rbody = error.read()
            response_headers = dict(error.info())
        except (urllib.error.URLError, ValueError) as error:
            WalkScoreError.from_exception(error)

        response_headers = dict((k.lower(), v) for k, v
                                in six.iteritems(dict(response_headers)))

        return rbody, rcode, response_headers

    def close(self):
        pass
