"""A daily progress log viewer plugin for novelibre.

Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_progress
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from pathlib import Path

from apptk.view.set_icon_tk import set_icon
from nvlib.plugin.plugin_base import PluginBase
from nvprogresslib.nvprogress_globals import _
from nvprogresslib.nvprogress_globals import open_help
from nvprogresslib.progress_viewer import ProgressViewer


class Plugin(PluginBase):
    """novelibre daily progress log viewer plugin class."""
    VERSION = '@release'
    API_VERSION = '4.3'
    DESCRIPTION = 'A daily progress log viewer'
    URL = 'https://github.com/peter88213/nv_progress'

    FEATURE = _('Daily progress log')
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
    OPTIONS = {}

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='normal')

    def install(self, model, view, controller, prefs=None):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Optional arguments:
            prefs -- deprecated. Please use controller.get_preferences() instead.
        
        Extends the superclass method.
        """
        super().install(model, view, controller)
        self._progress_viewer = None

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/{self.INI_FILENAME}'
        self.configuration = self._mdl.nvService.make_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        self.kwargs.update(self.configuration.options)

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Progress viewer Online help'), command=open_help)

        # Create an entry in the Tools menu.
        self._ui.toolsMenu.add_command(label=self.FEATURE, command=self._start_viewer)
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')

    def on_close(self):
        """Close the window.
        
        Overrides the superclass method.
        """
        self.on_quit()

    def on_quit(self):
        """Write back the configuration file.
        
        Overrides the superclass method.
        """
        if self._progress_viewer:
            if self._progress_viewer.isOpen:
                self._progress_viewer.on_quit()

        #--- Save configuration
        for keyword in self.kwargs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.kwargs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.kwargs[keyword]
        self.configuration.write(self.iniFile)

    def _start_viewer(self):
        if self._progress_viewer:
            if self._progress_viewer.isOpen:
                if self._progress_viewer.state() == 'iconic':
                    self._progress_viewer.state('normal')
                self._progress_viewer.lift()
                self._progress_viewer.focus()
                self._progress_viewer.refresh()
                return

        self._progress_viewer = ProgressViewer(self._mdl, self._ui, self._ctrl, self)
        self._progress_viewer.title(f'{self._mdl.novel.title} - {self.FEATURE}')
        set_icon(self._progress_viewer, icon='wLogo32', default=False)

