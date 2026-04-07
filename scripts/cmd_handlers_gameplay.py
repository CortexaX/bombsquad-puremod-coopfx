# -*- coding: utf-8 -*-

import bs
import bsInternal


def register(handlers, ctx):
    c = ctx['c']

    def _handle_freeze(clientID, args, raw):
        target = args[0]
        if target == 'all':
            if not c.checkRole('vip', clientID, silent=True):
                bs.screenMessage('你没有权限', color=(1, 0, 0), clients=[clientID], transient=True)
                return True
            for i in bs.getSession().players:
                try:
                    i.actor.node.handleMessage(bs.FreezeMessage())
                except Exception:
                    pass
            return True

        try:
            bs.getSession().players[int(target)].actor.node.handleMessage(bs.FreezeMessage())
        except Exception:
            bs.screenMessage('PLAYER NOT FOUND', color=(1, 0, 0), clients=[clientID], transient=True)
        return True

    def _handle_thaw(clientID, args, raw):
        target = args[0]
        if target == 'all':
            for i in bs.getSession().players:
                try:
                    i.actor.node.handleMessage(bs.ThawMessage())
                except Exception:
                    pass
            return True

        try:
            bs.getSession().players[int(target)].actor.node.handleMessage(bs.ThawMessage())
        except Exception:
            bs.screenMessage('PLAYER NOT FOUND', color=(1, 0, 0), clients=[clientID], transient=True)
        return True

    def _handle_kill(clientID, args, raw):
        target = args[0]
        if target == 'all':
            if not c.checkRole('admin', clientID, silent=True):
                bs.screenMessage('你没有权限', color=(1, 0, 0), clients=[clientID], transient=True)
                return True
            for i in bs.getSession().players:
                try:
                    i.actor.node.handleMessage(bs.DieMessage())
                except Exception:
                    pass
            return True

        try:
            bs.getSession().players[int(target)].actor.node.handleMessage(bs.DieMessage())
        except Exception:
            bs.screenMessage('PLAYER NOT FOUND', color=(1, 0, 0), clients=[clientID], transient=True)
        return True

    def _handle_heal(clientID, args, raw):
        target = args[0]

        if target == 'all':
            if not c.checkRole('admin', clientID, silent=True):
                bs.screenMessage('你没有权限', color=(1, 0, 0), clients=[clientID], transient=True)
                return True
            for i in bs.getActivity().players:
                try:
                    if i.actor.exists():
                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType='health'))
                except Exception:
                    pass
            return True

        if len(target) > 2:
            found = False
            for i in bs.getActivity().players:
                try:
                    if i.actor.exists() and i.getName().encode('utf-8') == target:
                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType='health'))
                        found = True
                except Exception:
                    pass
            if found:
                bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
            else:
                bsInternal._chatMessage('PLAYER NOT FOUND')
            return True

        try:
            bs.getActivity().players[int(target)].actor.node.handleMessage(bs.PowerupMessage(powerupType='health'))
            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
        except Exception:
            bsInternal._chatMessage('PLAYER NOT FOUND')
        return True

    def _handle_fly(clientID, args, raw):
        target = args[0]
        if target == 'all':
            for i in bsInternal._getForegroundHostActivity().players:
                try:
                    i.actor.node.fly = True
                except Exception:
                    pass
            return True

        try:
            p = bsInternal._getForegroundHostActivity().players[int(target)]
            p.actor.node.fly = (p.actor.node.fly == False)
        except Exception:
            bs.screenMessage('PLAYER NOT FOUND', color=(1, 0, 0), clients=[clientID], transient=True)
        return True

    handlers.update({
        '/freeze': _handle_freeze,
        '/thaw': _handle_thaw,
        '/kill': _handle_kill,
        '/heal': _handle_heal,
        '/fly': _handle_fly,
    })
