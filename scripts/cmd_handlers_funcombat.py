# -*- coding: utf-8 -*-

import bs
import bsInternal
import bsUtils
import random


_ALLOWED_SPAZ = ['ali', 'agent', 'bunny', 'cyborg', 'pixie', 'robot', 'alien', 'witch', 'wizard', 'bones', 'zoe', 'santa']


def _activity_players():
    try:
        return bs.getActivity().players
    except Exception:
        return []


def _session_players():
    try:
        return bs.getSession().players
    except Exception:
        return []


def _find_by_name(players, target):
    out = []
    for p in players:
        try:
            if p.getName().encode('utf-8') == target:
                out.append(p)
        except Exception:
            pass
    return out


def _resolve_players(target, players):
    if target == 'all':
        return list(players)
    if len(target) > 2:
        return _find_by_name(players, target)
    try:
        idx = int(target)
        if 0 <= idx < len(players):
            return [players[idx]]
    except Exception:
        pass
    return []


def _set_box_model(node, model_name, tex_name):
    node.torsoModel = bs.getModel(model_name)
    node.colorMaskTexture = bs.getTexture(tex_name)
    node.colorTexture = bs.getTexture(tex_name)
    node.highlight = (1, 1, 1)
    node.color = (1, 1, 1)
    node.headModel = None
    node.style = 'cyborg'


def _set_invisible(node):
    node.headModel = None
    node.torsoModel = None
    node.pelvisModel = None
    node.upperArmModel = None
    node.foreArmModel = None
    node.handModel = None
    node.upperLegModel = None
    node.lowerLegModel = None
    node.toesModel = None
    node.style = 'cyborg'


def _apply_spaz(node, name):
    node.colorTexture = bs.getTexture(name + 'Color')
    node.colorMaskTexture = bs.getTexture(name + 'ColorMask')
    node.headModel = bs.getModel(name + 'Head')
    node.torsoModel = bs.getModel(name + 'Torso')
    node.pelvisModel = bs.getModel(name + 'Pelvis')
    node.upperArmModel = bs.getModel(name + 'UpperArm')
    node.foreArmModel = bs.getModel(name + 'ForeArm')
    node.handModel = bs.getModel(name + 'Hand')
    node.upperLegModel = bs.getModel(name + 'UpperLeg')
    node.lowerLegModel = bs.getModel(name + 'LowerLeg')
    node.toesModel = bs.getModel(name + 'Toes')
    node.style = name


