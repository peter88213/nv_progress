"""Provide platform specific settings for the nv_progress plugin.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_progress
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import platform

from nvprogresslib.platform.generic_keys import GenericKeys
from nvprogresslib.platform.mac_keys import MacKeys
from nvprogresslib.platform.windows_keys import WindowsKeys

if platform.system() == 'Windows':
    PLATFORM = 'win'
    KEYS = WindowsKeys()
elif platform.system() in ('Linux', 'FreeBSD'):
    PLATFORM = 'ix'
    KEYS = GenericKeys()
elif platform.system() == 'Darwin':
    PLATFORM = 'mac'
    KEYS = MacKeys()
else:
    PLATFORM = ''
    KEYS = GenericKeys()

