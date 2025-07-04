#!/usr/bin/python3
"""Install the nv_progress plugin. 

Version @release

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_progress
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
from shutil import copytree
from shutil import copy2
from pathlib import Path
try:
    from tkinter import *
except ModuleNotFoundError:
    print('The tkinter module is missing. Please install the tk support package for your python3 version.')
    sys.exit(1)

PLUGIN = 'nv_progress.py'
VERSION = ' @release'

root = Tk()
processInfo = Label(root, text='')
message = []


def output(text):
    message.append(text)
    processInfo.config(text=('\n').join(message))


if __name__ == '__main__':
    scriptPath = os.path.abspath(sys.argv[0])
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    # Open a tk window.
    root.geometry("600x150")
    root.title(f'Install {PLUGIN}{VERSION}')
    header = Label(root, text='')
    header.pack(padx=5, pady=5)

    # Prepare the messaging area.
    processInfo.pack(padx=5, pady=5)

    # Install the plugin.
    homePath = str(Path.home()).replace('\\', '/')
    noveltreeDir = f'{homePath}/.noveltree'
    if os.path.isdir(noveltreeDir):
        if os.path.isfile(f'./{PLUGIN}'):
            pluginDir = f'{noveltreeDir}/plugin'
            os.makedirs(pluginDir, exist_ok=True)
            copy2(PLUGIN, f'{pluginDir}/{PLUGIN}')
            output(f'Sucessfully installed "{PLUGIN}" at "{os.path.normpath(pluginDir)}"')
        else:
            output(f'ERROR: file "{PLUGIN}" not found.')

        # Install the localization files.
        output(f'Copying locale ...')
        copytree('locale', f'{noveltreeDir}/locale', dirs_exist_ok=True)

        # Install the icon files.
        output(f'Copying icons ...')
        copytree('icons', f'{noveltreeDir}/icons', dirs_exist_ok=True)
    else:
        output(f'ERROR: Cannot find a noveltree installation at "{noveltreeDir}"')

    root.quitButton = Button(text="Quit", command=quit)
    root.quitButton.config(height=1, width=30)
    root.quitButton.pack(padx=5, pady=5)
    root.mainloop()
