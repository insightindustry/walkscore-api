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

from tests.fixtures import input_files, check_input_file
from walkscore.api import WalkScoreAPI
from walkscore.locationscore import LocationScore
from walkscore import errors

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

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


@pytest.mark.parametrize('use_key_from_env, api_key_override, address, longitude_latitude, return_transit_score, return_bike_score, expected_status, error', [
    (True, None, '1119 8th Avenue Seattle, WA 98101', (-122.3295, 47.6085), True, True, 1, None),
    (True, None, '1119 8th Avenue Seattle, WA 98101', None, True, True, 30, TypeError),
    (True, None, '1119 8th Avenue Seattle, WA 98101', (-122.3295, None), True, True, 30, errors.InvalidCoordinatesError),
    (True, None, None, (-122.3295, 47.6085), True, True, 1, None),
    (False, None, '1119 8th Avenue Seattle, WA 98101', (-122.3295, 47.6085), True, True, 1, errors.AuthenticationError),
    (False, 'invalid api key', '1119 8th Avenue Seattle, WA 98101', (-122.3295, 47.6085), True, True, 1, errors.AuthenticationError),

    (True, None, '1119 8th Avenue Seattle, WA 98101', (-122.3295, 47.6085), True, False, 1, None),
    (True, None, '1119 8th Avenue Seattle, WA 98101', (-122.3295, 47.6085), False, True, 1, None),
    (True, None, '1119 8th Avenue Seattle, WA 98101', (-122.3295, 47.6085), False, False, 1, None),

])
def test_get_score(use_key_from_env, api_key_override, address, longitude_latitude, return_transit_score, return_bike_score, expected_status, error):
    if api_key_override:
        api_key = api_key_override
    elif use_key_from_env:
        api_key = DEFAULT_API_KEY
    else:
        api_key = None

    api = WalkScoreAPI(api_key = api_key)

    if not error:
        if longitude_latitude:
            result = api.get_score(latitude = longitude_latitude[1],
                                   longitude = longitude_latitude[0],
                                   address = address,
                                   return_transit_score = return_transit_score,
                                   return_bike_score = return_bike_score)

        else:
            result = api.get_score(address = address)
    else:
        with pytest.raises(error):
            if longitude_latitude:
                result = api.get_score(latitude = longitude_latitude[1],
                                       longitude = longitude_latitude[0],
                                       address = address,
                                       return_transit_score = return_transit_score,
                                       return_bike_score = return_bike_score)
            else:
                result = api.get_score(address = address)

    if not error:
        assert result is not None
        assert isinstance(result, LocationScore) is True
        assert result.status == expected_status
        assert result.walk_score is not None
        assert checkers.is_numeric(result.walk_score) is True

        if return_transit_score:
            assert result.transit_score is not None
            assert checkers.is_numeric(result.transit_score) is True
        else:
            assert result.transit_score is None
        if return_bike_score:
            assert result.bike_score is not None
            assert checkers.is_numeric(result.bike_score) is True
        else:
            assert result.bike_score is None
