.. WalkScore API documentation master file, created by
   sphinx-quickstart on Tue Aug 27 13:46:37 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

####################################################
The WalkScore Library
####################################################

**(Unofficial) Python Bindings for the WalkScore API**

.. sidebar:: Version Compatability

 The **WalkScore Library** is designed to be compatible with:

   * Python 3.6 or higher

.. include:: _unit_tests_code_coverage.rst

.. toctree::
  :hidden:
  :maxdepth: 3
  :caption: Contents:

  Home <self>
  Quickstart: Patterns and Best Practices <quickstart>
  API Reference <api>
  Error Reference <errors>
  Contributor Guide <contributing>
  Testing Reference <testing>
  Release History <history>
  Glossary <glossary>
  License <license>

The **WalkScore Library** is a Python library that provides Python bindings for the
`WalkScore API <https://www.walkscore.com/>`_. It enables you to retrieve
:term:`WalkScores <WalkScore>`, :term:`TransitScores <TransitScore>`, and
:term:`BikeScores <BikeScore>` from the API within your Python code.

.. warning::

  The **WalkScore Library** is completely unaffiliated with
  `WalkScore <http://www.walkscore.com>`_. It is entirely unofficial and was
  developed based on publicly available documentation of the WalkScore APIs
  published to the WalkScore website. Use of WalkScore is subject to WalkScore's
  licenses and terms of service, and this library is not endorsed by WalkScore
  or any affiliates thereof.

.. contents::
 :depth: 2
 :backlinks: entry

-----------------

***************
Installation
***************

.. include:: _installation.rst

Dependencies
==============

.. include:: _dependencies.rst

-------------

Key WalkScore Features
========================

* Python representation of :term:`WalkScores <WalkScore>`,
  :term:`TransitScores <TransitScore>`, and :term:`BikeScores <BikeScore>`
* Easy serialization and deserialization of API responses to Python objects,
  :class:`dict <python:dict>` objects or :term:`JSON`
* Built-in back-off/retry logic if the WalkScore API is unstable at any moment
  in time
* Robust error handling to surface meaningful information to help you debug your
  code.

------------------

********************************
Hello, World and Basic Usage
********************************

1. Import the WalkScore API
===============================

.. code-block:: python

  from walkscore import WalkScoreAPI

2. Initialize the API
============================

You can either use a single object to communicate with all of the available
WalkScore APIs, or initialize a single object for each API:

.. code-block:: python

  api_key = 'YOUR API KEY GOES HERE'

  score_api = WalkScoreAPI(api_key = api_key)

3. Retrieve a Score
=============================

.. code-block:: python

  address = '123 Anyplace St Anywhere, AK 12345'

  result = score_api.get_score(longitude = 123.45, latitude = 54.321, address = address)

  # the WalkScore for the location
  result.walk_score

  # the TransitScore for the location
  result.transit_score

  # the BikeScore for the location
  result.bike_score

--------------

*********************
Questions and Issues
*********************

You can ask questions and report issues on the project's
`Github Issues Page <https://github.com/insightindustry/walkscore-api/issues>`_

-----------------

*********************
Contributing
*********************

We welcome contributions and pull requests! For more information, please see the
:doc:`Contributor Guide <contributing>`

-------------------

*********************
Testing
*********************

We use `TravisCI <http://travisci.org>`_ for our build automation and
`ReadTheDocs <https://readthedocs.org>`_ for our documentation.

Detailed information about our test suite and how to run tests locally can be
found in our :doc:`Testing Reference <testing>`.

--------------------

**********************
License
**********************

**WalkScore** is made available under an :doc:`MIT License <license>`.

----------------

********************
Indices and tables
********************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
