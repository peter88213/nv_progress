"""Provide a class for CSV progress file representation.

Copyright (c) 2026 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import csv

from nvprogress.nvprogress_locale import _
from nvprogress.progress_log import ProgressLog


class CsvProgressLog(ProgressLog):

    EXTENSION = '.csv'

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

