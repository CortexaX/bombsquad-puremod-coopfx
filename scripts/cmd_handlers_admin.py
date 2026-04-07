# -*- coding: utf-8 -*-

import bs
import bsInternal


def _find_player_by_client_id(client_id):
    # Prefer session-level lookup: works in lobby/party and in-game.
    try:
        session = bsInternal._getForegroundHostSession()
        if session is not None:
            for p in session.players:
                try:
                    if p.getInputDevice().getClientID() == client_id:
                        return p
                except Exception:
                    pass
    except Exception:
        pass

    # Fallback to activity-level lookup.
    try:
        activity = bsInternal._getForegroundHostActivity()
        if activity is not None:
            for p in activity.players:
                try:
                    if p.getInputDevice().getClientID() == client_id:
                        return p
                except Exception:
                    pass
    except Exception:
        pass

    return None


def _get_roster_display_by_client_id(client_id):
    for client in bsInternal._getGameRoster():
        try:
            if int(client.get('clientID')) == int(client_id):
                return client.get('displayString', '')
        except Exception:
            pass
    return ''


def _get_account_id_by_client_id(client_id):
    # First try session players.
    try:
        session = bsInternal._getForegroundHostSession()
        if session is not None:
            for p in session.players:
                try:
                    if int(p.getInputDevice().getClientID()) == int(client_id):
                        return p.get_account_id()
                except Exception:
                    pass
    except Exception:
        pass

    # Then try activity players.
    try:
        activity = bsInternal._getForegroundHostActivity()
        if activity is not None:
            for p in activity.players:
                try:
                    if int(p.getInputDevice().getClientID()) == int(client_id):
                        return p.get_account_id()
                except Exception:
                    pass
    except Exception:
        pass

    # Finally try roster metadata (field names vary by build).
    try:
        for client in bsInternal._getGameRoster():
            try:
                if int(client.get('clientID')) == int(client_id):
                    aid = client.get('accountID') or client.get('accountId') or client.get('account_id')
                    if aid:
                        return aid
            except Exception:
                pass
    except Exception:
        pass

    return None


def _save_role_list(mid_storage, MID, key, values):
    clean = []
    for v in values:
        if v not in clean:
            clean.append(v)
    mid_storage.save(MID, {key: clean})


def register(handlers, ctx):
    MID = ctx['MID']
    mid_storage = ctx['mid_storage']

    def _mutate_role_list(clientID, args, key):
        cid = int(args[0])
        action = args[1].lower()

        aid = _get_account_id_by_client_id(cid)
        if not aid:
            bs.screenMessage('PLAYER NOT FOUND (check /list clientID)', color=(1, 0, 0), clients=[clientID], transient=True)
            return True

        current = list(getattr(MID, key))

        if action == 'add':
            if aid not in current:
                current.append(aid)
            cl_str = _get_roster_display_by_client_id(cid)
            if cl_str:
                try:
                    with open(bs.getEnvironment()['systemScriptsDirectory'] + '/membersidlogged.txt', mode='a') as fi:
                        fi.write(cl_str + ' || ' + aid + '\n')
                except Exception:
                    pass
        elif action == 'remove':
            if aid in current:
                current.remove(aid)
        else:
            bs.screenMessage('action must be add/remove', color=(1, 0, 0), clients=[clientID], transient=True)
            return True

        _save_role_list(mid_storage, MID, key, current)
        bs.screenMessage(key + ' updated', color=(0, 1, 0), clients=[clientID], transient=True)
        return True

    def _handle_admin(clientID, args, raw):
        return _mutate_role_list(clientID, args, 'admins')

    def _handle_vip(clientID, args, raw):
        return _mutate_role_list(clientID, args, 'vips')

    def _handle_member(clientID, args, raw):
        return _mutate_role_list(clientID, args, 'members')

    def _handle_quit(clientID, args, raw):
        bsInternal.quit()
        return True

    def _handle_max_players(clientID, args, raw):
        try:
            count = int(args[0])
            if count < 1:
                count = 1
            bsInternal._getForegroundHostSession()._maxPlayers = count
            bsInternal._setPublicPartyMaxSize(count)
            # keep config values aligned for future/new sessions
            bs.getConfig()['Team Game Max Players'] = count
            bs.getConfig()['Free-for-All Max Players'] = count
            bsInternal._chatMessage('Players limit set to ' + str(count))
        except Exception:
            bs.screenMessage('Error!', color=(1, 0, 0), clients=[clientID], transient=True)
        return True

    handlers.update({
        '/admin': _handle_admin,
        '/vip': _handle_vip,
        '/member': _handle_member,
        '/quit': _handle_quit,
        '/maxPlayers': _handle_max_players,
    })
