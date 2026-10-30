"""Provide a class for JSON progress file representation.

Copyright (c) 2026 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import json

from nvprogress.progress_log import ProgressLog


class JsonProgressLog(ProgressLog):

    EXTENSION = '.json'

    def write(self):
        with open(self.filePath, 'w', encoding='utf-8') as f:
            json.dump(
                [(d, self.wcLog[d][0], self.wcLog[d][1]) for d in self.wcLog],
                f,
                indent=4,
            )

