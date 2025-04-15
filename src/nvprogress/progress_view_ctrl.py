"""Provide a mixin class for a progress view controller.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_progress
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date

from nvlib.controller.sub_controller import SubController


class ProgressViewCtrl(SubController):

    def initialize_controller(self, model, view, controller, prefs):
        super().initialize_controller(model, view, controller)
        self.isOpen = True
        self.build_tree()

    def build_tree(self):
        self.reset_tree()
        wcLog = {}

        # Copy the read-in word count log.
        for wcDate in self._mdl.prjFile.wcLog:
            sessionDate = date.fromisoformat(wcDate).strftime('%x')
            wcLog[sessionDate] = self._mdl.prjFile.wcLog[wcDate]

        # Add the word count determined when opening the project.
        for wcDate in self._mdl.prjFile.wcLogUpdate:
            sessionDate = date.fromisoformat(wcDate).strftime('%x')
            wcLog[sessionDate] = self._mdl.prjFile.wcLogUpdate[wcDate]

        # Add the actual word count.
        newCountInt, newTotalCountInt = self._mdl.prjFile.count_words()
        newCount = str(newCountInt)
        newTotalCount = str(newTotalCountInt)
        today = date.today().strftime('%x')
        wcLog[today] = [newCount, newTotalCount]

        lastCount = 0
        lastTotalCount = 0
        for wc in wcLog:
            countInt = int(wcLog[wc][0])
            countDiffInt = countInt - lastCount
            totalCountInt = int(wcLog[wc][1])
            totalCountDiffInt = totalCountInt - lastTotalCount
            if countDiffInt == 0 and totalCountDiffInt == 0:
                continue

            if countDiffInt > 0:
                nodeTags = ('positive')
            else:
                nodeTags = ('negative')
            columns = [
                wc,
                str(wcLog[wc][0]),
                str(countDiffInt),
                str(wcLog[wc][1]),
                str(totalCountDiffInt),
                ]
            lastCount = countInt
            lastTotalCount = totalCountInt
            # startIndex = 'end'
            # chronological order
            startIndex = '0'
            # reverse order
            self.tree.insert('', startIndex, iid=wc, values=columns, tags=nodeTags, open=True)

