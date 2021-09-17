import logging
import threading
import traceback

import PySimpleGUI as sg
import requests

from ktlauncher.exceptions import KTUserError
from ktlauncher.modpacks import set_pack, do_reset
from ktlauncher.gui import make_window, disable_buttons, show_message, \
    show_exception

log = logging.getLogger('ktlauncher')


def run_in_thread(fn):
    def _fn():
        try:
            fn()
        except KTUserError as err:
            traceback.print_exc()
            log.error(f'User error {err} in thread')
            show_message('Ошибка :/', str(err))
        except requests.Timeout as err:
            traceback.print_exc()
            log.error(f'Timeout {err}')
            show_message('Ошибка :/', 'Таймаут соединения с сервером', str(err))
        except Exception as err:
            traceback.print_exc()
            log.exception('Unhandled error in thread')
            show_exception(err)
    t = threading.Thread(target=_fn, daemon=True)
    t.start()


def main_window(packs, dirs):
    ok_button = sg.Button("Установить модпак", pad=((0, 0), (20, 0)), key='-OK-')
    reset_button = sg.Button("Отключить модпак", pad=((50, 0), (20, 0)), enable_events=True, key='-RESET-')
    prb_text = sg.Text()
    prb = sg.ProgressBar(max_value=1, expand_x=True, size=(0, 10), border_width=1, relief=sg.RELIEF_RAISED)
    list_values = [p.name for p in packs.values()]
    packs_box = sg.Combo(
        values=list_values,
        default_value=list_values[0],
        size=(40, 20),
        key="-PACKS-",
        readonly=True,
    )
    col = [
        [sg.Text("Модпак"), packs_box],
        [ok_button, reset_button],
        [prb_text],
        [prb],
    ]

    for event, values in make_window(col):
        if str(event) == '-OK-':
            def run():
                with disable_buttons(ok_button, reset_button):
                    pack_name = values['-PACKS-']
                    try:
                        set_pack(packs[pack_name], dirs, prb_text, prb)
                    finally:
                        prb_text.update('')
                    prb_text.update('Модпак установлен')
            run_in_thread(run)
        elif str(event) == '-RESET-':
            with disable_buttons(ok_button, reset_button):
                do_reset(dirs)
                prb_text.update('Модпак отключен')
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
