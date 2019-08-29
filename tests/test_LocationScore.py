# -*- coding: utf-8 -*-

"""
******************************************
tests.test_LocationScore
******************************************

Tests for the :class:`LocationScore` class.

"""
# pylint: disable=line-too-long

import pytest
import datetime
try:
    import simplejson as json
except ImportError:
    import json

from validator_collection import checkers

from tests.fixtures import input_files, check_input_file
from walkscore.locationscore import LocationScore


@pytest.mark.parametrize('arguments, error', [
    (None, None),
    ({
         'walk_score': 12,
         'walk_description': 'Test Description!',
         'walk_updated': datetime.datetime.now(),
         'transit_score': 34,
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'http://www.someurl.com',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, None),
    ({
         'walk_score': 12,
         'walk_description': 'Test Description!',
         'walk_updated': 'not a datetime',
         'transit_score': 34,
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'http://www.someurl.com',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, TypeError),
    ({
         'walk_score': 12,
         'walk_description': 'Test Description!',
         'walk_updated': datetime.datetime.now(),
         'transit_score': 'not-a-number',
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'http://www.someurl.com',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, TypeError),
    ({
         'walk_score': 12,
         'walk_description': 'Test Description!',
         'walk_updated': datetime.datetime.now(),
         'transit_score': 34,
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'not a url',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, TypeError),
])
def test_LocationScore__init__(arguments, error):
    if arguments and not error:
        result = LocationScore(**arguments)
    elif arguments and error:
        with pytest.raises(error):
            result = LocationScore(**arguments)
    elif not arguments:
        result = LocationScore()

    if not error:
        assert isinstance(result, LocationScore) is True


@pytest.mark.parametrize('arguments, api_compatible, expected_result, error', [
    (None, False, {
          'status': None,
          'walk': {
              'score': None,
              'description': None,
              'updated': None
          },
          'transit': {
              'score': None,
              'description': None,
              'summary': None,
          },
          'bike': {
              'score': None,
              'description': None,
          },
          'logo_url': None,
          'more_info_icon': None,
          'more_info_link': None,
          'help_link': None,
          'property_page_link': None,
          'snapped_coordinates': {
              'latitude': None,
              'longitude': None
          },
          'original_coordinates': {
              'address': None,
              'latitude': None,
              'longitude': None
          }
    }, None),
    (None, True, {
          'status': None,
          'walkscore': None,
          'description': None,
          'updated': None,
          'transit': {
              'score': None,
              'description': None,
              'summary': None,
          },
          'bike': {
              'score': None,
              'description': None,
          },
          'logo_url': None,
          'more_info_icon': None,
          'more_info_link': None,
          'help_link': None,
          'ws_link': None,
          'snapped_lat': None,
          'snapped_lon': None
    }, None),
    ({
         'walk_score': 12,
         'walk_description': 'Test Description!',
         'walk_updated': datetime.datetime.now(),
         'transit_score': 34,
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'http://www.someurl.com',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, False, {
          'status': None,
          'walk': {
              'score': 12,
              'description': 'Test Description!',
              'updated': datetime.datetime.now()
          },
          'transit': {
              'score': 34,
              'description': 'Test Description!',
              'summary': 'Test Summary!',
          },
          'bike': {
              'score': 56,
              'description': 'Test Description!',
          },
          'logo_url': 'http://www.test.com',
          'more_info_icon': 'http://www.someurl.com',
          'more_info_link': 'http://www.someurl.com',
          'help_link': 'http://www.someurl.com',
          'property_page_link': 'http://www.someurl.com',
          'snapped_coordinates': {
              'latitude': None,
              'longitude': None
          },
          'original_coordinates': {
              'address': '123 Anyplace St, Anywhere, AK 12345',
              'latitude': 123.45,
              'longitude': 123.45
          }
    }, None),
    ({
         'walk_score': 12,
         'walk_description': 'Test Description!',
         'walk_updated': datetime.datetime.now(),
         'transit_score': 34,
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'http://www.someurl.com',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, True, {
          'status': None,
          'walkscore': 12,
          'description': 'Test Description!',
          'updated': datetime.datetime.now(),
          'transit': {
              'score': 34,
              'description': 'Test Description!',
              'summary': 'Test Summary!'
          },
          'bike': {
              'score': 56,
              'description': 'Test Description!'
          },
          'logo_url': 'http://www.test.com',
          'more_info_icon': 'http://www.someurl.com',
          'more_info_link': 'http://www.someurl.com',
          'help_link': 'http://www.someurl.com',
          'ws_link': 'http://www.someurl.com',
          'snapped_lat': None,
          'snapped_lon': None
    }, None),
])
def test_LocationScore_to_dict(arguments, api_compatible, expected_result, error):
    if arguments and not error:
        obj = LocationScore(**arguments)
    elif not arguments and not error:
        obj = LocationScore()

    if not error:
        result = obj.to_dict(api_compatible = api_compatible)
    else:
        with pytest.raises(error):
            result = obj.to_dict(api_compatible = api_compatible)

    if not error:
        assert result is not None
        assert checkers.are_dicts_equivalent(result, expected_result) is True


@pytest.mark.parametrize('obj, api_compatible, error', [
    (None, False, None),
    (None, True, None),
    ({
          'status': None,
          'walk': {
              'score': None,
              'description': None,
              'updated': None
          },
          'transit': {
              'score': None,
              'description': None,
              'summary': None,
          },
          'bike': {
              'score': None,
              'description': None,
          },
          'logo_url': None,
          'more_info_icon': None,
          'more_info_link': None,
          'help_link': None,
          'property_page_link': None,
          'snapped_coordinates': {
              'latitude': None,
              'longitude': None
          },
          'original_coordinates': {
              'address': None,
              'latitude': None,
              'longitude': None
          }
    }, False, None),
    ({
          'status': None,
          'walk': {
              'score': None,
              'description': None,
              'updated': None
          },
          'transit': {
              'score': None,
              'description': None,
              'summary': None,
          },
          'bike': {
              'score': None,
              'description': None,
          },
          'logo_url': None,
          'more_info_icon': None,
          'more_info_link': None,
          'help_link': None,
          'property_page_link': None,
          'snapped_coordinates': {
              'latitude': None,
              'longitude': None
          },
          'original_coordinates': {
              'address': None,
              'latitude': None,
              'longitude': None
          }
    }, True, None),
    ({
          'status': None,
          'walkscore': 12,
          'description': 'Test Description!',
          'updated': datetime.datetime.now(),
          'transit': {
              'score': 34,
              'description': 'Test Description!',
              'summary': 'Test Summary!'
          },
          'bike': {
              'score': 56,
              'description': 'Test Description!'
          },
          'logo_url': 'http://www.test.com',
          'more_info_icon': 'http://www.someurl.com',
          'more_info_link': 'http://www.someurl.com',
          'help_link': 'http://www.someurl.com',
          'ws_link': 'http://www.someurl.com',
          'snapped_lat': None,
          'snapped_lon': None
    }, False, None),
    ({
          'status': None,
          'walkscore': 12,
          'description': 'Test Description!',
          'updated': datetime.datetime.now(),
          'transit': {
              'score': 34,
              'description': 'Test Description!',
              'summary': 'Test Summary!'
          },
          'bike': {
              'score': 56,
              'description': 'Test Description!'
          },
          'logo_url': 'http://www.test.com',
          'more_info_icon': 'http://www.someurl.com',
          'more_info_link': 'http://www.someurl.com',
          'help_link': 'http://www.someurl.com',
          'ws_link': 'http://www.someurl.com',
          'snapped_lat': None,
          'snapped_lon': None
    }, True, None),
])
def test_LocationScore_from_dict(obj, api_compatible, error):
    if not error:
        result = LocationScore.from_dict(obj, api_compatible = api_compatible)
    else:
        with pytest.raises(error):
            result = LocationScore.from_dict(obj, api_compatible = api_compatible)

    if not error:
        assert isinstance(result, LocationScore) is True

        serialized_result = result.to_dict(api_compatible = api_compatible)
        print(serialized_result)

        roundtrip_result = LocationScore.from_dict(serialized_result,
                                                   api_compatible = api_compatible)
        roundtrip_serialization = roundtrip_result.to_dict(api_compatible = api_compatible)

        assert checkers.are_dicts_equivalent(roundtrip_serialization,
                                             serialized_result) is True


@pytest.mark.parametrize('obj, api_compatible, error', [
    (None, False, None),
    (None, True, None),
    ({
          'status': None,
          'walk': {
              'score': None,
              'description': None,
              'updated': None
          },
          'transit': {
              'score': None,
              'description': None,
              'summary': None,
          },
          'bike': {
              'score': None,
              'description': None,
          },
          'logo_url': None,
          'more_info_icon': None,
          'more_info_link': None,
          'help_link': None,
          'property_page_link': None,
          'snapped_coordinates': {
              'latitude': None,
              'longitude': None
          },
          'original_coordinates': {
              'address': None,
              'latitude': None,
              'longitude': None
          }
    }, False, None),
    ({
          'status': None,
          'walk': {
              'score': None,
              'description': None,
              'updated': None
          },
          'transit': {
              'score': None,
              'description': None,
              'summary': None,
          },
          'bike': {
              'score': None,
              'description': None,
          },
          'logo_url': None,
          'more_info_icon': None,
          'more_info_link': None,
          'help_link': None,
          'property_page_link': None,
          'snapped_coordinates': {
              'latitude': None,
              'longitude': None
          },
          'original_coordinates': {
              'address': None,
              'latitude': None,
              'longitude': None
          }
    }, True, None),
    ({
          'status': None,
          'walkscore': 12,
          'description': 'Test Description!',
          'updated': datetime.datetime.now(),
          'transit': {
              'score': 34,
              'description': 'Test Description!',
              'summary': 'Test Summary!'
          },
          'bike': {
              'score': 56,
              'description': 'Test Description!'
          },
          'logo_url': 'http://www.test.com',
          'more_info_icon': 'http://www.someurl.com',
          'more_info_link': 'http://www.someurl.com',
          'help_link': 'http://www.someurl.com',
          'ws_link': 'http://www.someurl.com',
          'snapped_lat': None,
          'snapped_lon': None
    }, False, None),
    ({
          'status': None,
          'walkscore': 12,
          'description': 'Test Description!',
          'updated': datetime.datetime.now(),
          'transit': {
              'score': 34,
              'description': 'Test Description!',
              'summary': 'Test Summary!'
          },
          'bike': {
              'score': 56,
              'description': 'Test Description!'
          },
          'logo_url': 'http://www.test.com',
          'more_info_icon': 'http://www.someurl.com',
          'more_info_link': 'http://www.someurl.com',
          'help_link': 'http://www.someurl.com',
          'ws_link': 'http://www.someurl.com',
          'snapped_lat': None,
          'snapped_lon': None
    }, True, None)
])
def test_LocationScore_from_json(obj, api_compatible, error):
    if obj:
        if obj.get('updated', None) is not None:
            obj['updated'] = obj.get('updated').isoformat()
        elif 'walk' in obj and obj.get('walk',
                                       {}).get('updated', None) is not None:
            obj['walk']['updated'] = obj['walk']['updated'].isoformat()

        obj = json.dumps(obj)

    if not error:
        result = LocationScore.from_json(obj, api_compatible = api_compatible)
    else:
        with pytest.raises(error):
            result = LocationScore.from_json(obj, api_compatible = api_compatible)

    if not error:
        assert isinstance(result, LocationScore) is True

        serialized_result = result.to_dict(api_compatible = api_compatible)

        roundtrip_result = LocationScore.from_json(serialized_result,
                                                   api_compatible = api_compatible)
        roundtrip_serialization = roundtrip_result.to_dict(api_compatible = api_compatible)

        assert checkers.are_dicts_equivalent(roundtrip_serialization,
                                             serialized_result) is True


@pytest.mark.parametrize('arguments, expected_result', [
    (None, "LocationScore(address = 'None', original_latitude = None, original_longitude = None)"),
    ({
         'walk_score': 12,
         'walk_description': 'Test Description!',
         'walk_updated': datetime.datetime.now(),
         'transit_score': 34,
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'http://www.someurl.com',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, "LocationScore(address = '123 Anyplace St, Anywhere, AK 12345', original_latitude = 123.45, original_longitude = 123.45)"),
])
def test_LocationScore__repr__(arguments, expected_result):
    if arguments:
        obj = LocationScore(**arguments)
    else:
        obj = LocationScore()

    result = obj.__repr__()

    assert result == expected_result

@pytest.mark.parametrize('arguments, expected_result', [
    (None, "LocationScore(address = 'None')"),
    ({
         'walk_score': 12,
         'walk_description': 'Test Description!',
         'walk_updated': datetime.datetime.now(),
         'transit_score': 34,
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'http://www.someurl.com',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, "LocationScore(address = '123 Anyplace St, Anywhere, AK 12345')"),
])
def test_LocationScore__str__(arguments, expected_result):
    if arguments:
        obj = LocationScore(**arguments)

    if arguments:
        obj = LocationScore(**arguments)
    else:
        obj = LocationScore()

    result = str(obj)

    assert result == expected_result


@pytest.mark.parametrize('arguments1, arguments2, expected_result', [
    (None, None, True),
    ({
         'walk_score': 12,
         'walk_description': 'Test Description!',
         'walk_updated': datetime.datetime.now(),
         'transit_score': 34,
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'http://www.someurl.com',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, {
         'walk_score': 12,
         'walk_description': 'Test Description!',
         'walk_updated': datetime.datetime.now(),
         'transit_score': 34,
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'http://www.someurl.com',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, True),
    ({
         'walk_score': 12,
         'walk_description': 'Test Description!',
         'walk_updated': datetime.datetime.now(),
         'transit_score': 34,
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'http://www.someurl.com',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, {
         'walk_score': 12,
         'walk_description': 'Different description!!',
         'walk_updated': datetime.datetime.now(),
         'transit_score': 34,
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'http://www.someurl.com',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, False)
])
def test_LocationScore__eq__(arguments1, arguments2, expected_result):
    if arguments1:
        obj1 = LocationScore(**arguments1)
    else:
        obj1 = LocationScore()

    if arguments2:
        obj2 = LocationScore(**arguments2)
    else:
        obj2 = LocationScore()

    result = obj1 == obj2

    assert result is expected_result


@pytest.mark.parametrize('arguments, expected_result', [
    (None, False),
    ({
         'status': 1,
         'walk_description': 'Test Description!',
         'walk_updated': datetime.datetime.now(),
         'transit_score': 34,
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'http://www.someurl.com',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, True),
    ({
         'status': 30,
         'walk_description': 'Test Description!',
         'walk_updated': datetime.datetime.now(),
         'transit_score': 34,
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'http://www.someurl.com',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, False),
    ({
         'status': None,
         'walk_description': 'Test Description!',
         'walk_updated': datetime.datetime.now(),
         'transit_score': 34,
         'transit_description': 'Test Description!',
         'transit_summary': 'Test Summary!',
         'bike_score': 56,
         'bike_description': 'Test Description!',
         'logo_url': 'http://www.test.com',
         'more_info_icon': 'http://www.someurl.com',
         'more_info_link': 'http://www.someurl.com',
         'help_link': 'http://www.someurl.com',
         'property_page_link': 'http://www.someurl.com',
         'address': '123 Anyplace St, Anywhere, AK 12345',
         'original_latitude': 123.45,
         'original_longitude': 123.45
    }, False),
])
def test_LocationScore__bool__(arguments, expected_result):
    if arguments:
        obj = LocationScore(**arguments)

    if arguments:
        obj = LocationScore(**arguments)
    else:
        obj = LocationScore()

    result = bool(obj)

    assert result == expected_result
