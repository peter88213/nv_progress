"""Provide a service class for the progress viewer.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_progress
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path

from nvlib.controller.sub_controller import SubController
from nvlib.gui.set_icon_tk import set_icon
from nvprogress.nvprogress_locale import _
from nvprogress.progress_view import ProgressView


class ProgressService(SubController):
    INI_FILENAME = 'progress.ini'
    INI_FILEPATH = '.novx/config'
    SETTINGS = dict(
        window_geometry='510x440',
        date_width=100,
        wordcount_width=100,
        wordcount_delta_width=100,
        totalcount_width=100,
        totalcount_delta_width=100,
    )
    OPTIONS = dict(
        force_logging=True,
    )

    def __init__(self, model, view):
        self._mdl = model
        self._ui = view
        self.progressView = None

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            configDir = '.'
        self.configuration = self._mdl.nvService.new_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS,
            filePath=f'{configDir}/{self.INI_FILENAME}',
        )
        self.configuration.read()
        self._prefs = {}
        self._prefs.update(self.configuration.settings)
        self._prefs.update(self.configuration.options)

    def on_close(self):
        """Close the window.
        
        Overrides the superclass method.
        """
        self.on_quit()

    def on_open(self):
        """Actions to be performed after a project is opened.
        
        Make sure the project's word count logging is activated.
        
        Overrides the superclass method.        
        """
        if self._prefs['force_logging'] and not self._mdl.novel.saveWordCount:
            self._mdl.novel.saveWordCount = True
            self._ui.set_status(f"#{_('Word count logging is enabled')}.")

    def on_quit(self):
        """Write back the configuration file.
        
        Overrides the superclass method.
        """
        if self.progressView is not None:
            if self.progressView.isOpen:
                self.progressView.on_quit()

        #--- Save configuration
        for keyword in self._prefs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self._prefs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self._prefs[keyword]
        self.configuration.write()

    def start_viewer(self, windowTitle):
        if self.progressView:
            if self.progressView.isOpen:
                if self.progressView.state() == 'iconic':
                    self.progressView.state('normal')
                self.progressView.lift()
                self.progressView.focus()
                return

        self.progressView = ProgressView(
            self._mdl,
            self._prefs,
        )
        self.progressView.title(
            f'{self._mdl.novel.title} - {windowTitle}'
        )
        set_icon(self.progressView, icon='progress', default=False)

