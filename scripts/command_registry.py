# -*- coding: utf-8 -*-
"""
Command registry + precheck middleware for legacy cheatCmd.
Python 2.7 compatible.
"""

import bs


def _parse(msg):
    if msg is None:
        return '', []
    clean = msg.strip()
    if clean == '':
        return '', []
    parts = clean.split()
    return parts[0], parts[1:]


def build_default_registry():
    """
    role: owner|admin|vip|member|any
    min_args: int
    usage: shown when args are insufficient
    """
    reg = {
        '/help': {'role': 'any', 'min_args': 0},
        '/list': {'role': 'member', 'min_args': 0},
        '/me': {'role': 'any', 'min_args': 0},
        '/top': {'role': 'any', 'min_args': 0},
        '/ego': {'role': 'any', 'min_args': 0},

        '/kick': {'role': 'admin', 'min_args': 1, 'usage': '/kick <name|clientID>'},
        '/getlost': {'role': 'admin', 'min_args': 1, 'usage': '/getlost <name|clientID>'},

        '/admin': {'role': 'owner', 'min_args': 2, 'usage': '/admin <clientID> add|remove'},
        '/vip': {'role': 'admin', 'min_args': 2, 'usage': '/vip <clientID> add|remove'},
        '/member': {'role': 'owner', 'min_args': 2, 'usage': '/member <clientID> add|remove'},
        '/quit': {'role': 'owner', 'min_args': 0},
        '/maxPlayers': {'role': 'admin', 'min_args': 1, 'usage': '/maxPlayers <count>'},

        '/ooh': {'role': 'any', 'min_args': 0},
        '/playSound': {'role': 'any', 'min_args': 1, 'usage': '/playSound <sound> [count] [intervalMs]'},
        '/nv': {'role': 'any', 'min_args': 0},
        '/end': {'role': 'admin', 'min_args': 0},
        '/tint': {'role': 'admin', 'min_args': 1, 'usage': '/tint <r g b|r bright speed>'},
        '/sm': {'role': 'admin', 'min_args': 0},
        '/cameraMode': {'role': 'admin', 'min_args': 0},
        '/lm444': {'role': 'any', 'min_args': 0},
        '/id': {'role': 'admin', 'min_args': 1, 'usage': '/id <index>'},
        '/icy': {'role': 'admin', 'min_args': 2, 'usage': '/icy <srcIndex> <dstIndex>'},
        '/floorReflection': {'role': 'admin', 'min_args': 0},
        '/ac': {'role': 'admin', 'min_args': 1, 'usage': '/ac <r g b|r bright speed>'},
        '/iceOff': {'role': 'any', 'min_args': 0},
        '/reflections': {'role': 'admin', 'min_args': 2, 'usage': '/reflections <type(1/0)> <scale>'},
        '/reset': {'role': 'any', 'min_args': 0},
        '/disco': {'role': 'any', 'min_args': 0},
        '/contact': {'role': 'any', 'min_args': 0},
        '/tag': {'role': 'any', 'min_args': 0, 'usage': '/tag <text>'},

        '/freeze': {'role': 'member', 'min_args': 1, 'usage': '/freeze <all|index>'},
        '/thaw': {'role': 'member', 'min_args': 1, 'usage': '/thaw <all|index>'},
        '/kill': {'role': 'vip', 'min_args': 1, 'usage': '/kill <all|index>'},
        '/heal': {'role': 'member', 'min_args': 1, 'usage': '/heal <all|index>'},
        '/fly': {'role': 'admin', 'min_args': 1, 'usage': '/fly <all|index>'},

        '/curse': {'role': 'member', 'min_args': 1, 'usage': '/curse <all|index|name>'},
        '/box': {'role': 'any', 'min_args': 1, 'usage': '/box <all|index|name>'},
        '/mine': {'role': 'any', 'min_args': 1, 'usage': '/mine <all|index|name>'},
        '/headless': {'role': 'any', 'min_args': 1, 'usage': '/headless <all|index|name>'},
        '/shield': {'role': 'admin', 'min_args': 1, 'usage': '/shield <all|index|name>'},
        '/celebrate': {'role': 'any', 'min_args': 1, 'usage': '/celebrate <all|index|name>'},
        '/remove': {'role': 'admin', 'min_args': 1, 'usage': '/remove <all|index|name>'},
        '/hug': {'role': 'any', 'min_args': 1, 'usage': '/hug <all|indexA indexB>'},
        '/gm': {'role': 'admin', 'min_args': 0},
        '/spaz': {'role': 'any', 'min_args': 2, 'usage': '/spaz <all|index|name> <character>'},
        '/inv': {'role': 'any', 'min_args': 1, 'usage': '/inv <all|index|name>'},
        '/punch': {'role': 'admin', 'min_args': 0},
        '/gift': {'role': 'admin', 'min_args': 0},
        '/shatter': {'role': 'admin', 'min_args': 2, 'usage': '/shatter <all|index> <value>'},
        '/sleep': {'role': 'admin', 'min_args': 1, 'usage': '/sleep <all|index|name>'},
        '/cmr': {'role': 'admin', 'min_args': 0},
    }
    return reg


def precheck(cheat_options, client_id, msg, registry):
    """
    Returns (ok, normalized_msg).
    - ok=False means middleware already handled response.
    - normalized_msg can be passed to legacy handler.
    """
    cmd, args = _parse(msg)
    if cmd == '':
        return False, msg

    spec = registry.get(cmd)

    # Unknown command: pass through to legacy handler so behavior is unchanged.
    if spec is None:
        return True, msg

    role = spec.get('role', 'any')
    min_args = int(spec.get('min_args', 0))

    if role != 'any':
        if not cheat_options.checkRole(role, client_id, silent=True):
            bs.screenMessage('你没有权限', color=(1, 0, 0), clients=[client_id], transient=True)
            return False, msg

    if len(args) < min_args:
        usage = spec.get('usage')
        if usage:
            bs.screenMessage('Using: ' + usage,
                             color=(1, 0, 0), clients=[client_id], transient=True)
        else:
            bs.screenMessage('参数不足',
                             color=(1, 0, 0), clients=[client_id], transient=True)
        return False, msg

    return True, cmd + (' ' + ' '.join(args) if args else '')
