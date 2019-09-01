**********************************
Error Reference
**********************************

.. module:: walkscore.errors

.. contents::
  :local:
  :depth: 3
  :backlinks: entry

----------

Handling Errors
=================

Stack Traces
--------------

Because **WalkScore** produces exceptions which inherit from the standard
library, it leverages the same API for handling stack trace information.
This means that it will be handled just like a normal exception in unit test
frameworks, logging solutions, and other tools that might need that information.


WalkScore Errors
===================

WalkScoreError (from :class:`ValueError <python:ValueError>`)
--------------------------------------------------------------------

.. autoclass:: WalkScoreError

----------------

AuthenticationError (from :class:`WalkScoreError`)
--------------------------------------------------------------------

.. autoclass:: AuthenticationError

----------------

InternalAPIError (from :class:`WalkScoreError`)
--------------------------------------------------------------------

.. autoclass:: InternalAPIError

----------------

BlockedIPError (from :class:`WalkScoreError`)
--------------------------------------------------------------------

.. autoclass:: BlockedIPError

----------------

QuotaError (from :class:`WalkScoreError`)
--------------------------------------------------------------------

.. autoclass:: QuotaError

----------------

ScoreInProgressError (from :class:`WalkScoreError`)
--------------------------------------------------------------------

.. autoclass:: ScoreInProgressError

----------------

InvalidCoordinatesError (from :class:`WalkScoreError`)
--------------------------------------------------------------------

.. autoclass:: InvalidCoordinatesError

----------------

BindingError (from :class:`WalkScoreError`)
--------------------------------------------------------------------

.. autoclass:: BindingError

----------------

HTTPConnectionError (from :class:`WalkScoreError`)
--------------------------------------------------------------------

.. autoclass:: HTTPConnectionError

----------------

HTTPTimeoutError (from :class:`HTTPConnectionError`)
--------------------------------------------------------------------

.. autoclass:: HTTPTimeoutError

----------------

SSLError (from :class:`WalkScoreError`)
--------------------------------------------------------------------

.. autoclass:: SSLError
