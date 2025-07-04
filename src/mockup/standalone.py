"""A test application for the nv_progress plugin.

For further information see https://github.com/peter88213/nv_progress
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from novxlib.config.configuration import Configuration
from novxlib.ui.main_tk import MainTk
from nv_progress import Plugin
from nvlib.model.nv_work_file import NvWorkFile
from nvprogresslib.nvprogress_globals import _
import tkinter as tk

APPLICATION = 'View daily progress log'


class NvServiceMock:

    def make_configuration(self, **kwargs):
        return Configuration(**kwargs)


class ProgressTk(MainTk):

    def __init__(self):
        kwargs = {
                'root_geometry': '800x500',
                'last_open': '',
                }
        super().__init__(APPLICATION, **kwargs)
        self.nvService = NvServiceMock()
        self._YW_CLASS = NvWorkFile
        self.toolsMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Tools'), menu=self.toolsMenu)
        self.helpMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Help'), menu=self.helpMenu)
        self.plugin = Plugin()
        self.plugin.install(self, self, self)

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        super().disable_menu()
        self.plugin.disable_menu()

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        super().enable_menu()
        self.plugin.enable_menu()


if __name__ == '__main__':
    ui = ProgressTk()
    ui.start()

