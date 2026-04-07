# -*- coding: utf-8 -*-
#https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
import bs
import bsInternal
import bsPowerup
import bsUtils
import random
import membersID as MID
import mid_storage
import command_registry
import cmd_handlers_social
import cmd_handlers_admin
import cmd_handlers_gameplay
import cmd_handlers_system
import cmd_handlers_funcombat
import BuddyBunny
import os
import json
import re



class cheatOptions(object):
    def __init__(self):
        self.all = True # just in case
       
        
        self.tint = None # needs for /nv
    
    def _get_account_id(self, clientID):
        client = None
        try:
            activity = bsInternal._getForegroundHostActivity()
            if activity is None:
                return None
            for i in activity.players:
                if i.getInputDevice().getClientID() == clientID:
                    client = i.get_account_id()
                    break
        except Exception:
            client = None
        return client

    def checkRole(self, role, clientID, silent=False):
        client = self._get_account_id(clientID)
        allowed = False

        if MID.allAdmins:
            allowed = True
        elif role == 'owner':
            allowed = (client in MID.owners)
        elif role == 'admin':
            allowed = (client in MID.admins or client in MID.owners)
        elif role == 'vip':
            allowed = (client in MID.vips or client in MID.admins or client in MID.owners)
        elif role == 'member':
            allowed = (client in MID.members or client in MID.vips or client in MID.admins or client in MID.owners)
        elif role == 'any':
            allowed = True

        if not silent:
            if allowed:
                bs.screenMessage('指令使用成功', color=(random.random(), random.random(), random.random()),
                                 clients=[clientID], transient=True)
            else:
                bs.screenMessage('你没有权限', color=(1, 0, 0), clients=[clientID], transient=True)

        return allowed

    def checkOwner(self, clientID):
        return self.checkRole('owner', clientID, silent=False)

    def checkAdmin(self, clientID):
        return self.checkRole('admin', clientID, silent=False)

    def checkMember(self, clientID):
        return self.checkRole('member', clientID, silent=False)

    def checkVip(self, clientID):
        return self.checkRole('vip', clientID, silent=False)
    def set_tag(self,clientID):
        # Always define attribute to avoid AttributeError in UI-context edge cases.
        self.tag_client = None
        try:
            self.tag_client = self._get_account_id(clientID)
        except Exception:
            self.tag_client = None
        return self.tag_client
    def kickByNick(self,nick):
        roster = bsInternal._getGameRoster()
        for i in roster:
            try:
                if i['players'][0]['nameFull'].lower().find(nick.encode('utf-8').lower()) != -1:
                    bsInternal._disconnectClient(int(i['clientID']))
            except:
                pass
      #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
    def opt(self,clientID,msg):
        """Legacy entry kept for compatibility; command logic moved to modular handlers."""
        bs.screenMessage('指令不存在', color=(1, 0, 0), clients=[clientID], transient=True)
        return

c = cheatOptions()
COMMANDS = command_registry.build_default_registry()

# Round-6: move all known command routing into registry/dispatcher.
# Unmigrated commands are routed via legacy passthrough handlers.
ALL_KNOWN_COMMANDS = [
    '/ac', '/admin', '/box', '/cameraMode', '/celebrate', '/cmr', '/contact', '/curse',
    '/disco', '/ego', '/end', '/floorReflection', '/fly', '/freeze', '/getlost', '/gift',
    '/gm', '/headless', '/heal', '/help', '/hug', '/iceOff', '/icy', '/id', '/inv', '/kick',
    '/kill', '/list', '/lm444', '/maxPlayers', '/me', '/member', '/mine', '/nv', '/ooh',
    '/playSound', '/punch', '/quit', '/reflections', '/remove', '/reset', '/shatter',
    '/shield', '/sleep', '/sm', '/spaz', '/tag', '/thaw', '/tint', '/top', '/vip'
]

def _help_msg(clientID):


    bs.screenMessage('Try commands', color=(random.random(), random.random(),random.random()), clients=[clientID], transient=True)

    bs.screenMessage('/inv /spaz /box /headless', color=(random.random(), random.random(),random.random()), clients=[clientID], transient=True)

    bs.screenMessage('/shatter /sleep /iceoff /heal', color=(random.random(), random.random(),random.random()), clients=[clientID], transient=True)

    bs.screenMessage('/fly /gm /hug /remove /alien all', color=(random.random(), random.random(),random.random()), clients=[clientID], transient=True)

    bs.screenMessage('/freeze all /nv /ooh /mine all  /sm /end /curse', color=(random.random(), random.random(),random.random()), clients=[clientID],
                     transient=True)

    bs.screenMessage('/kick /remove /bouncer /mix /thanos and many more', color=(random.random(), random.random(),random.random()), clients=[clientID],
                     transient=True)

def cmnd(msg,clientID):
    if bsInternal._getForegroundHostActivity() is not None:
        ok, normalized = command_registry.precheck(c, clientID, msg, COMMANDS)
        if not ok:
            return

        # Round-6: all known commands are now registry-routed.
        if _dispatch_registry_command(clientID, normalized):
            return

        # Unknown command fallback (future custom command safety-net).
        c.opt(clientID, normalized)
