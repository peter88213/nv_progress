"""Provide a word count log dictionary.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date


class WcLogDict(dict):
    # key: str -- date (iso formatted)
    # value: list -- [word count: int, with unused: int]

    def update(self, prjFile):
        self.clear()

        # Copy the read-in word count log.
        lastTotals = None
        for wcDate in prjFile.wcLog:
            totals = prjFile.wcLog[wcDate]
            if totals != lastTotals:
                self[wcDate] = totals
                lastTotals = totals

        # Add the word count determined when opening the project.
        for wcDate in prjFile.wcLogUpdate:
            totals = prjFile.wcLogUpdate[wcDate]
            if totals != lastTotals:
                self[wcDate] = totals
                lastTotals = totals

        # Add the actual word count.
        totals = list(prjFile.count_words())
        if totals != lastTotals:
            today = date.today().isoformat()
            self[today] = totals
