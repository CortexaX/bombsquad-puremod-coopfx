# -*- coding: utf-8 -*-

import bs
import bsInternal
import os
import json


def register(handlers, ctx):
    c = ctx['c']
    MID = ctx['MID']
    help_fn = ctx['_help_msg']
    print_top10 = ctx['print_top10']
    get_info = ctx['get_info']
    get_account_id_by_clientid = ctx['get_account_id_by_clientid']

    def _handle_help(clientID, args, raw):
        help_fn(clientID)
        return True

    def _handle_list(clientID, args, raw):
        bs.screenMessage('========For kick=======', color=(1, 0, 0), clients=[clientID], transient=True)
        for i in bsInternal._getGameRoster():
            try:
                bs.screenMessage(i['players'][0]['nameFull'].encode('utf-8') +
                                 '     (/kick ' + str(i['clientID']) + ')',
                                 color=(1, 0.4, 0), clients=[clientID], transient=True)
            except Exception:
                pass
        bs.screenMessage('=================', color=(1, 0, 0), clients=[clientID], transient=True)
        bs.screenMessage('========For Other Commands=======', color=(1, 0.6, 0.4), clients=[clientID], transient=True)
        for s in bsInternal._getForegroundHostSession().players:
            bs.screenMessage(s.getName() + '     ' + str(bsInternal._getForegroundHostSession().players.index(s)),
                             color=(0.5, 0.7, 0.3), clients=[clientID], transient=True)
        return True

    def _handle_kick(clientID, args, raw):
        target = args[0]
        try:
            cid = int(target)
            accountid = None
            for cl in bsInternal._getForegroundHostSession().players:
                if cl.getInputDevice().getClientID() == cid:
                    accountid = cl.get_account_id()
                    break
            if accountid in MID.owners:
                bs.screenMessage('cant kick owner', color=(1, 0, 0), clients=[clientID], transient=True)
                return True
            bsInternal._disconnectClient(cid)
            return True
        except Exception:
            c.kickByNick(target)
            return True

    def _handle_me(clientID, args, raw):
        query_cid = clientID
        if len(args) > 0:
            try:
                query_cid = int(args[0])
            except Exception:
                bs.screenMessage('clientID must be a number', color=(1, 0, 0), clients=[clientID], transient=True)
                return True

        playeraccountid = ''
        playername = ''
        for i in bsInternal._getForegroundHostActivity().players:
            if i.getInputDevice().getClientID() == query_cid:
                playeraccountid = i.get_account_id()
                playername = i.getName()
                break

        if playeraccountid == '':
            bs.screenMessage('PLAYER NOT FOUND', color=(1, 0, 0), clients=[clientID], transient=True)
            return True

        stats = {}
        if os.path.exists('stats.json'):
            try:
                with open('stats.json') as f:
                    stats = json.loads(f.read())
            except Exception:
                stats = {}

        if playeraccountid not in stats:
            bs.screenMessage('Not played any match yet', color=(0, 1, 1), clients=[clientID], transient=True)
        else:
            killed = stats[playeraccountid].get('killed', 0)
            kills = stats[playeraccountid].get('kills', 0)
            played = stats[playeraccountid].get('played', 0)
            bs.screenMessage(playername + ':' + ' Kills:' + str(kills) + ', Killed:' + str(killed) + ', Matches:' + str(played),
                             color=(0, 1, 1), clients=[clientID], transient=True)
        return True

    def _handle_top(clientID, args, raw):
        top = print_top10()
        bs.screenMessage(top, color=(1, 1, 1), clients=[clientID], transient=True)
        return True

    def _handle_ego(clientID, args, raw):
        account_id = get_account_id_by_clientid(clientID)
        info = get_info(account_id)
        if info is None:
            bs.screenMessage('请进入游戏再查询', color=(1, 0, 0), clients=[clientID], transient=True)
            return True

        kills = info['kills']
        killed = info['killed']
        kd = float(kills) / killed if killed > 0 else float(kills)
        kd_str = u"%.2f" % kd
        bs.screenMessage(
            u"" + info['name_full'] +
            u" 得分: " + unicode(info['scores']) +
            u" KD: " + kd_str +
            u" 距上一名还差分数: " + (unicode(info['diff_to_prev']) if info['diff_to_prev'] is not None else u"无"),
            color=(1, 1, 1), clients=[clientID], transient=True)
        return True

    handlers.update({
        '/help': _handle_help,
        '/list': _handle_list,
        '/kick': _handle_kick,
        '/me': _handle_me,
        '/top': _handle_top,
        '/ego': _handle_ego,
    })
