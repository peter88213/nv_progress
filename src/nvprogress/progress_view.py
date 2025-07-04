"""Provide a tkinter widget for progress log display.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_progress
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.observer import Observer
from nvprogress.nvprogress_locale import _
from nvprogress.platform.platform_settings import KEYS
from nvprogress.platform.platform_settings import PLATFORM
from nvprogress.progress_view_ctrl import ProgressViewCtrl
import tkinter as tk


class ProgressView(tk.Toplevel, Observer, ProgressViewCtrl):

    def __init__(self, model, view, controller, prefs):
        tk.Toplevel.__init__(self)
        self.prefs = prefs

        self.geometry(self.prefs['window_geometry'])
        self.lift()
        self.focus()
        self.protocol("WM_DELETE_WINDOW", self.on_quit)
        if PLATFORM != 'win':
            self.bind(KEYS.QUIT_PROGRAM[0], self.on_quit)

        #--- Tree for log view.
        columns = (
            'date',
            'wordCount',
            'wordCountDelta',
            'totalWordCount',
            'totalWordCountDelta',
            'spacer',
            )
        self.tree = ttk.Treeview(self, selectmode='none', columns=columns)
        scrollY = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollY.set)
        scrollY.pack(side='right', fill='y')
        self.tree.pack(fill='both', expand=True)
        self.tree.heading('date', text=_('Date'))
        self.tree.heading('wordCount', text=_('Words total'))
        self.tree.heading('wordCountDelta', text=_('Daily'))
        self.tree.heading('totalWordCount', text=_('With unused'))
        self.tree.heading('totalWordCountDelta', text=_('Daily'))
        self.tree.column('#0', width=0)
        self.tree.column('date', anchor='center', width=self.prefs['date_width'], stretch=False)
        self.tree.column('wordCount', anchor='center', width=self.prefs['wordcount_width'], stretch=False)
        self.tree.column('wordCountDelta', anchor='center', width=self.prefs['wordcount_delta_width'], stretch=False)
        self.tree.column('totalWordCount', anchor='center', width=self.prefs['totalcount_width'], stretch=False)
        self.tree.column('totalWordCountDelta', anchor='center', width=self.prefs['totalcount_delta_width'], stretch=False)

        self.tree.tag_configure('positive', foreground='black')
        self.tree.tag_configure('negative', foreground='red')

        # "Close" button.
        ttk.Button(self, text=_('Close'), command=self.on_quit).pack(side='right', padx=5, pady=5)

        self.initialize_controller(model, view, controller, prefs)
        self._mdl.add_observer(self)

    def on_quit(self, event=None):
        self._mdl.delete_observer(self)
        self.prefs['window_geometry'] = self.winfo_geometry()
        self.prefs['date_width'] = self.tree.column('date', 'width')
        self.prefs['wordcount_width'] = self.tree.column('wordCount', 'width')
        self.prefs['wordcount_delta_width'] = self.tree.column('wordCountDelta', 'width')
        self.prefs['totalcount_width'] = self.tree.column('totalWordCount', 'width')
        self.prefs['totalcount_delta_width'] = self.tree.column('totalWordCountDelta', 'width')
        self.destroy()
        self.isOpen = False

    def refresh(self):
        self.build_tree()

    def reset_tree(self):
        """Clear the displayed tree."""
        for child in self.tree.get_children(''):
            self.tree.delete(child)

