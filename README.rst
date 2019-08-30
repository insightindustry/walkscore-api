####################################################
WalkScore API
####################################################

**(Unofficial) Python Bindings for the WalkScore API**

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Branch
     - Unit Tests
   * - `latest <https://github.com/insightindustry/walkscore-api/tree/master>`_
     -
       .. image:: https://travis-ci.org/insightindustry/walkscore-api.svg?branch=master
         :target: https://travis-ci.org/insightindustry/walkscore
         :alt: Build Status (Travis CI)

       .. image:: https://codecov.io/gh/insightindustry/walkscore-api/branch/master/graph/badge.svg
         :target: https://codecov.io/gh/insightindustry/walkscore
         :alt: Code Coverage Status (Codecov)

       .. image:: https://readthedocs.org/projects/walkscore-api/badge/?version=latest
         :target: http://walkscore-api.readthedocs.io/en/latest/?badge=latest
         :alt: Documentation Status (ReadTheDocs)

   * - `v.1.0 <https://github.com/insightindustry/walkscore-api/tree/v.1.0.0>`_
     -
       .. image:: https://travis-ci.org/insightindustry/walkscore-api.svg?branch=v.1.0.0
         :target: https://travis-ci.org/insightindustry/walkscore
         :alt: Build Status (Travis CI)

       .. image:: https://codecov.io/gh/insightindustry/walkscore-api/branch/v.1.0.0/graph/badge.svg
         :target: https://codecov.io/gh/insightindustry/walkscore
         :alt: Code Coverage Status (Codecov)

       .. image:: https://readthedocs.org/projects/walkscore-api/badge/?version=v.1.0.0
         :target: http://walkscore-api.readthedocs.io/en/latest/?badge=v.1.0.0
         :alt: Documentation Status (ReadTheDocs)


   * - `develop <https://github.com/insightindustry/walkscore-api/tree/develop>`_
     -
       .. image:: https://travis-ci.org/insightindustry/walkscore-api.svg?branch=develop
         :target: https://travis-ci.org/insightindustry/walkscore
         :alt: Build Status (Travis CI)

       .. image:: https://codecov.io/gh/insightindustry/walkscore-api/branch/develop/graph/badge.svg
         :target: https://codecov.io/gh/insightindustry/walkscore
         :alt: Code Coverage Status (Codecov)

       .. image:: https://readthedocs.org/projects/walkscore-api/badge/?version=develop
         :target: http://walkscore-api.readthedocs.io/en/latest/?badge=develop
         :alt: Documentation Status (ReadTheDocs)

The **WalkScore Library** is a Python library that provides Python bindings for the
`WalkScore API <https://www.walkscore.com/>`_. It enables you to retrieve
WalkScores, TransitScores, and BikeScores from the API within your Python code
in Python versions 3.6 and higher.

.. warning::

  The **WalkScore Library** is completely unaffiliated with
  `WalkScore <http://www.walkscore.com>`_. It is entirely unofficial and was
  developed based on publicly available documentation of the WalkScore APIs
  published to the WalkScore website. Use of WalkScore is subject to WalkScore's
  licenses and terms of service, and this library is not endorsed by WalkScore
  or any affiliates thereof.

**COMPLETE DOCUMENTATION:** http://walkscore-api.readthedocs.org/en/latest/index.html

.. contents::
 :depth: 3
 :backlinks: entry

-----------------

***************
Installation
***************

To install the **WalkScore Library**, just execute:

.. code:: bash

 $ pip install walkscore-api


Dependencies
==============

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Python 3.x
   * - | * `Validator-Collection v1.3 <https://github.com/insightindustry/validator-collection>`_ or higher
       | * `Backoff-Utils v.1.0 <https://github.com/insightindustry/backoff-utils>`_ or higher

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

  from walkscore import WalkScoreAPI

2. Initialize the API
============================

You can either use a single object to communicate with all of the available
WalkScore APIs, or initialize a single object for each API:

.. code-block:: python

  api_key = 'YOUR API KEY GOES HERE'

  walkscore_api = WalkScoreAPI(api_key = api_key)

3. Retrieve a Score
=============================

.. code-block:: python

  address = '123 Anyplace St Anywhere, AK 12345'

  result = walkscore_api.get_score(latitude = 123.45, longitude = 54.321, address = address)

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
