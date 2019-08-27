# -*- coding: utf-8 -*-
"""(Unofficial) Python bindings for the WalkScore API.

While this entry point to the library exposes all classes and functions for
convenience, those items themselves are actually implemented and documented in
child modules.

"""

import os

# Get the version number from the _version.py file
version_dict = {}
with open(os.path.join(os.path.dirname(__file__), '__version__.py')) as version_file:
    exec(version_file.read(), version_dict)                                     # pylint: disable=W0122

__version__ = version_dict.get('__version__')

from walkscore.api import WalkScoreAPI
from walkscore.locationscore import LocationScore

__all__ = [
    'WalkScoreAPI',
    'LocationScore',
]
