"""Provide a base class for progress file representation.

Copyright (c) 2026 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC

from nvlib.model.file.file import File
from nvprogress.nvprogress_locale import _


class ProgressLog(File, ABC):

    DESCRIPTION = _('Daily progress log file')
    SUFFIX = 'log'

    def __init__(self, filePath, **kwargs):
        File.__init__(self, filePath, **kwargs)
        self.wcLog = None

