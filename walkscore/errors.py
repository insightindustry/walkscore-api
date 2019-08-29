# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member class documentation is automatically incorporated
# there as needed.

from validator_collection import validators

class WalkScoreError(ValueError):
    """Base error raised by **WalkScore**. Inherits from
    :class:`ValueError <python:ValueError>`.
    """
    pass

class InternalAPIError(WalkScoreError):
    """Internal error within the WalkScore API itself. Inherits from
    :class:`WalkScoreError`.
    """
    pass

class AuthenticationError(WalkScoreError):
    """Error raised when attempting to retrieve a score with an invalid API key."""
    pass

class BlockedIPError(WalkScoreError):
    """Error raised when attempting to retrieve a score from a blocked IP address."""
    pass

class QuotaError(WalkScoreError):
    """Error raised when you have exceeded your daily quota."""
    pass

class ScoreInProgressError(WalkScoreError):
    """Error raised when a score for the location supplied is being calculated
    and is not yet available."""
    pass

class InvalidCoordinatesError(WalkScoreError):
    """Error raised when the coordinates supplied for a location are invlaid."""
    pass

class BindingError(WalkScoreError):
    """Error produced when the WalkScore Library has an incorrect API
    binding.
    """
    status_code = 500

class HTTPConnectionError(WalkScoreError):
    """Error produced when the WalkScore Library is unable to connect to the API, but
    did not time out.
    """
    status_code = 500


class HTTPTimeoutError(HTTPConnectionError):
    """Error produced when the API times out or returns a ``Status Code: 504``.

    This error indicates that the underlying API timed out and did not return a result.
    """
    status_code = 504

class SSLError(WalkScoreError):
    """Error produced when an SSL certificate cannot be verified, returns a
    ``Status Code: 495``.
    """
    status_code = 495


def parse_http_error(status_code, http_response):
    """Return the error based on the ``http_response`` received.

    :param status_code: The original status code received.
    :type status_code: :class:`int <python:int>`

    :param http_response: The HTTP response that was retrieved.

    :returns: Tuple with:

      * the status code received,
      * the error type received,
      * the error message received
    """
    try:
        status_code = http_response.status_code
    except AttributeError:
        pass

    error_type = DEFAULT_ERROR_CODES.get(status_code, None)
    message = None

    try:
        response_json = http_response.json()
        message = response_json.get('message', message)
    except ValueError:
        message = http_response.text
    except AttributeError:
        try:
            message = http_response.decode('utf-8')
        except AttributeError:
            message = http_response

    if isinstance(error_type, str):
        error_type = ERROR_TYPES.get(error_type, None)

    if not error_type and status_code >= 500:
        error_type = InternalAPIError

    return status_code, error_type, message

# pylint: disable=R1711
def check_for_errors(status_code, http_response = None):
    """Raise an error based on the ``status_code`` received.

    :param status_code: The status code whose error should be returned.
    :type status_code: :class:`int <python:int>`

    :param http_response: The HTTP response object that will be parsed to determine
      the message.

    :returns: :obj:`None <python:None>` if no error matches ``status_code``
    :raises WalkScoreError: or a sub-type thereof based on ``status_code``

    """
    status_code, error_type, message = parse_http_error(status_code, http_response)
    if error_type:
        print(error_type)
        raise error_type(message)

    return None
# pylint: enable=R1711

DEFAULT_ERROR_CODES = {
    500: 'WalkScoreError',
    401: 'AuthenticationError',
    403: 'AuthorizationError',
    404: 'ResourceNotFoundError',
    409: 'WalkScoreError',
    504: 'HTTPTimeoutError',
    495: 'SSLError',
    2: 'ScoreInProgressError',
    30: 'InvalidCoordinatesError',
    31: 'InternalAPIError',
    40: 'AuthenticationError',
    41: 'QuotaError'
}

ERROR_TYPES = {
    'WalkScoreError': WalkScoreError,
    'AuthenticationError': AuthenticationError,
    'AuthorizationError': BlockedIPError,
    'ResourceNotFoundError': InvalidCoordinatesError,
    'ConflictError': WalkScoreError,
    'HTTPTimeoutError': HTTPTimeoutError,
    'SSLError': SSLError,
    'InvalidURLError': BindingError,
    'DownloadError': WalkScoreError,
    'ResponseTooLargeError': InternalAPIError,
    'HTTPConnectionError': HTTPConnectionError,
    'URLError': BindingError,
    'ValueError': WalkScoreError,
    'InternalAPIError': InternalAPIError,
    'QuotaError': QuotaError,
    'InvalidCoordinatesError': InvalidCoordinatesError,
    'ScoreInProgressError': ScoreInProgressError
}
