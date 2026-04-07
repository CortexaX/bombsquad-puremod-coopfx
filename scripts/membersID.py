# -*- coding: utf-8 -*-
"""
membersID runtime data loader.

Source of truth is now membersID.json (same directory).
Other modules can keep using: import membersID as MID
"""

import os
import json
import bs


_DEFAULT_DATA = {
    'allAdmins': False,
    'admins': ['pb-IF4sUVcqDQ=='],
    'vips': ['pb-IF4IUW4nEA==', 'pb-IF4nUWcuCw=='],
    'members': [],
    'owners': [],
    'members_count': [],
    'mods': [],
    'nooby': [],
    'whitelist': [],
    'muted': [],
    'rejected': [],
    'sparkEffect': [],
    'splinterEffect': [],
    'slimeEffect': [],
    'metalEffect': [],
    'smokeEffect': [],
    'iceEffect': [],
    'colorEffect': [],
    'lightEffect': [],
    'glowEffect': [],
    'crownTag': [],
    'dragonTag': [],
    'helmetTag': [],
    'bombTag': [],
    'tripleMan': [],
    'iceMan': [],
    'impactMan': [],
    'invMan': [],
    'radiusMan': [],
    'morLife': [],
    'spazBombMan': [],
    'glueMan': [],
    'speedMan': [],
    'bombMan': [],
    'mod2': [],
    'mute5': [],
    'owner2': [],
    'authentication': {},
    'verification': []
}


def _json_path():
    return os.path.join(bs.getEnvironment()['systemScriptsDirectory'], 'membersID.json')


def _atomic_write(path, content):
    tmp_path = path + '.tmp'
    f = open(tmp_path, 'w')
    try:
        f.write(content)
    finally:
        f.close()
    os.rename(tmp_path, path)


def _save_json(data):
    _atomic_write(_json_path(), json.dumps(data, indent=2, sort_keys=True))


def _load_json():
    path = _json_path()
    data = dict(_DEFAULT_DATA)

    if os.path.exists(path):
        try:
            f = open(path, 'r')
            try:
                raw = json.loads(f.read())
            finally:
                f.close()
            if isinstance(raw, dict):
                for k, v in raw.items():
                    if k in data:
                        data[k] = v
        except Exception:
            # keep defaults if json is broken
            pass
    else:
        # first run: emit json with defaults
        _save_json(data)

    return data


_data = _load_json()
for _k, _v in _data.items():
    globals()[_k] = _v
