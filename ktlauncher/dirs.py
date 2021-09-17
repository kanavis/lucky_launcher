import os
from pathlib import Path

from ktlauncher import settings
from ktlauncher.exceptions import KTError, KTUserError
from ktlauncher.platform import plat


def get_res_path(res: str) -> Path:
    return Path(__file__).parent / Path('res') / Path(res)


def get_log_file(root_file: str):
    return Path(root_file).parent / Path('main.log')


class Dirs:
    def __init__(self):
        self.HOME_DIR = self._home_dir()
        self.MY_DIR = self.HOME_DIR / Path(self._wrap(settings.DIR_NAME))
        self.PACKS_DIR = self.MY_DIR / Path(settings.PACKS_DIR)
        self.TLAUNCHER_DIR = self.HOME_DIR / Path(self._wrap(settings.TLAUNCHER_DIR))
        self.MC_DIR = self.HOME_DIR / Path(self._wrap(settings.MC_DIR))

    def _wrap(self, s: str):
        if not plat.is_windows:
            s = '.' + s
        return s

    def _home_dir(self):
        if plat.is_windows:
            return Path(os.path.expandvars(r'%APPDATA%'))
        elif plat.is_mac:
            return Path(os.environ['HOME']) / Path(*settings.MAC_APP_PATH)
        else:
            return Path(os.environ['HOME'])

    @property
    def tlauncher_config(self):
        return self.TLAUNCHER_DIR / Path(settings.TLAUNCHER_CONF)

    @property
    def download_file(self):
        return self.MY_DIR / Path(settings.DOWNLOAD_FILE)

    def get_pack_path(self, mod_name: str):
        return self.PACKS_DIR / mod_name

    def get_pack_seq_path(self, mod_name: str):
        return self.get_pack_path(mod_name) / settings.SEQ_FILE

    def get_pack_file_list_path(self, mod_name: str):
        return self.get_pack_path(mod_name) / settings.FILE_LIST_FILE


def init_dirs():
    dirs = Dirs()
    if not os.path.exists(dirs.HOME_DIR):
        raise KTError('Home dir does not exist')
    if not os.path.exists(dirs.MY_DIR):
        os.makedirs(dirs.MY_DIR)
    if not os.path.exists(dirs.PACKS_DIR):
        os.makedirs(dirs.PACKS_DIR)
    if not (
        os.path.exists(dirs.TLAUNCHER_DIR) and
        os.path.exists(dirs.tlauncher_config)
    ):
        raise KTUserError('Ой, сначала надо хотя бы раз\nзапустить TLauncher')

    return dirs
