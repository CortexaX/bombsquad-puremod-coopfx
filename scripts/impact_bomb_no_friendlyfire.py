# -*- coding: utf-8 -*-
"""
API4 gameplay rules patch:
1) Players + bots default to impact bombs.
2) Player explosion damage does not affect any players.
3) Friendly-fire between players is disabled.
"""

import bs
import bsSpaz


def bsGetAPIVersion():
    return 4


def bsGetGames():
    return []


_patched = False
_orig_spaz_init = None
_orig_player_handle = None


def _patched_spaz_init(self, *args, **kwargs):
    _orig_spaz_init(self, *args, **kwargs)
    try:
        self.bombTypeDefault = 'impact'
        self.bombType = 'impact'
    except Exception:
        pass


def _same_team(player_a, player_b):
    try:
        team_a = player_a.getTeam()
        team_b = player_b.getTeam()
        return (team_a is not None and team_b is not None and team_a is team_b)
    except Exception:
        return False


def _should_block_hit(victim_player_spaz, msg):
    if not isinstance(msg, bs.HitMessage):
        return False

    source_player = msg.sourcePlayer
    if source_player is None or not source_player.exists():
        return False

    victim_player = victim_player_spaz.getPlayer()
    if victim_player is None or not victim_player.exists():
        return False

    # Player bomb/explosion never hurts players (enemy or teammate).
    try:
        if msg.hitType == 'explosion':
            return True
    except Exception:
        pass

    # Disable all player-vs-player friendly fire.
    if _same_team(source_player, victim_player):
        return True

    return False


def _patched_player_handle(self, msg):
    if _should_block_hit(self, msg):
        return
    return _orig_player_handle(self, msg)


def install():
    global _patched
    global _orig_spaz_init
    global _orig_player_handle

    if _patched:
        return

    _orig_spaz_init = bsSpaz.Spaz.__init__
    _orig_player_handle = bsSpaz.PlayerSpaz.handleMessage

    bsSpaz.Spaz.__init__ = _patched_spaz_init
    bsSpaz.PlayerSpaz.handleMessage = _patched_player_handle

    _patched = True
    print '[impact_bomb_no_friendlyfire] installed'


install()
