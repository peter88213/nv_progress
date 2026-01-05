"""A daily progress log viewer plugin for novelibre.

Requires Python 3.7+
Copyright (c) 2025 Peter Triesberger
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

from nvprogress.nvprogress_locale import _
from nvlib.controller.plugin.plugin_base import PluginBase
from nvprogress.progress_service import ProgressService


class Plugin(PluginBase):
    """novelibre daily progress log viewer plugin class."""
    VERSION = '@release'
    API_VERSION = '5.44'
    DESCRIPTION = 'A daily progress log viewer'
    URL = 'https://github.com/peter88213/nv_progress'
    HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_progress'

    FEATURE = _('Daily progress log')

    def install(self, model, view, controller):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller.

        Extends the superclass method.
        """
        super().install(model, view, controller)
        self.progressService = ProgressService(model, view)
        self._icon = self._get_icon('progress.png')

        #--- Configure the main menu.

        # Create an entry in the Tools menu.
        label = self.FEATURE
        self._ui.toolsMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            command=self.start_viewer,
            state='disabled',
        )
        self._ui.toolsMenu.disableOnClose.append(label)

        # Add an entry to the Help menu.
        label = _('Progress viewer Online help')
        self._ui.helpMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            command=self.open_help,
        )

    def on_close(self):
        self.progressService.on_close()

    def on_open(self):
        self.progressService.on_open()

    def on_quit(self):
        self.progressService.on_quit()

    def open_help(self, event=None):
        webbrowser.open(self.HELP_URL)

    def start_viewer(self):
        self.progressService.start_viewer(self.FEATURE)

