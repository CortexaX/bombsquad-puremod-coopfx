# -*- coding: utf-8 -*-
"""
Persistence helpers for membersID.json.
"""

import os
import json


def _members_json_path():
    import bs
    return os.path.join(bs.getEnvironment()['systemScriptsDirectory'], 'membersID.json')


def _atomic_write(path, content):
    tmp_path = path + '.tmp'
    f = open(tmp_path, 'w')
    try:
        f.write(content)
    finally:
        f.close()
    os.rename(tmp_path, path)


def _load_json(path):
    if not os.path.exists(path):
        return {}
    f = open(path, 'r')
    try:
        data = json.loads(f.read())
    finally:
        f.close()
    return data if isinstance(data, dict) else {}


def save(mid_module, updates):
    """
    Persist selected keys to membersID.json and reload membersID module.

    Args:
        mid_module: imported membersID module object (usually MID).
        updates: dict, e.g. {'admins': [...], 'authentication': {...}}
    """
    if not updates:
        return False

    try:
        # keep runtime module state in sync first
        for key, value in updates.items():
            setattr(mid_module, key, value)

        path = _members_json_path()
        data = _load_json(path)

        # prefer module defaults if available
        try:
            defaults = getattr(mid_module, '_DEFAULT_DATA', None)
            if isinstance(defaults, dict):
                merged = dict(defaults)
                merged.update(data)
                data = merged
        except Exception:
            pass

        data.update(updates)
        _atomic_write(path, json.dumps(data, indent=2, sort_keys=True))

        # reload membersID to refresh globals from json
        reload(mid_module)
        return True
    except Exception:
        try:
            import bs
            bs.printException('mid_storage.save failed')
        except Exception:
            pass
        return False
