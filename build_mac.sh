#!/bin/bash
env/bin/pyinstaller --osx-bundle-identifier 'Lucky Launcher' --icon 'ktlauncher/res/app_icon.icns' --windowed --add-data "./ktlauncher/res/lucky.png:./ktlauncher/res/" main.py
