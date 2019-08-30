# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

import os

from validator_collection import validators

from walkscore.http_client import default_http_client
from walkscore.locationscore import LocationScore
from walkscore.utilities import check_for_errors
from walkscore.errors import AuthenticationError, InvalidCoordinatesError


class WalkScoreAPI(object):
    """The Python object which exposes the WalkScore API's functionality."""

    _BASE_URL = 'http://api.walkscore.com'
    _SCORE_ENDPOINT = '/score'

    def __init__(self,
                 api_key = None,
                 http_client = None,
                 proxy = None,
                 max_retries = None):
        """

        :param api_key: The API key provided by WalkScore used to authenticate
          your application. If :obj:`None <python:None>` or not specified will
          default to the ``WALKSCORE_API_KEY`` environment variable if present,
          and :obj:`None <python:None>` if not.
        :type api_key: :class:`str <python:str>` / :obj:`None <python:None>`

        :param http_client: The HTTP client instance to use for the execution of requests.
          If not overridden, will default to
          `urlfetch <https://github.com/ifduyue/urlfetch>`_,
          `requests <https://github.com/kennethreitz/requests>`_,
          `pycurl <https://github.com/pycurl/pycurl>`_,
          :doc:`urllib2 <python:urllib2>` in order based on whether they are available
          in the environment.

          .. tip::

            You can override the HTTP client by supplying a
            :class:`HTTPClient <walkscore.HTTPClient>` instance to the method.

        :type http_client: :class:`HTTPClient <walkscore.http_client>`

        :param proxy: The URL to use as an HTTP proxy. Defaults to
          :obj:`None <python:None>`.
        :type proxy: :class:`str <python:str>` / :obj:`None <python:None>`

        :param max_retries: Determines the maximum number of HTTP request attempts to
          make on network failure before giving up. If not specified, defaults to
          environment variable ``BACKOFF_DEFAULT_TRIES`` or ``3`` if not available.
        :type max_retries: :class:`int <python:int>`

        """
        self._api_key = None
        self._http_client = None
        self._proxy = None
        self._max_retries = None

        if not api_key:
            api_key = os.getenv('WALKSCORE_API_KEY', None)

        self.api_key = api_key
        self.http_client = http_client
        self.proxy = proxy
        self.max_retries = max_retries

    @property
    def api_key(self):
        """The API key used to sign requests made against the API.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = validators.string(value, allow_empty = True)

    @property
    def http_client(self):
        """The object instance to use as the HTTP client to make HTTP requests against
        the WalkScore API.

        :rtype: :class:`HTTPClient <walkscore.HTTPClient>`
        """
        if not self._http_client:
            return default_http_client(proxy = self.proxy)

        return self._http_client

    @http_client.setter
    def http_client(self, value):
        if value and not checkers.is_type(value, 'HTTPClient'):
            raise ValueError('http_client must be of type "HTTPClient", was "%s"' %
                             str(type(value)))

        self._http_client = value

    @property
    def proxy(self):
        """The URL to use as a proxy for requests made to the WalkScore API.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._proxy

    @proxy.setter
    def proxy(self, value):
        self._proxy = validators.url(value, allow_empty = True)
        self.http_client.proxy = self._proxy

    @property
    def max_retries(self):
        """The number of attempts to make on network connectivity-related API failures.

        :rtype: :class:`int <python:int>`
        """
        if not self._max_retries:
            return validators.integer(os.getenv('BACKOFF_DEFAULT_TRIES', '3'))

        return self._max_retries

    @max_retries.setter
    def max_retries(self, value):
        self._max_retries = validators.integer(value, allow_empty = True)

    @property
    def _API_URL(self):
        """The full URL to use when requesting scores from the WalkScore API.

        :rtype: :class:`str <python:str>`
        """
        return self._BASE_URL + self._SCORE_ENDPOINT

    def get_score(self,
                  latitude,
                  longitude,
                  address = None,
                  return_transit_score = True,
                  return_bike_score = True,
                  max_retries = None):
              """Retrieve the :term:`WalkScore`, :term:`TransitScore`, and/or
              :term:`BikeScore` for a given location from the WalkScore API.

              :param latitude: The latitude of the location whose score(s) should
                be retrieved.
              :type latitude: numeric

              :param longitude: The longitude of the location whose score(s) should
                be retrieved.
              :type longitude: numeric

              :param address: The address whose score(s) should be retrieved.
                Defaults to :obj:`None <python:None>`.
              :type address: :class:`str <python:str>` / :obj:`None <python:None>`

              :param return_transit_score: If ``True``, will
                return the location's :term:`TransitScore`. Defaults to
                ``True``.
              :type return_transit_score: :class:`bool <python:bool>`

              :param return_bike_score: If ``True``, will
                return the location's :term:`BikeScore`. Defaults to
                ``True``.
              :type return_bike_score: :class:`bool <python:bool>`

              :param max_retries: The maximum number of retries to attempt if the
                WalkScore API times out or otherwise fails to return a response.
                If :obj:`None <python:None>`, will apply the default the configured
                when initializing the WalkScore API object. To suppress all retries,
                set to 0. Defaults to :obj:`None <python:None>`.
              :type max_retries: :obj:`None <python:None>` / :class:`int <python:int>`

              :returns: The location's :term:`WalkScore`, :term:`TransitScore`,
                and :term:`BikeScore` with meta-data.
              :rtype: :class:`LocationScore <walkscore.locationscore.LocationScore>`

              :raises AuthenticationError: if the API key is invalid
              :raises ScoreInProgressError: if the score is being calculated and is not
                currently available
              :raises WalkScoreError: if an internal WalkScore API error occurred
              :raises QuotaError: if your daily quota has been exceeded
              :raises BlockedIPError: if your IP address has been blocked
              :raises InvalidCoordinatesError: if your latitude/longitude coordinates
                are not valid

              """
              if not self.api_key:
                  raise AuthenticationError('No API key supplied.')

              if not (latitude and longitude):
                  raise InvalidCoordinatesError('No coordinates supplied.')

              if latitude:
                  latitude = validators.numeric(latitude, allow_empty = False)
                  latitude = str(latitude)
              if longitude:
                  longitude = validators.numeric(longitude, allow_empty = False)
                  longitude = str(longitude)

              if max_retries is None:
                  max_retries = self.max_retries

              method = 'GET'
              parameters = {
                  'address': address,
                  'lat': latitude,
                  'lon': longitude,
                  'format': 'json',
                  'transit': 1,
                  'bike': 1,
                  'wsapikey': self.api_key
              }

              if not return_bike_score:
                  parameters['bike'] = None

              if not return_transit_score:
                  parameters['transit'] = None

              if max_retries:
                  response = self.http_client.request_with_retries(method,
                                                                   self._API_URL,
                                                                   parameters = parameters,
                                                                   request_body = None)
              else:
                  response = self.http_client.request(method,
                                                      self._API_URL,
                                                      parameters = parameters,
                                                      request_body = None)

              result_set = check_for_errors(*response)

              result = LocationScore.from_json(result_set[0],
                                               api_compatible = True)

              result.address = address
              result.original_latitude = latitude
              result.original_longitude = longitude

              return result
