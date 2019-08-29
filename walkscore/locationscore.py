# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers


class LocationScore(object):
    """Object representation of a location's scoring data returned from the
    WalkScore API."""

    def __init__(self,
                 address = None,
                 original_latitude = None,
                 original_longitude = None,
                 status = None,
                 walk_score = None,
                 walk_description = None,
                 walk_updated = None,
                 transit_score = None,
                 transit_description = None,
                 transit_summary = None,
                 bike_score = None,
                 bike_description = None,
                 bike_summary = None,
                 logo_url = None,
                 more_info_icon = None,
                 more_info_link = None,
                 help_link = None,
                 snapped_latitude = None,
                 snapped_longitude = None,
                 property_page_link = None):
        self._address = None
        self._status = None

        self._walk_score = None
        self._walk_description = None
        self._walk_updated = None
        self._ws_link = None

        self._transit_score = None
        self._transit_description = None
        self._transit_summary = None

        self._bike_score = None
        self._bike_description = None
        self._bike_summary = None

        self._logo_url = None
        self._more_info_icon = None
        self._more_info_link = None
        self._help_link = None

        self._original_latitude = None
        self._original_longitude = None
        self._snapped_latitude = None
        self._snapped_longitude = None

        self._property_page_link = None

        self.status = status
        self.address = address

        self.walk_score = walk_score
        self.walk_description = walk_description
        self.walk_updated = walk_updated

        self.transit_score = transit_score
        self.transit_description = transit_description
        self.transit_summary = transit_summary

        self.bike_score = bike_score
        self.bike_description = bike_description

        self.logo_url = logo_url
        self.more_info_icon = more_info_icon
        self.more_info_link = more_info_link
        self.help_link = help_link

        self.original_latitude = original_latitude
        self.original_longitude = original_longitude
        self.snapped_latitude = snapped_latitude
        self.snapped_longitude = snapped_longitude

        self.property_page_link = property_page_link

    def __repr__(self):
        return ("LocationScore(address = '{}',"
                " original_latitude = {},"
                " original_longitude = {})".format(self.address,
                                                   self.original_latitude,
                                                   self.original_longitude))

    def __str__(self):
        return "LocationScore(address = '{}')".format(self.address)

    def __eq__(self, other):
        if isinstance(other, LocationScore):
            other = other.to_dict(api_compatible = False)

        if isinstance(other, dict):
            dict_form = self.to_dict(api_compatible = False)
            if checkers.are_dicts_equivalent(dict_form, other):
                return True

            dict_form = self.to_dict(api_compatible = True)
            if checkers.are_dicts_equivalent(dict_form, other):
                return True

        return False

    def __bool__(self):
        if not self.status or self.status != 1:
            return False

        return True

    @property
    def status(self):
        """Status Code of the result.

        :rtype: :class:`int <python:int>`
        """
        return self._status

    @status.setter
    def status(self, value):
        self._status = validators.integer(value, allow_empty = True)

    @property
    def address(self):
        """The original address supplied for the :class:`LocationScore`.

        :rtype: :class:`str <python:str>`
        """
        return self._address

    @address.setter
    def address(self, value):
        self._address = validators.string(value, allow_empty = True)

    @property
    def walk_score(self):
        """The :term:`WalkScore` for the location, measuring walkability on a
        scale from 0 to 100.

        :rtype: :class:`int <python:int>`
        """
        return self._walk_score

    @walk_score.setter
    def walk_score(self, value):
        self._walk_score = validators.integer(value,
                                              allow_empty = True,
                                              minimum = 0,
                                              maximum = 100)

    @property
    def walk_description(self):
        """A textual description of the location's walkability.

        :rtype: :class:`str <python:str>`
        """
        return self._walk_description

    @walk_description.setter
    def walk_description(self, value):
        self._walk_description = validators.string(value, allow_empty = True)

    @property
    def walk_updated(self):
        """The timestamp for when the location's :term:`WalkScore` was last
        updated.

        :rtype: :class:`datetime <python:datetime.datetime>`
        """
        return self._walk_updated

    @walk_updated.setter
    def walk_updated(self, value):
        self._walk_updated = validators.datetime(value, allow_empty = True)

    @property
    def property_page_link(self):
        """URL to the walkscore.com score and map for the location.

        :rtype: :class:`str <python:str>`
        """
        return self._property_page_link

    @property_page_link.setter
    def property_page_link(self, value):
        self._property_page_link = validators.url(value, allow_empty = True)

    @property
    def transit_score(self):
        """The :term:`TransitScore` for the location, measuring ease-of-transit
        on a scale from 0 to 100.

        :rtype: :class:`int <python:int>`
        """
        return self._transit_score

    @transit_score.setter
    def transit_score(self, value):
        self._transit_score = validators.integer(value,
                                                 allow_empty = True,
                                                 minimum = 0,
                                                 maximum = 100)

    @property
    def transit_description(self):
        """A textual description of the location's ease-of-transit.

        :rtype: :class:`str <python:str>`
        """
        return self._transit_description

    @transit_description.setter
    def transit_description(self, value):
        self._transit_description = validators.string(value, allow_empty = True)

    @property
    def transit_summary(self):
        """A textual summary of the location's ease-of-transit.

        :rtype: :class:`str <python:str>`
        """
        return self._transit_summary

    @transit_summary.setter
    def transit_summary(self, value):
        self._transit_summary = validators.string(value, allow_empty = True)


    @property
    def bike_score(self):
        """The :term:`TransitScore` for the location, measuring bike-ability
        on a scale from 0 to 100.

        :rtype: :class:`int <python:int>`
        """
        return self._bike_score

    @bike_score.setter
    def bike_score(self, value):
        self._bike_score = validators.integer(value,
                                              allow_empty = True,
                                              minimum = 0,
                                              maximum = 100)

    @property
    def bike_description(self):
        """A textual description of the location's bike-ability.

        :rtype: :class:`str <python:str>`
        """
        return self._bike_description

    @bike_description.setter
    def bike_description(self, value):
        self._bike_description = validators.string(value, allow_empty = True)

    @property
    def logo_url(self):
        """URL to the WalkScore logo.

        :rtype: :class:`str <python:str>`
        """
        return self._logo_url

    @logo_url.setter
    def logo_url(self, value):
        self._logo_url = validators.url(value, allow_empty = True)

    @property
    def more_info_icon(self):
        """URL to the question mark icon to display next to the Score.

        :rtype: :class:`str <python:str>`
        """
        return self._more_info_icon

    @more_info_icon.setter
    def more_info_icon(self, value):
        self._more_info_icon = validators.url(value, allow_empty = True)

    @property
    def more_info_link(self):
        """URL for the question mark displayed next to the Score to link to.

        :rtype: :class:`str <python:str>`
        """
        return self._more_info_link

    @more_info_link.setter
    def more_info_link(self, value):
        self._more_info_link = validators.url(value, allow_empty = True)

    @property
    def help_link(self):
        """URL to the "How WalkScore Works" page.

        :rtype: :class:`str <python:str>`
        """
        return self._help_link

    @help_link.setter
    def help_link(self, value):
        self._help_link = validators.url(value, allow_empty = True)

    @property
    def original_latitude(self):
        """The latitude of the location as originally supplied.

        :rtype: :class:`float <python:float>`
        """
        return self._original_latitude

    @original_latitude.setter
    def original_latitude(self, value):
        self._original_latitude = validators.float(value, allow_empty = True)

    @property
    def original_longitude(self):
        """The longitude of the location as originally supplied.

        :rtype: :class:`float <python:float>`
        """
        return self._original_longitude

    @original_longitude.setter
    def original_longitude(self, value):
        self._original_longitude = validators.float(value, allow_empty = True)

    @property
    def original_coordinates(self):
        """The coordinates of the location as originally supplied.

        :rtype: :class:`tuple <python:tuple>` of longitude and latitude as
          :class:`float <python:float>` values
        """
        return self.original_longitude, self.original_latitude

    @original_coordinates.setter
    def original_coordinates(self, value):
        value = validators.iterable(value,
                                    allow_empty = True,
                                    minimum_length = 2,
                                    maximum_length = 2)
        self.original_longitude = value[0]
        self.original_latitude = value[1]

    @property
    def snapped_latitude(self):
        """The latitude of the location as returned by the API.

        :rtype: :class:`float <python:float>`
        """
        return self._snapped_latitude

    @snapped_latitude.setter
    def snapped_latitude(self, value):
        self._snapped_latitude = validators.float(value, allow_empty = True)

    @property
    def snapped_longitude(self):
        """The longitude of the location as returned by the API.

        :rtype: :class:`float <python:float>`
        """
        return self._snapped_longitude

    @snapped_longitude.setter
    def snapped_longitude(self, value):
        self._snapped_longitude = validators.float(value, allow_empty = True)

    @property
    def snapped_coordinates(self):
        """The coordinates of the location as returned by the API.

        :rtype: :class:`tuple <python:tuple>` of longitude and latitude as
          :class:`float <python:float>` values
        """
        return self.snapped_longitude, self.snapped_latitude

    @snapped_coordinates.setter
    def snapped_coordinates(self, value):
        value = validators.iterable(value,
                                    allow_empty = True,
                                    minimum_length = 2,
                                    maximum_length = 2)
        self.snapped_longitude = value[0]
        self.snapped_latitude = value[1]

    def to_dict(self, api_compatible = False):
        """Serialize the :class:`LocationScore` to a :class:`dict <python:dict>`.

        :param api_compatible: If ``True``, returns a :class:`dict <python:dict>`
          whose structure is compatible with the JSON object returned by the
          WalkScore API. If ``False``, returns a slightly more normalized
          :class:`dict <python:dict>` representation. Defaults to ``False``.
        :type api_compatible: :class:`bool <python:bool>`

        :returns: :class:`dict <python:dict>` representation of the object
        :rtype: :class:`dict <python:dict>`
        """

        if not api_compatible:
            result = {
                'status': self.status,
                'walk': {
                    'score': self.walk_score,
                    'description': self.walk_description,
                    'updated': self.walk_updated,
                },
                'transit': {
                    'score': self.transit_score,
                    'description': self.transit_description,
                    'summary': self.transit_summary
                },
                'bike': {
                    'score': self.bike_score,
                    'description': self.bike_description
                },
                'original_coordinates': {
                    'longitude': self.original_longitude,
                    'latitude': self.original_latitude,
                    'address': self.address
                },
                'snapped_coordinates': {
                    'longitude': self.snapped_longitude,
                    'latitude': self.snapped_latitude
                },
                'logo_url': self.logo_url,
                'more_info_icon': self.more_info_icon,
                'more_info_link': self.more_info_link,
                'help_link': self.help_link,
                'property_page_link': self.property_page_link
            }
        else:
            result = {
                'status': self.status,
                'walkscore': self.walk_score,
                'description': self.walk_description,
                'updated': self.walk_updated,
                'transit': {
                    'score': self.transit_score,
                    'description': self.transit_description,
                    'summary': self.transit_summary
                },
                'bike': {
                    'score': self.bike_score,
                    'description': self.bike_description
                },
                'snapped_lat': self.snapped_latitude,
                'snapped_lon': self.snapped_longitude,
                'logo_url': self.logo_url,
                'more_info_icon': self.more_info_icon,
                'more_info_link': self.more_info_link,
                'help_link': self.help_link,
                'ws_link': self.property_page_link
            }

        return result

    def to_json(self, api_compatible = False):
        """Serialize the :class:`LocationScore` to a :term:`JSON` string.

        :param api_compatible: If ``True``, returns a JSON object whose structure
          is compatible with the JSON object returned by the
          WalkScore API. If ``False``, returns a slightly more normalized
          structure. Defaults to ``False``.
        :type api_compatible: :class:`bool <python:bool>`

        :returns: :class:`str <python:str>` representation of a JSON object
        :rtype: :class:`str <python:str>`

        """
        interim = self.to_dict(api_compatible = api_compatible)
        if api_compatible and interim['updated'] is not None:
            interim['updated'] = interim['updated'].isoformat()
        elif not api_compatible:
            interim['walk']['updated'] = interim['walk']['updated'].isoformat()

        result = json.dumps(interim)

        return result

    @classmethod
    def from_dict(cls, obj, api_compatible = False):
        """Create a :class:`LocationScore` instance from a
        :class:`dict <python:dict>` representation.

        :param obj: The :class:`dict <python:dict>` representation of the location
          score.
        :type obj: :class:`dict <python:dict>`

        :param api_compatible: If ``True``, expects ``obj`` to be a
          :class:`dict <python:dict>` whose structure is compatible with the
          JSON object returned by the WalkScore API. If ``False``, expects a
          slightly more normalized :class:`dict <python:dict>` representation.
          Defaults to ``False``.
        :type api_compatible: :class:`bool <python:bool>`

        :returns: :class:`LocationScore` representation of ``obj``.
        :rtype: :class:`LocationScore`
        """
        obj = validators.dict(obj, allow_empty = True)

        result = cls()

        if obj and not api_compatible:
            result.address = obj.get('original_coordinates',
                                     {}).get('address', None)
            result.original_latitude = obj.get('original_coordinates',
                                               {}).get('latitude')
            result.original_longitude = obj.get('original_coordinates',
                                                {}).get('longitude')
            result.snapped_latitude = obj.get('snapped_coordinates',
                                               {}).get('latitude')
            result.snapped_longitude = obj.get('snapped_coordinates',
                                                {}).get('longitude')

            result.walk_score = obj.get('walk', {}).get('score', None)
            result.walk_description = obj.get('walk', {}).get('description', None)
            result.walk_updated = obj.get('walk', {}).get('updated', None)

            result.property_page_link = obj.get('property_page_link', None)

        elif obj:
            result.walk_score = obj.get('walkscore', None)
            result.walk_description = obj.get('description', None)
            result.walk_updated = obj.get('updated', None)

            result.snapped_latitude = obj.get('snapped_lat', None)
            result.snapped_longitude = obj.get('snapped_lon', None)

            result.property_page_link = obj.get('ws_link', None)

        if obj:
            result.status = obj.get('status', None)

            result.transit_score = obj.get('transit', {}).get('score', None)
            result.transit_description = obj.get('transit',
                                                 {}).get('description', None)
            result.transit_summary = obj.get('transit', {}).get('summary', None)

            result.bike_score = obj.get('bike', {}).get('score', None)
            result.bike_description = obj.get('bike', {}).get('description', None)

            result.logo_url = obj.get('logo_url', None)
            result.more_info_icon = obj.get('more_info_icon', None)
            result.more_info_link = obj.get('more_info_link', None)
            result.help_link = obj.get('help_link', None)

        return result

    @classmethod
    def from_json(cls, obj, api_compatible = False):
        """Create a :class:`LocationScore` instance from a JSON representation.

        :param obj: The JSON representation of the location score.
        :type obj: :class:`str <python:str>` or :class:`bytes <python:bytes>`

        :param api_compatible: If ``True``, expects ``obj`` to be a JSON object
          whose structure is compatible with the JSON object returned by the
          WalkScore API. If ``False``, expects a slightly more normalized
          representation. Defaults to ``False``.
        :type api_compatible: :class:`bool <python:bool>`

        :returns: :class:`LocationScore` representation of ``obj``.
        :rtype: :class:`LocationScore`
        """
        obj = validators.json(obj,
                              allow_empty = True)

        return cls.from_dict(obj, api_compatible = api_compatible)
