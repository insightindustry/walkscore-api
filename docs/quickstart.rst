******************************************
Quickstart: Patterns and Best Practices
******************************************

.. contents::
  :local:
  :depth: 3
  :backlinks: entry

----------

Installation
===============

.. include:: _installation.rst

-----------

Initializing the API
=======================

To initialize the :class:`WalkScoreAPI <walkscore.WalkScoreAPI>` object all you
need to do is instantiate it:

.. code-block:: python

  from walkscore import WalkScoreAPI

  # supplying an API key
  walkscore = WalkScoreAPI(api_key = 'MY API KEY GOES HERE')

  # using an API key in the "WALKSCORE_API_KEY" environment variables
  walkscore = WalkScoreAPI()

--------------

Configuring the HTTP Client
==============================

You can heavily customize the HTTP client used by the WalkScore Library. By
default, the library will look for HTTP libraries in the following order:

* `urlfetch <https://pypi.org/project/urlfetch/>`_
* `requests <https://pypi.org/project/requests/2.7.0/>`_
* `pycurl <http://pycurl.io/>`_
* :doc:`urllib <python:urllib>` (Python standard library)

.. tip::

  You can also override the HTTP client by subclassing the
  :class:`HTTPClient <walkscore.http_client.HTTPClient>` class.

There are three ways to customize / configure the HTTP client:

#. Subclass the :class:`HTTP Client <walkscore.http_client.HTTPClient>` class.
#. Supply a proxy URL.
#. Configure the maximum number of retries.

Subclassing the Client
************************

.. code-block:: python

  from walkscore import WalkScoreAPI

  from my_custom_client import MyCustomHTTPClient

  walkscore = WalkScoreAPI(http_client = MyCustomHTTPClient)


Configuring a Proxy
***********************

.. code-block:: python

  from walkscore import WalkScoreAPI

  walkscore = WalkScoreAPI(proxy = 'http://www.some-proxy-url')

Configuring the Maximum Number of Retries
*********************************************

If the WalkScore Library is unable to get a response from the WalkScore API, it
will automatically apply an exponential backoff/retry strategy. However, you can
configure the maximum number of retries that it attempts. This can be configured
in two ways:

#. By setting the ``BACKOFF_DEFAULT_TRIES`` environment variable.
#. By passing the maximum number of retries in the ``max_retries`` argument:

    .. code-block:: python

      from walkscore import WalkScoreAPI

      walkscore = WalkScoreAPI(max_retries = 5)

----------------------

Getting Scores
=======================

To retrieve scores, all you need to do is to call the
:func:`get_score() <walkscore.WalkScoreAPI.get_score>` method on the initialized API:

.. code-block:: python

  from walkscore import WalkScoreAPI

  walkscore = WalkScoreAPI(api_key = 'MY API KEY GOES HERE')

  result = walkscore.get_score(latitude = 123.45, longitude = 54.321)

.. note::

  In order to retrieve a score from the API, you *must* supply the latitude and
  longitude of the point you are looking for. The WalkScore API does *not* support
  geocoding based on addresses, although an address can provide more precise
  results if you supply it as well.

.. tip::

  In order to get better performance out of the underlying WalkScore API, you may
  want to suppress the calculation / retrieval of
  :term:`TransitScores <TransitScore>` and/or :term:`BikeScores <BikeScore>` if
  you don't need them. To do that, all you need to do is pass the appropriate
  arguments into the :func:`get_score() <walkscore.WalkScoreAPI.get_score>` method:

  .. code-block:: python

    result = walkscore.get_score(latitude = 123.45,
                                 longitude = 54.321,
                                 return_transit_score = False,
                                 return_bike_score = False)

The results returned by the :func:`get_score() <walkscore.WalkScoreAPI.get_score>` method
are always :class:`LocationScore <walkscore.LocationScore>` instances.

----------------------

Working with Scores
=========================

When the WalkScore Library has retrieved a score for a given set of coordinates,
you can work with it as any other Python object. See the :class:`LocationScore`
reference documentation for more insight into its properties.

However, there are a number of key serialization / deserialization methods that
you may find useful:

* :func:`.to_json() <walkscore.LocationScore.to_json>` which returns a JSON representation
  of the location score, either normalized to a cleaner/more consistent structure
  preferred by the WalkScore Library or mirroring the WalkScore API's JSON
  structure
* :func:`.from_json() <walkscore.LocationScore.from_json>` which returns a
  :class:`LocationScore` instance generated from a JSON string
* :func:`.to_dict() <walkscore.LocationScore.to_dict>` which returns a
  :class:`dict <python:dict>` representation fo the location score, either
  normalized to a cleaner/more consistent structure preferred by the WalkScore
  Library or mirroring the WalkScore API's JSON structure
* :func:`.from_dict() <walkscore.LocationScore.from_dict>` which returns a
  :class:`LocationScore <walkscore.LocationScore>` instance generated from a
  :class:`dict <python:dict>`

------------------------
