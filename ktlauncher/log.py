import logging

from ktlauncher.dirs import get_log_file

log = logging.getLogger('ktlauncher')


def setup_log(root_file: str):
    log.setLevel('DEBUG')
    h1 = logging.StreamHandler()
    h1.setLevel('DEBUG')
    log.addHandler(h1)

    try:
        h2 = logging.FileHandler(filename=get_log_file(root_file), mode='w')
        h2.setLevel('DEBUG')
        log.addHandler(h2)
    except Exception:
        log.exception('Cannot add log file')
