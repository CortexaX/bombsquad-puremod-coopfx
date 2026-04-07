# -*- coding: utf-8 -*-

import bs
import bsInternal
import bsUtils
import os
import json
import re


def register(handlers, ctx):
    c = ctx['c']

    def _kick_by_target(target):
        try:
            cid = int(target)
            bsInternal._disconnectClient(cid)
        except Exception:
            c.kickByNick(target)

    def _handle_getlost(clientID, args, raw):
        _kick_by_target(args[0])
        return True

    def _handle_ooh(clientID, args, raw):
        if len(args) > 0:
            s = int(args[0])

            def _recur(cn):
                bs.playSound(bs.getSound('ooh'), volume=2)
                cn -= 1
                if cn > 0:
                    delay = int(args[1]) if len(args) > 1 else 1000
                    bs.gameTimer(delay, bs.Call(_recur, cn=cn))

            _recur(s)
        else:
            bs.playSound(bs.getSound('ooh'), volume=2)
        return True

    def _handle_play_sound(clientID, args, raw):
        if len(args) > 1:
            count = int(args[1])

            def _recur(cn):
                bs.playSound(bs.getSound(str(args[0])), volume=2)
                cn -= 1
                if cn > 0:
                    delay = int(args[2]) if len(args) > 2 else 1000
                    bs.gameTimer(delay, bs.Call(_recur, cn=cn))

            _recur(count)
        else:
            bs.playSound(bs.getSound(str(args[0])), volume=2)
        return True

    def _handle_nv(clientID, args, raw):
        if c.tint is None:
            c.tint = bs.getSharedObject('globals').tint
        off = (len(args) > 0 and args[0] == u'off')
        bs.getSharedObject('globals').tint = c.tint if off else (0.5, 0.7, 1)
        return True

    def _handle_end(clientID, args, raw):
        try:
            bsInternal._getForegroundHostActivity().endGame()
        except Exception:
            pass
        return True

    def _handle_tint(clientID, args, raw):
        if len(args) == 0:
            bsInternal._chatMessage('Using: /tint R G B')
            bsInternal._chatMessage('OR')
            bsInternal._chatMessage('Using: /tint r bright speed')
            return True

        if args[0] == 'r':
            if len(args) < 3:
                bs.screenMessage('Using: /tint r <bright> <speed>', color=(1, 0, 0), clients=[clientID], transient=True)
                return True
            m = float(args[1])
            s = float(args[2])
            bsUtils.animateArray(bs.getSharedObject('globals'), 'tint', 3,
                                 {0: (1 * m, 0, 0), s: (0, 1 * m, 0), s * 2: (0, 0, 1 * m), s * 3: (1 * m, 0, 0)},
                                 True)
            return True

        if len(args) < 3:
            bs.screenMessage('Using: /tint <r> <g> <b>', color=(1, 0, 0), clients=[clientID], transient=True)
            return True
        try:
            bs.getSharedObject('globals').tint = (float(args[0]), float(args[1]), float(args[2]))
        except Exception:
            bs.screenMessage('Error!', color=(1, 0, 0), clients=[clientID], transient=True)
        return True

    def _handle_sm(clientID, args, raw):
        g = bs.getSharedObject('globals')
        g.slowMotion = (g.slowMotion == False)
        return True

    def _handle_camera_mode(clientID, args, raw):
        try:
            g = bs.getSharedObject('globals')
            g.cameraMode = 'rotate' if g.cameraMode == 'follow' else 'follow'
        except Exception:
            pass
        return True

    def _handle_lm444(clientID, args, raw):
        arr = []
        for i in range(100):
            try:
                arr.append(bsInternal._getChatMessages()[-1 - i])
            except Exception:
                pass
        arr.reverse()
        for msg in arr:
            bsInternal._chatMessage(msg)
        return True

    def _handle_id(clientID, args, raw):
        if len(args) == 0:
            bsInternal._chatMessage('Using: /gp number of list')
            return True
        try:
            s = bsInternal._getForegroundHostSession()
            for i in s.players[int(args[0])].getInputDevice()._getPlayerProfiles():
                try:
                    bsInternal._chatMessage(i)
                except Exception:
                    pass
        except Exception:
            bs.screenMessage('PLAYER NOT FOUND', color=(1, 0, 0), clients=[clientID], transient=True)
        return True

    def _handle_icy(clientID, args, raw):
        try:
            act = bsInternal._getForegroundHostActivity()
            act.players[int(args[0])].actor.node = act.players[int(args[1])].actor.node
        except Exception:
            bs.screenMessage('Error!', color=(1, 0, 0), clients=[clientID], transient=True)
        return True

    def _handle_floor_reflection(clientID, args, raw):
        g = bs.getSharedObject('globals')
        g.floorReflection = (g.floorReflection == False)
        return True

    def _handle_ac(clientID, args, raw):
        if len(args) == 0:
            bsInternal._chatMessage('Using: /ac R G B')
            bsInternal._chatMessage('OR')
            bsInternal._chatMessage('Using: /ac r bright speed')
            return True

        if args[0] == 'r':
            if len(args) < 3:
                bs.screenMessage('Using: /ac r <bright> <speed>', color=(1, 0, 0), clients=[clientID], transient=True)
                return True
            m = float(args[1])
            s = float(args[2])
            bsUtils.animateArray(bs.getSharedObject('globals'), 'ambientColor', 3,
                                 {0: (1 * m, 0, 0), s: (0, 1 * m, 0), s * 2: (0, 0, 1 * m), s * 3: (1 * m, 0, 0)},
                                 True)
            return True

        if len(args) < 3:
            bs.screenMessage('Using: /ac <r> <g> <b>', color=(1, 0, 0), clients=[clientID], transient=True)
            return True
        try:
            bs.getSharedObject('globals').ambientColor = (float(args[0]), float(args[1]), float(args[2]))
        except Exception:
            bs.screenMessage('Error!', color=(1, 0, 0), clients=[clientID], transient=True)
        return True

    def _handle_ice_off(clientID, args, raw):
        activity = bsInternal._getForegroundHostActivity()
        try:
            activity.getMap().node.materials = [bs.getSharedObject('footingMaterial')]
            activity.getMap().isHockey = False
        except Exception:
            pass
        try:
            activity.getMap().floor.materials = [bs.getSharedObject('footingMaterial')]
            activity.getMap().isHockey = False
        except Exception:
            pass
        for i in activity.players:
            try:
                i.actor.node.hockey = False
            except Exception:
                pass
        return True

    def _set_reflections(mode_type, scale):
        act = bsInternal._getForegroundHostActivity()
        for part in ['node', 'bg', 'floor', 'center']:
            try:
                obj = getattr(act.getMap(), part)
                obj.reflection = mode_type
                obj.reflectionScale = scale
            except Exception:
                pass

    def _handle_reflections(clientID, args, raw):
        if len(args) < 2:
            bsInternal._chatMessage('Using: /reflections type(1/0) scale')
            return True
        try:
            rs = [int(args[1])]
            typ = 'soft' if int(args[0]) == 0 else 'powerup'
            _set_reflections(typ, rs)
        except Exception:
            bs.screenMessage('Error!', color=(1, 0, 0), clients=[clientID], transient=True)
        return True

    def _handle_reset(clientID, args, raw):
        _set_reflections('soft', 0)
        bs.getSharedObject('globals').ambientColor = (0, 0, 0)
        bs.getSharedObject('globals').tint = (1, 1, 1)
        return True

    def _handle_disco(clientID, args, raw):
        times = [0]

        def disco_red():
            bs.getSharedObject('globals').tint = (1, .6, .6)
            bs.gameTimer(230, bs.Call(disco_blue))

        def disco_blue():
            bs.getSharedObject('globals').tint = (.6, 1, .6)
            bs.gameTimer(230, bs.Call(disco_green))

        def disco_green():
            bs.getSharedObject('globals').tint = (.6, .6, 1)
            if times[0] < 10:
                times[0] += 1
                bs.gameTimer(230, bs.Call(disco_red))
            else:
                bs.getSharedObject('globals').tint = (1, 1, 1)

        bs.gameTimer(300, bs.Call(disco_red))
        return True

    def _handle_contact(clientID, args, raw):
        bs.screenMessage('discord QINUAN', color=(0, 0, 1), clients=[clientID], transient=True)
        return True

    def _handle_tag(clientID, args, raw):
        account_id = c.set_tag(clientID)
        if not account_id:
            bs.screenMessage('无法识别你的账号，请重试', color=(1, 0, 0), clients=[clientID], transient=True)
            return True

        tagfile = 'tag.json'
        if os.path.exists(tagfile):
            try:
                with open(tagfile) as f:
                    tag = json.loads(f.read())
            except Exception:
                tag = {}
        else:
            tag = {}

        if len(args) == 0:
            bs.screenMessage('没检测到你输入的标签', color=(1, 0, 0), clients=[clientID], transient=True)
            tag[account_id] = None
            with open(tagfile, 'w') as f:
                f.write(json.dumps(tag))
            return True

        text = args[0]
        patterns = [r"A\.D\.M\.I\.N", r"B\.O\.S\.S", r"腐竹", r"服主", r"owner", r"Owner", r"管理员", r"草泥马", r"妈", r"傻", r"逼", r"废", r"死", r"弟弟"]
        for pattern in patterns:
            if re.search(pattern, text):
                bs.screenMessage('好小子想造反啊', color=(1, 0, 0), clients=[clientID], transient=True)
                return True

        tag[account_id] = text[0:12]
        with open(tagfile, 'w') as f:
            f.write(json.dumps(tag))
        bs.screenMessage('标签保存成功: ' + text[0:12], color=(0, 1, 0), clients=[clientID], transient=True)
        return True

    handlers.update({
        '/getlost': _handle_getlost,
        '/ooh': _handle_ooh,
        '/playSound': _handle_play_sound,
        '/nv': _handle_nv,
        '/end': _handle_end,
        '/tint': _handle_tint,
        '/sm': _handle_sm,
        '/cameraMode': _handle_camera_mode,
        '/lm444': _handle_lm444,
        '/id': _handle_id,
        '/icy': _handle_icy,
        '/floorReflection': _handle_floor_reflection,
        '/ac': _handle_ac,
        '/iceOff': _handle_ice_off,
        '/reflections': _handle_reflections,
        '/reset': _handle_reset,
        '/disco': _handle_disco,
        '/contact': _handle_contact,
        '/tag': _handle_tag,
    })
