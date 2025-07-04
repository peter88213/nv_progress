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
import webbrowser

from nvlib.controller.plugin.plugin_base import PluginBase
from nvprogress.nvprogress_locale import _
from nvprogress.progress_service import ProgressService


class Plugin(PluginBase):
    """novelibre daily progress log viewer plugin class."""
    VERSION = '@release'
    API_VERSION = '5.0'
    DESCRIPTION = 'A daily progress log viewer'
    URL = 'https://github.com/peter88213/nv_progress'
    HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_progress'

    FEATURE = _('Daily progress log')

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

    def install(self, model, view, controller):
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
        self.progressService = ProgressService(model, view, controller)

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Progress viewer Online help'), command=self.open_help)

        # Create an entry in the Tools menu.
        self._ui.toolsMenu.add_command(label=self.FEATURE, command=self.start_viewer)
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')

    def on_close(self):
        """Close the window.
        
        Overrides the superclass method.
        """
        self.progressService.on_close()

    def on_quit(self):
        """Write back the configuration file.
        
        Overrides the superclass method.
        """
        self.progressService.on_quit()

    def open_help(self, event=None):
        webbrowser.open(self.HELP_URL)

    def start_viewer(self):
        self.progressService.start_viewer(self.FEATURE)

