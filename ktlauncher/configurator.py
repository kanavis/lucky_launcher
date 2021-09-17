from shutil import copyfile

from ktlauncher.dirs import Dirs


def get_nl(s: str):
    if s.endswith('\r\n'):
        return '\r\n'
    else:
        return '\n'


def set_config_value(dirs: Dirs, key: str, value: str):
    config = dirs.tlauncher_config
    copyfile(config, str(config) + '.bak')

    rows = []
    changed = False
    with open(config, 'r') as f:
        for row in f:
            parts = row.split('=', 1)
            if len(parts) == 2 and parts[0].strip() == key:
                row = parts[0] + '=' + value + get_nl(parts[1])
                changed = True
            rows.append(row)

    if not changed:
        nl = get_nl(parts[0]) if parts else '\n'
        rows.append(key + '=' + value + nl)

    with open(config, 'w') as f:
        for row in rows:
            f.write(row)
