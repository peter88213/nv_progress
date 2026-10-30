"""Provide a daily progress log file exporter mixin class.

Copyright (c) 2026 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from nvprogress.csv_progress_log import CsvProgressLog
from nvprogress.nvprogress_locale import _
from nvprogress.wc_log_dict import WcLogDict


class LogExporter:
    LOGFILE_CLASS = CsvProgressLog

    def export_progress_log(self, event=None):
        if self._mdl.prjFile is None:
            return

        if self._mdl.prjFile.filePath is None:
            return

        self._ui.restore_status()

        LogfilePath = (
            f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}'
            f'_{self.LOGFILE_CLASS.SUFFIX}'
            f'{self.LOGFILE_CLASS.EXTENSION}'
        )
        progressLogfile = self.LOGFILE_CLASS(LogfilePath)
        progressLogfile.wcLog = WcLogDict()
        progressLogfile.wcLog.update(self._mdl.prjFile)
        try:
            progressLogfile.write()
        except Exception as ex:
            self._ui.set_status(f'!{str(ex)}')
        else:
            self._ui.set_status(f'{_("File exported")}: {LogfilePath}')

