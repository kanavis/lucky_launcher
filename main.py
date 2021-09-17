#!/usr/bin/env python3
import logging
import traceback

from ktlauncher.dirs import init_dirs
from ktlauncher.exceptions import KTUserError
from ktlauncher.gui import show_message, show_exception
from ktlauncher.load_packs import load_packs
from ktlauncher.log import setup_log
from ktlauncher.main_window import main_window

log = logging.getLogger('ktlauncher')


def main():
    try:
        setup_log(__file__)
        packs = load_packs()
        dirs = init_dirs()
        main_window(packs, dirs)
    except KeyboardInterrupt:
        print('Killed')
    except KTUserError as err:
        traceback.print_exc()
        log.error(f'User error {err}')
        show_message('Ошибка :/', str(err))
    except Exception as err:
        traceback.print_exc()
        log.exception('Unhandled error')
        show_exception(err)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('killed')
