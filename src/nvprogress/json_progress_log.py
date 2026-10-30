"""Provide a class for JSON progress file representation.

Copyright (c) 2025-2026 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import json

from nvlib.model.file.file import File
from nvprogress.nvprogress_locale import _


class JsonProgressLog(File):

    DESCRIPTION = _('Daily progress log file')
    EXTENSION = '.json'
    SUFFIX = 'log'

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath, **kwargs)
        self.wcLog = None

    def write(self):
        with open(self.filePath, 'w', encoding='utf-8') as f:
            json.dump(
                [(d, self.wcLog[d][0], self.wcLog[d][1]) for d in self.wcLog],
                f,
                indent=4,
            )