bs.realTimer(5000,bs.Call(bsInternal._setPartyIconAlwaysVisible,True))

import bsUI
bs.realTimer(10000,bs.Call(bsUI.onPartyIconActivate,(0,0)))## THATS THE TRICKY PART check ==> 23858 bsUI / _handleLocalChatMessage


def get_info(account_id):
    '''
    print u"账号ID:", info["account_id"]
    print u"昵称:", info["name_full"]
    print u"击杀:", info["kills"]
    print u"得分:", info["scores"]
    print u"对局:", info["played"]
    print u"被杀:", info["killed"]
    print u"当前排名:", info["rank"]
    if not info["diff_to_prev"] is None:
        print u"距上一名还差分数:", info["diff_to_prev"]
    '''
    with open('stats2.json', 'r') as f:
        data = json.load(f)

    ranking = sorted(
        data.items(),
        key=lambda x: x[1].get("scores", 0),
        reverse=True
    )

    rank = None
    for idx, (aid, info) in enumerate(ranking, start=1):
        if aid == account_id:
            rank = idx
            break

    if account_id not in data:
        return None

    info = data[account_id]

    result = {
        "account_id": account_id,
        "name_full": info.get("name_full"),
        "kills": info.get("kills"),
        "scores": info.get("scores"),
        "played": info.get("played"),
        "killed": info.get("killed"),
        "rank": rank
    }

    if rank:
        if rank > 1:
            prev_score = ranking[rank-2][1].get("scores", 0)
            curr_score = info.get("scores", 0)
            diff = prev_score - curr_score
            result["diff_to_prev"] = diff
        else:
            result["diff_to_prev"] = None  # 第一名，没有上一名

    return result


import re

def print_top10():
    def clean_name(html_name):
        # 简单用正则去除所有标签，提取纯文本
        return re.sub(r'<.*?>', '', html_name).strip()

    with open('stats2.json', 'r') as f:
        data = json.load(f)

    ranking = sorted(
        data.items(),
        key=lambda x: x[1].get("scores", 0),
        reverse=True
    )

    lines = []
 #   lines.append(u"===== 前十名积分排行榜 (用 name_html 纯文本名) =====")

    for rank, (account_id, info) in enumerate(ranking[:10], start=1):
        raw_name = info.get("name_html", u"未知")
        name = clean_name(raw_name)
        # name 可能是unicode或str，统一转unicode
        if isinstance(name, str):
            name = name.decode('utf-8')
        scores = info.get("scores", 0)
        lines.append(u"%d. %s — 分数: %d" % (rank, name, scores))

    # 返回一个unicode字符串，换行分割
    return u"\n".join(lines)




def get_account_id_by_clientid(clientID):
    session = bs.getSession()
    for player in session.players:
        try:
            if player.getInputDevice().getClientID() == clientID:
                return player.get_account_id()
        except Exception as e:
            bs.screenMessage('Error: %s' % e)
    return None


def _parse_cmd(msg):
    clean = (msg or '').strip()
    if clean == '':
        return '', []
    parts = clean.split()
    return parts[0], parts[1:]


def _handle_legacy_passthrough(clientID, args, raw):
    # Keep legacy behavior for commands not yet fully rewritten.
    c.opt(clientID, raw)
    return True


_REGISTRY_HANDLERS = {}


def _init_registry_handlers():
    ctx = {
        'c': c,
        'MID': MID,
        'mid_storage': mid_storage,
        '_help_msg': _help_msg,
        'print_top10': print_top10,
        'get_info': get_info,
        'get_account_id_by_clientid': get_account_id_by_clientid,
    }

    cmd_handlers_social.register(_REGISTRY_HANDLERS, ctx)
    cmd_handlers_admin.register(_REGISTRY_HANDLERS, ctx)
    cmd_handlers_gameplay.register(_REGISTRY_HANDLERS, ctx)
    cmd_handlers_system.register(_REGISTRY_HANDLERS, ctx)
    cmd_handlers_funcombat.register(_REGISTRY_HANDLERS, ctx)

    # Route all known commands through dispatcher.
    for cmd in ALL_KNOWN_COMMANDS:
        if cmd not in COMMANDS:
            COMMANDS[cmd] = {'role': 'any', 'min_args': 0}
        if cmd not in _REGISTRY_HANDLERS:
            _REGISTRY_HANDLERS[cmd] = _handle_legacy_passthrough


_init_registry_handlers()


def _dispatch_registry_command(clientID, msg):
    cmd, args = _parse_cmd(msg)
    if cmd == '':
        return True

    handler = _REGISTRY_HANDLERS.get(cmd)
    if handler is None:
        return False

    try:
        # Chat callbacks run in UI context; many gameplay APIs require an
        # activity/session context. Route handler execution through the current
        # foreground host activity when available.
        activity = bsInternal._getForegroundHostActivity()
        if activity is not None:
            with bs.Context(activity):
                return bool(handler(clientID, args, msg))
        else:
            return bool(handler(clientID, args, msg))
    except Exception:
        bs.printException('registry handler failed: ' + cmd)
        bs.screenMessage('命令执行失败', color=(1, 0, 0), clients=[clientID], transient=True)
        return True


#for help contact mr.smoothy#5824 on discord