def register(handlers, ctx):
    c = ctx['c']

    def _handle_curse(clientID, args, raw):
        target = args[0]
        if target == 'all':
            if not c.checkRole('admin', clientID, silent=True):
                bs.screenMessage('你没有权限', color=(1, 0, 0), clients=[clientID], transient=True)
                return True
            for i in _session_players():
                try:
                    i.actor.curse()
                except Exception:
                    pass
            return True

        players = _resolve_players(target, _session_players())
        if not players:
            bs.screenMessage('PLAYER NOT FOUND', color=(1, 0, 0), clients=[clientID], transient=True)
            return True
        for p in players:
            try:
                p.actor.curse()
            except Exception:
                pass
        return True

    def _handle_box(clientID, args, raw):
        target = args[0]
        if target == 'all' and not c.checkRole('admin', clientID, silent=True):
            bs.screenMessage('你没有权限', color=(1, 0, 0), clients=[clientID], transient=True)
            return True

        players = _resolve_players(target, _session_players())
        for p in players:
            try:
                _set_box_model(p.actor.node, 'tnt', 'tnt')
            except Exception:
                pass
        return True

    def _handle_mine(clientID, args, raw):
        target = args[0]
        if target == 'all' and not c.checkRole('admin', clientID, silent=True):
            bs.screenMessage('你没有权限', color=(1, 0, 0), clients=[clientID], transient=True)
            return True

        players = _resolve_players(target, _session_players())
        for p in players:
            try:
                _set_box_model(p.actor.node, 'landMine', 'landMine')
            except Exception:
                pass
        return True

    def _handle_headless(clientID, args, raw):
        players = _resolve_players(args[0], _activity_players())
        if not players:
            bsInternal._chatMessage('PLAYER NOT FOUND')
            return True
        for p in players:
            try:
                if p.actor.exists():
                    p.actor.node.headModel = None
                    p.actor.node.style = 'cyborg'
            except Exception:
                pass
        bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
        return True

    def _handle_shield(clientID, args, raw):
        target = args[0]
        players = _resolve_players(target, _activity_players())
        if not players:
            bsInternal._chatMessage('PLAYER NOT FOUND')
            return True
        for p in players:
            try:
                if p.actor.exists():
                    p.actor.node.handleMessage(bs.PowerupMessage(powerupType='shield'))
            except Exception:
                pass
        bsInternal._chatMessage('shield will give you Protection')
        return True

    def _handle_celebrate(clientID, args, raw):
        players = _resolve_players(args[0], _activity_players())
        for p in players:
            try:
                if p.actor.exists():
                    p.actor.node.handleMessage('celebrate', 30000)
            except Exception:
                pass
        return True

    def _handle_remove(clientID, args, raw):
        target = args[0]
        if target == 'all':
            for p in _session_players():
                try:
                    p.removeFromGame()
                except Exception:
                    pass
            return True

        players = _resolve_players(target, _session_players())
        if not players:
            bsInternal._chatMessage('You cant remove any one')
            return True
        for p in players:
            try:
                p.removeFromGame()
            except Exception:
                pass
        return True

    def _handle_hug(clientID, args, raw):
        act_players = _activity_players()
        if args[0] == 'all':
            if not c.checkRole('admin', clientID, silent=True):
                bs.screenMessage('你没有权限', color=(1, 0, 0), clients=[clientID], transient=True)
                return True
            pairs = [(0, 1), (1, 0), (3, 2), (4, 3), (5, 6), (6, 7)]
            for a, b in pairs:
                try:
                    act_players[a].actor.node.holdNode = act_players[b].actor.node
                except Exception:
                    pass
            return True

        if len(args) < 2:
            bs.screenMessage('Using: /hug <indexA> <indexB> or /hug all', color=(1, 0, 0), clients=[clientID], transient=True)
            return True
        try:
            act_players[int(args[0])].actor.node.holdNode = act_players[int(args[1])].actor.node
        except Exception:
            pass
        return True

    def _toggle_gm(player):
        player.actor.node.hockey = (player.actor.node.hockey == False)
        player.actor.node.invincible = (player.actor.node.invincible == False)
        player.actor._punchPowerScale = 5 if player.actor._punchPowerScale == 1.2 else 1.2

    def _handle_gm(clientID, args, raw):
        act = _activity_players()
        if len(args) == 0:
            # Legacy behavior: no-arg /gm targets the issuer.
            for p in act:
                try:
                    if p.getInputDevice().getClientID() == clientID:
                        _toggle_gm(p)
                        return True
                except Exception:
                    pass
            return True

        try:
            p = act[int(args[0])]
            _toggle_gm(p)
        except Exception:
            bs.screenMessage('PLAYER NOT FOUND', color=(1, 0, 0), clients=[clientID], transient=True)
        return True

    def _handle_spaz(clientID, args, raw):
        if len(args) < 2:
            bs.screenMessage('Using: /spaz <all|index> <character>', color=(1, 0, 0), clients=[clientID], transient=True)
            return True
        target = args[0]
        char = args[1]
        if char not in _ALLOWED_SPAZ:
            bsInternal._chatMessage('use ali,agent,bunny,cyborg,pixie,robot,alien,witch,wizard,bones,santa,zoe')
            return True

        if target == 'all' and not c.checkRole('admin', clientID, silent=True):
            bs.screenMessage('你没有权限', color=(1, 0, 0), clients=[clientID], transient=True)
            return True

        players = _resolve_players(target, _session_players())
        for p in players:
            try:
                _apply_spaz(p.actor.node, char)
            except Exception:
                pass
        return True

    def _handle_inv(clientID, args, raw):
        target = args[0]
        if target == 'all' and not c.checkRole('admin', clientID, silent=True):
            bs.screenMessage('你没有权限', color=(1, 0, 0), clients=[clientID], transient=True)
            return True

        players = _resolve_players(target, _session_players())
        for p in players:
            try:
                _set_invisible(p.actor.node)
            except Exception:
                pass
        return True

    def _handle_punch(clientID, args, raw):
        if len(args) == 0:
            for p in _activity_players():
                try:
                    p.actor.node.handleMessage(bs.PowerupMessage(powerupType='punch'))
                except Exception:
                    pass
            bsInternal._chatMessage('MUST USE PLAYER ID OR NICK')
            return True

        players = _resolve_players(args[0], _activity_players())
        if not players:
            bsInternal._chatMessage('PLAYER NOT FOUND')
            return True
        for p in players:
            try:
                if p.actor.exists():
                    p.actor.node.handleMessage(bs.PowerupMessage(powerupType='punch'))
            except Exception:
                pass
        bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
        return True

    def _handle_gift(clientID, args, raw):
        powers = ['shield', 'punch', 'curse', 'health']
        for p in _activity_players():
            try:
                if p.actor.exists():
                    p.actor.node.handleMessage(bs.PowerupMessage(powerupType=powers[random.randrange(0, 4)]))
            except Exception:
                pass
        return True

    def _handle_shatter(clientID, args, raw):
        if len(args) < 2:
            bs.screenMessage('Using: /shatter <all|index> <value>', color=(1, 0, 0), clients=[clientID], transient=True)
            return True
        target = args[0]
        val = int(args[1])
        players = _resolve_players(target, _activity_players())
        for p in players:
            try:
                p.actor.node.shattered = val
            except Exception:
                pass
        return True

    def _handle_sleep(clientID, args, raw):
        players = _resolve_players(args[0], _session_players())
        for p in players:
            try:
                p.actor.node.handleMessage('knockout', 5000)
            except Exception:
                pass
        return True

    def _handle_cmr(clientID, args, raw):
        time_ms = 8000
        if len(args) > 0:
            try:
                time_ms = int(args[0])
            except Exception:
                pass

        op = 0.08
        std = bs.getSharedObject('globals').vignetteOuter
        bsUtils.animateArray(bs.getSharedObject('globals'), 'vignetteOuter', 3,
                             {0: bs.getSharedObject('globals').vignetteOuter, 17000: (0, 1, 0)})

        m = bsInternal._getForegroundHostActivity().getMap()
        for attr in ['node', 'bg', 'node1', 'node2', 'node3', 'steps', 'floor', 'center']:
            obj = None
            try:
                obj = getattr(m, attr)
                obj.opacity = op
            except Exception:
                pass
            try:
                if obj is not None and hasattr(obj, 'node'):
                    obj.node.opacity = op
            except Exception:
                pass

        def off():
            for attr in ['node', 'bg', 'node1', 'node2', 'node3', 'steps', 'floor', 'center']:
                obj = None
                try:
                    obj = getattr(m, attr)
                    obj.opacity = 1
                except Exception:
                    pass
                try:
                    if obj is not None and hasattr(obj, 'node'):
                        obj.node.opacity = 1
                except Exception:
                    pass
            bsUtils.animateArray(bs.getSharedObject('globals'), 'vignetteOuter', 3,
                                 {0: bs.getSharedObject('globals').vignetteOuter, 100: std})

        bs.gameTimer(time_ms, bs.Call(off))
        return True

    handlers.update({
        '/curse': _handle_curse,
        '/box': _handle_box,
        '/mine': _handle_mine,
        '/headless': _handle_headless,
        '/shield': _handle_shield,
        '/celebrate': _handle_celebrate,
        '/remove': _handle_remove,
        '/hug': _handle_hug,
        '/gm': _handle_gm,
        '/spaz': _handle_spaz,
        '/inv': _handle_inv,
        '/punch': _handle_punch,
        '/gift': _handle_gift,
        '/shatter': _handle_shatter,
        '/sleep': _handle_sleep,
        '/cmr': _handle_cmr,
    })
