# -*- coding: utf-8 -*-
"""
Standalone API4 effect mod: lightning strike on kill.

- Triggers when a player kills another player.
- Triggers when a player kills a bot.
- Safe for legacy API4 (Python 2.7).
"""

import random
import bs
import bsUtils
import bsSpaz


def bsGetAPIVersion():
    return 4


def bsGetGames():
    # Effect-only mod; no game modes to register.
    return []


_patched = False
_orig_player_spaz_handle = None
_orig_bot_spaz_handle = None


def _emit_lightning(pos):
    if pos is None:
        return

    x, y, z = pos

    # vertical lightning sparks
    for i in range(9):
        p = (x + random.uniform(-0.12, 0.12), y + (i * 0.65), z + random.uniform(-0.12, 0.12))
        bs.emitBGDynamics(position=p,
                          velocity=(random.uniform(-1.2, 1.2), random.uniform(-1.0, 1.0), random.uniform(-1.2, 1.2)),
                          count=random.randint(10, 20),
                          scale=0.35 + random.random() * 0.35,
                          spread=0.08,
                          chunkType='spark')

    # impact sparks near ground
    bs.emitBGDynamics(position=pos,
                      velocity=(0, 2.5, 0),
                      count=40,
                      scale=0.55,
                      spread=0.2,
                      chunkType='spark')

    # flash light
    light = bs.newNode('light', attrs={
        'position': (x, y + 2.2, z),
        'color': (0.55, 0.75, 1.25),
        'radius': 0.12,
        'heightAttenuated': False,
        'intensity': 0.0
    })
    bsUtils.animate(light, 'intensity', {0: 0.0, 40: 1.9, 95: 0.0})
    bsUtils.animate(light, 'radius', {0: 0.12, 40: 1.9, 95: 0.12})
    bs.gameTimer(120, light.delete)

    # thunder-ish sound stack
    try:
        bs.playSound(bs.getSound('impactHard2'), position=pos, volume=1.1)
    except Exception:
        pass
    try:
        bs.playSound(bs.getSound('shieldDown'), position=pos, volume=0.75)
    except Exception:
        pass


def _player_kill_by_other_player(self, msg):
    if getattr(self, '_dead', False):
        return False
    if msg.immediate or msg.how == 'leftGame':
        return False

    killer = None

    # same logic path as PlayerSpaz death attribution
    if (self.heldCount > 0 and self.lastPlayerHeldBy is not None
            and self.lastPlayerHeldBy.exists()):
        killer = self.lastPlayerHeldBy
    else:
        if (self.lastPlayerAttackedBy is not None
                and self.lastPlayerAttackedBy.exists()
                and bs.getGameTime() - self.lastAttackedTime < 4000):
            killer = self.lastPlayerAttackedBy

    if killer is None or not killer.exists():
        return False

    # ignore suicides
    try:
        if killer == self.getPlayer():
            return False
    except Exception:
        pass

    return True


def _bot_kill_by_player(self, msg):
    if getattr(self, '_dead', False):
        return False
    if msg.immediate:
        return False

    killer = None
    if (self.heldCount > 0 and self.lastPlayerHeldBy is not None
            and self.lastPlayerHeldBy.exists()):
        killer = self.lastPlayerHeldBy
    else:
        if (self.lastPlayerAttackedBy is not None
                and self.lastPlayerAttackedBy.exists()
                and bs.getGameTime() - self.lastAttackedTime < 4000):
            killer = self.lastPlayerAttackedBy

    return killer is not None and killer.exists()


def _patched_player_spaz_handle(self, msg):
    if isinstance(msg, bs.DieMessage):
        try:
            if _player_kill_by_other_player(self, msg) and self.node.exists():
                _emit_lightning(self.node.position)
        except Exception:
            pass
    return _orig_player_spaz_handle(self, msg)


def _patched_bot_spaz_handle(self, msg):
    if isinstance(msg, bs.DieMessage):
        try:
            if _bot_kill_by_player(self, msg) and self.node.exists():
                _emit_lightning(self.node.position)
        except Exception:
            pass
    return _orig_bot_spaz_handle(self, msg)


def install():
    global _patched
    global _orig_player_spaz_handle
    global _orig_bot_spaz_handle

    if _patched:
        return

    _orig_player_spaz_handle = bsSpaz.PlayerSpaz.handleMessage
    _orig_bot_spaz_handle = bsSpaz.SpazBot.handleMessage

    bsSpaz.PlayerSpaz.handleMessage = _patched_player_spaz_handle
    bsSpaz.SpazBot.handleMessage = _patched_bot_spaz_handle

    _patched = True
    print '[kill_lightning_fx] installed'


install()
