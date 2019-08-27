.. WalkScore API documentation master file, created by
   sphinx-quickstart on Tue Aug 27 13:46:37 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

####################################################
WalkScore API
####################################################

**(Unofficial) Python Bindings for the WalkScore API**

.. |strong| raw:: html

<strong>

.. |/strong| raw:: html

</strong>

.. sidebar:: Version Compatability

 **WalkScore** is designed to be compatible with:

   * Python 3.7 or higher

.. include:: _unit_tests_code_coverage.rst

.. toctree::
:hidden:
:maxdepth: 3
:caption: Contents:

Home <self>
Quickstart: Patterns and Best Practices <quickstart>
Using WalkScore <using>
API Reference <api>
Error Reference <errors>
Contributor Guide <contributing>
Testing Reference <testing>
Release History <history>
Glossary <glossary>
License <license>

**WalkScore** is a Python library that provides Python bindings for the
`WalkScore API <https://www.walkscore.com/>`_. It enables you to retrieve
WalkScores, TransitScores, and BikeScores from the API within your Python code.

.. contents::
 :depth: 3
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

* Python representation of WalkScores, TransitScores, and BikeScores.
* Easy serialization and deserialization of API responses to Python objects,
  :class:`dict <python:dict>` objects or JSON
* Built-in back-off/retry logic if the WalkScore API is unstable at any mometn in time
* Robust error handling to surface meaningful information to help you debug your
  code.

------------------

********************************
Hello, World and Basic Usage
********************************

1. Import the WalkScore API
===============================

.. code-block:: python

  from walkscore import ScoreAPI, WalkScore, TransitScore, BikeScore

2. Initialize the API
============================

You can either use a single object to communicate with all of the available
WalkScore APIs, or initialize a single object for each API:

.. code-block:: python

  api_key = 'YOUR API KEY GOES HERE'

  score_api = ScoreAPI(api_key = api_key)

  walkscore = WalkScore(api_key = api_key)
  transitscore = TransitScore(api_key = api_key)
  bikescore = BikeScore(api_key = api_key)

3. Retrieve a Score
=============================

.. code-block:: python

  address = '123 Anyplace St Anywhere, AK 12345'

  all_results = score_api.get(address)
  walk_score_result = score_api.walk(address)
  transit_score_result = score_api.transit(address)
  bike_score_result = score_api.bike(address)

  walk_result = walkscore.get(address)
  transit_result = transitscore.get(address)
  bike_result = bikescore.get(address)

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
