import logging
import traceback
from contextlib import contextmanager
from typing import List

import PySimpleGUI as sg

from ktlauncher.dirs import get_res_path

sg.theme('LightGray3')
log = logging.getLogger('ktlauncher')


def base_col() -> List[List[sg.Element]]:
    return [
        [
            sg.Text("Lucky Launcher", font='Verdana 18', pad=(50, 0)),
            sg.Image(str(get_res_path('lucky.png'))),
        ],
    ]


def make_window(col, main_window=True):
    base = base_col() if main_window else []
    layout = [
        [
            sg.Column(base + col),
        ],
    ]
    window = sg.Window("Lucky launcher", layout, font='Verdana 12')
    while True:
        event, values = window.read()
        log.debug(f'Event {event} {values}')
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        yield event, values


@contextmanager
def disable_buttons(*buttons: sg.Button):
    try:
        for b in buttons:
            b.update(disabled=True)
        yield
    finally:
        for b in buttons:
            b.update(disabled=False)


def show_message(header, text=None, mega_text=None):
    col = [[sg.Text(header, pad=(190, 0))]]
    if text:
        col.append([sg.Text(text, font='Verdana 8')])
    if mega_text:
        col.append([
            sg.Multiline(
                disabled=True,
                default_text=mega_text,
                size=(100, 50),
                font='Verdana 8',
            ),
        ])

    for _ in make_window(col, main_window=False):
        pass


def show_exception(err: Exception):
    exc_text = (
        str(err) + '\n' +
        '\n'.join(
            traceback.format_exception(None, err, err.__traceback__),
        )
    )
    show_message("Ошибка :(", mega_text=exc_text)
