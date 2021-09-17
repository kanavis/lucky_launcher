import hashlib
import logging
import os
import zipfile

import requests

from ktlauncher import settings
from ktlauncher.configurator import set_config_value
from ktlauncher.dirs import Dirs
import PySimpleGUI as sg

from ktlauncher.load_packs import Pack

log = logging.getLogger('ktlauncher')


def download_pack(url: str, local_filename: str, prb_text: sg.Text, prb: sg.ProgressBar):
    prb_text.update('Качаем модпак')
    with requests.get(url, stream=True, timeout=5) as r:
        log.debug(f'Opened stream {url}')
        r.raise_for_status()
        current_count = 0
        max_val = int(r.headers['Content-Length'])
        prb.update(current_count=current_count, max=max_val)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                current_count += len(chunk)
                prb.update(current_count=current_count)
                percents = int(current_count * 100/max_val)
                prb_text.update(f'Качаем модпак {percents}%')


def unzip_pack(zip_path: str, target_path: str, prb_text: sg.Text, prb: sg.ProgressBar):
    with zipfile.ZipFile(zip_path) as zf:
        infolist = zf.infolist()
        prb_text.update('Распаковываем модпак')
        max_val = len(infolist)
        prb.update(0, max=max_val)
        for current_count, member in enumerate(infolist, 1):
            zf.extract(member, target_path)
            prb.update(current_count=current_count)
            percents = int(current_count * 100 / max_val)
            prb_text.update(f'Распаковываем модпак {percents}%')


def get_local_md5(file_path: str) -> str:
    m = hashlib.md5()
    with open(file_path, 'rb') as f:
        line = f.read()
        m.update(line)
    local_md5 = m.hexdigest()
    log.debug(f'Got local md5 {local_md5}')
    return local_md5


def check_is_downloaded(pack: Pack, dirs: Dirs):
    if not os.path.exists(dirs.download_file):
        return False
    local_md5 = get_local_md5(dirs.download_file)
    log.debug(f'Remote md5 is {pack.md5}')
    return local_md5 == pack.md5


def write_seq(file_path: str, seq: int):
    with open(file_path, 'w') as f:
        f.write(str(seq))


def read_seq(file_path: str) -> int:
    with open(file_path, 'r') as f:
        return int(f.read().strip())


def write_file_list(pack_dir: str, file_list_path: str):
    pass


def check_file_list(pack_dir: str, file_list_path: str):
    pass


def check_is_unpacked(pack: Pack, pack_dir: str, seq_path: str, file_list_path: str):
    if not os.path.isdir(pack_dir):
        log.debug('Pack dir is missing')
        return False
    if not os.path.exists(seq_path):
        log.debug('Pack seq file is missing')
        return False
    if not os.path.exists(file_list_path):
        log.debug('Pack file list file is missing')
        return False
    local_seq = read_seq(seq_path)
    if pack.seq != local_seq:
        log.debug(f'Local seq: local != remote: {local_seq} != {pack.seq}')
        return False
    if not check_file_list(pack_dir, file_list_path):
        return False


def set_pack(pack: Pack, dirs: Dirs, prb_text: sg.Text, prb: sg.ProgressBar):
    prb_text.update('Подготовка')
    pack_dir = str(dirs.get_pack_path(pack.key))
    seq_path = str(dirs.get_pack_seq_path(pack.key))
    file_list_path = str(dirs.get_pack_file_list_path(pack.key))

    if check_is_unpacked(pack, pack_dir, seq_path, file_list_path):
        log.debug('Modpack is already unpacked and unbroken')
    else:
        if check_is_downloaded(pack, dirs):
            log.debug('File already exists with correct checksum')
        else:
            pack_url = settings.SERVER_URL + '/download/' + pack.key
            log.debug(f'Download pack {pack.name} from url {pack_url}')
            download_pack(pack_url, dirs.download_file, prb_text, prb)

        log.debug('Unzip pack')
        unzip_pack(dirs.download_file, pack_dir, prb_text, prb)

        write_file_list(pack_dir, file_list_path)
        write_seq(seq_path, pack.seq)

    set_config_value(dirs, settings.GAME_DIR_OPTION, pack_dir)
    set_config_value(dirs, settings.VERSION_OPTION, pack.ver)
    log.debug('Modpack setup complete')


def do_reset(dirs: Dirs):
    log.debug(f'Reset game dir to {dirs.MC_DIR}')
    set_config_value(dirs, settings.GAME_DIR_OPTION, str(dirs.MC_DIR))
