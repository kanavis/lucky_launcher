import dataclasses
from typing import Dict

import requests
from ktlauncher import settings


@dataclasses.dataclass
class Pack:
    name: str
    seq: int
    ver: str
    key: str
    md5: str


def load_packs() -> Dict[str, Pack]:
    res = requests.get(
        url=settings.SERVER_URL + '/packs',
        json=True,
    )
    return {r['name']: Pack(**r) for r in res.json().values()}
