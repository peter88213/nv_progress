"""Provide a class for CSV progress file representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import csv

from nvlib.model.file.file import File
from nvprogress.nvprogress_locale import _


class CsvProgressLog(File):

    DESCRIPTION = _('Daily progress log file')
    EXTENSION = '.csv'
    SUFFIX = 'log'

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath, **kwargs)
        self.wcLog = None

    def write(self):
        with open(self.filePath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerow(
                [_('Date'), _('Words total'), _('With unused')]
            )
            for date in self.wcLog:
                writer.writerow(
                    [date, self.wcLog[date][0], self.wcLog[date][1]]
                )

