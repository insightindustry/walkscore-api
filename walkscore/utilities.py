# -*- coding: utf-8 -*-

"""
################################
walkscore.utilities
################################

Implements utility functions used by the library.

"""
import os
import sys
from functools import wraps

from validator_collection import checkers, validators

import walkscore.errors as errors

CA_BUNDLE_PATH = os.path.join(
    os.path.dirname(__file__), "data/ca-certificates.crt"
)

_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)


def to_utf8(value):
    """Return a UTF-8 encoded version of ``value`` if ``value`` is a string.

    :returns: ``value`` if ``value`` is not a string or UTF-8 encoded
      :class:`str <python:str>`
    """
    if is_py2 and checkers.is_string(value, coerce_value = True):
        value = validators.string(value, coerce_value = True)
        return value.encode("utf-8")

    return value


def check_for_errors(response, status_code, headers):
    """Check the HTTP Status Code and the response for errors and raise an
    appropriate exception. Otherwise return the result as-is.

    :param response: The content of the response.
    :type response: :class:`bytes <python:bytes>`

    :param status_code: The HTTP Status Code returned.
    :type status_code: :class:`int <python:int>`

    :param headers: The HTTP Headers returned.
    :type headers: :class:`dict <python:dict>`

    :returns: The content of the HTTP response, the status code of the HTTP response,
      and the headers of the HTTP response.
    :rtype: :class:`tuple <python:tuple>` of :class:`bytes <python:bytes>`,
      :class:`int <python:int>`, and :class:`dict <python:dict>`

    """
    status_code = validators.integer(status_code, allow_empty = False)
    try:
        json_response = validators.json(response, allow_empty = True)
    except ValueError:
        if isinstance(response, bytes):
            response = response.decode('utf-8')
            
        json_response = validators.json(response, allow_empty = True)

    status_code, error_type, message = errors.parse_http_error(status_code,
                                                               response)
    if not error_type:
        ws_status = json_response.get('status', None)
        error_value = errors.DEFAULT_ERROR_CODES.get(ws_status, None)
        if error_value:
            error_type = errors.ERROR_TYPES.get(error_value, None)

    if error_type:
        raise error_type(message)

    return response, status_code, headers
