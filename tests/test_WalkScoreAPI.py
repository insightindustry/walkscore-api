# -*- coding: utf-8 -*-

"""
******************************************
tests.test_WalkScoreAPI
******************************************

Tests for the :class:`LocationScore` class.

"""
# pylint: disable=line-too-long

import os

import pytest
import datetime
try:
    import simplejson as json
except ImportError:
    import json

from validator_collection import checkers
from dotenv import load_dotenv

from tests.fixtures import input_files, check_input_file
from walkscore.api import WalkScoreAPI
from walkscore.locationscore import LocationScore
from walkscore import errors

load_dotenv()

DEFAULT_API_KEY = os.getenv('TEST_API_KEY', None)

@pytest.mark.parametrize('use_key_from_env, api_key_override', [
    (True, None),
    (True, 'custom-api-key'),
    (False, None),
    (False, 'custom-api-key'),
])
def test__init__(use_key_from_env, api_key_override):
    if api_key_override:
        api_key = api_key_override
    elif use_key_from_env:
        api_key = DEFAULT_API_KEY
    else:
        api_key = None

    result = WalkScoreAPI(api_key = api_key)

    assert result is not None
    assert isinstance(result, WalkScoreAPI) is True
    if api_key:
        assert result.api_key is not None
        assert result.api_key == api_key


@pytest.mark.parametrize('use_key_from_env, api_key_override, address, longitude_latitude, expected_status, error', [
    (True, None, '1119 8th Avenue Seattle, WA 98101', (-122.3295, 47.6085), 1, None),
    (True, None, '1119 8th Avenue Seattle, WA 98101', None, 30, errors.InvalidCoordinatesError),
    (True, None, '1119 8th Avenue Seattle, WA 98101', (-122.3295, None), 30, errors.InvalidCoordinatesError),
    (True, None, None, (-122.3295, 47.6085), 1, None),
    (False, None, '1119 8th Avenue Seattle, WA 98101', (-122.3295, 47.6085), 1, errors.AuthenticationError),
    (False, 'invalid api key', '1119 8th Avenue Seattle, WA 98101', (-122.3295, 47.6085), 1, errors.AuthenticationError),
])
def test_get_score(use_key_from_env, api_key_override, address, longitude_latitude, expected_status, error):
    if api_key_override:
        api_key = api_key_override
    elif use_key_from_env:
        api_key = DEFAULT_API_KEY
    else:
        api_key = None

    api = WalkScoreAPI(api_key = api_key)

    if not error:
        if longitude_latitude:
            result = api.get_score(address = address,
                                   latitude = longitude_latitude[1],
                                   longitude = longitude_latitude[0])
        else:
            result = api.get_score(address = address)
    else:
        with pytest.raises(error):
            if longitude_latitude:
                result = api.get_score(address = address,
                                       latitude = longitude_latitude[1],
                                       longitude = longitude_latitude[0])
            else:
                result = api.get_score(address = address)

    if not error:
        assert result is not None
        assert isinstance(result, LocationScore) is True
        assert result.status == expected_status