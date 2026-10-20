"""Provide a class for CSV progress file representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.file.file import File
from nvprogress.nvprogress_locale import _


class CsvProgressLog(File):

    DESCRIPTION = _('Daily progress log file')
    EXTENSION = 'csv'
    SUFFIX = 'log'

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath, **kwargs)
        self.wcLog = None

    def write(self):
        print(self.wcLog)

