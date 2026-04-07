# -*- coding: utf-8 -*-
import bs
import bsUtils
import bsPowerup
import random


def bsGetAPIVersion():
    return 4


def bsGetGames():
    return [DoubleFinalLastStandGame]


def bsGetLevels():
    # 关键：这里的 Level 内部唯一名决定排行榜分桶（全球榜按它区分）
    return [bs.Level(
        'Double Final Last Stand Ranked',
        displayName='${GAME}',
        gameType=DoubleFinalLastStandGame,
        settings={},
        previewTexName='rampagePreview')]


class DoubleFinalLastStandGame(bs.CoopGameActivity):

    tips = ['This level never ends, but a high score here\n'
            'will earn you eternal respect throughout the world.']

    @classmethod
    def getName(cls):
        return u'双倍最终杀敌战'

    @classmethod
    def getDescription(cls, sessionType):
        return u'在最后的荣耀史诗级慢动作大战中战斗至死!'

    def __init__(self, settings={}):
        settings['map'] = 'Rampage'
        bs.CoopGameActivity.__init__(self, settings)

        self.announcePlayerDeaths = True
        self._isSlowMotion = True

        self._newWaveSound = bs.getSound('scoreHit01')
        self._spawnCenter = (0, 5.5, -4.14)
        self._tntSpawnPosition = (0, 5.5, -6)
        self._powerupCenter = (0, 7, -4.14)
        self._powerupSpread = (7, 2)

        self._excludePowerups = []

        # 与原版同类，但会在 _startBotUpdates 里把刷新速度翻倍
        self._botSpawnTypes = {
            bs.BomberBot: [1.0, 0.0, 0.0],
            bs.BomberBotPro: [0.0, 0.05, 0.001],
            bs.BomberBotProShielded: [0.0, 0.02, 0.002],
            bs.ToughGuyBot: [1.0, 0.0, 0.0],
            bs.ToughGuyBotPro: [0.0, 0.05, 0.001],
            bs.ToughGuyBotProShielded: [0.0, 0.02, 0.002],
            bs.ChickBot: [0.3, 0.0, 0.0],
            bs.ChickBotPro: [0.0, 0.05, 0.001],
            bs.ChickBotProShielded: [0.0, 0.02, 0.002],
            bs.NinjaBot: [0.3, 0.05, 0.0],
            bs.MelBot: [0.1, 0.03, 0.001],
            bs.PirateBot: [0.05, 0.02, 0.002]
        }

    def onTransitionIn(self):
        bs.CoopGameActivity.onTransitionIn(self, music='Epic')
        bs.gameTimer(1300, bs.Call(bs.playSound, self._newWaveSound))
        self._scoreBoard = bs.ScoreBoard(label=bs.Lstr(resource='scoreText'), scoreSplit=0.5)
        self._score = bs.SecureInt(0)

    def onBegin(self):
        bs.CoopGameActivity.onBegin(self)
        self._dropPowerups(standardPoints=True)
        bs.gameTimer(2000, bs.WeakCall(self._startPowerupDrops))
        bs.gameTimer(1, bs.WeakCall(self._startBotUpdates))
        self.setupLowLifeWarningSound()
        self._updateScores()
        self._bots = bs.BotSet()
        self._dingSound = bs.getSound('dingSmall')
        self._dingSoundHigh = bs.getSound('dingSmallHigh')
        self._tntSpawner = bs.TNTSpawner(position=self._tntSpawnPosition, respawnTime=10000)
        # 连杀追踪: {playerKey: {'count': int, 'last': gameTimeMs}}
        self._killStreak = {}

    def spawnPlayer(self, player):
        pos = (self._spawnCenter[0] + random.uniform(-1.5, 1.5),
               self._spawnCenter[1],
               self._spawnCenter[2] + random.uniform(-1.5, 1.5))
        self.spawnPlayerSpaz(player, position=pos)

    def _startBotUpdates(self):
        # 双倍最终杀敌战：刷新速度 x2
        base = 3300 - 300 * (len(self.players))
        self._botUpdateInterval = max(500, int(base * 0.5))

        # 但第二波延后几秒，避免一口气全压上来
        self._updateBots()
        bs.gameTimer(2500, bs.WeakCall(self._updateBots))
        if len(self.players) > 2:
            bs.gameTimer(3800, bs.WeakCall(self._updateBots))
        if len(self.players) > 3:
            bs.gameTimer(5000, bs.WeakCall(self._updateBots))

        self._botUpdateTimer = bs.Timer(int(self._botUpdateInterval), bs.WeakCall(self._updateBots))

    def _dropPowerup(self, index, powerupType=None):
        if powerupType is None:
            powerupType = bsPowerup.Powerup.getFactory().getRandomPowerupType(excludeTypes=self._excludePowerups)
        bsPowerup.Powerup(position=self.getMap().powerupSpawnPoints[index], powerupType=powerupType).autoRetain()

    def _startPowerupDrops(self):
        self._powerupDropTimer = bs.Timer(3000, bs.WeakCall(self._dropPowerups), repeat=True)

    def _dropPowerups(self, standardPoints=False, forceFirst=None):
        if standardPoints:
            pts = self.getMap().powerupSpawnPoints
            for i, _pt in enumerate(pts):
                bs.gameTimer(1000 + i * 500,
                             bs.WeakCall(self._dropPowerup, i, forceFirst if i == 0 else None))
        else:
            pt = (self._powerupCenter[0] + random.uniform(-1.0 * self._powerupSpread[0], 1.0 * self._powerupSpread[0]),
                  self._powerupCenter[1],
                  self._powerupCenter[2] + random.uniform(-self._powerupSpread[1], self._powerupSpread[1]))
            bsPowerup.Powerup(position=pt,
                       powerupType=bsPowerup.Powerup.getFactory().getRandomPowerupType(excludeTypes=self._excludePowerups)).autoRetain()

    def _updateBots(self):
        self._botUpdateInterval = max(500, self._botUpdateInterval * 0.98)
        self._botUpdateTimer = bs.Timer(int(self._botUpdateInterval), bs.WeakCall(self._updateBots))

        botSpawnPoints = [[-5, 5.5, -4.14], [0, 5.5, -4.14], [5, 5.5, -4.14]]
        dists = [0, 0, 0]
        playerPts = []
        for player in self.players:
            try:
                if player.isAlive():
                    playerPts.append(player.actor.node.position)
            except Exception, e:
                print 'EXC in _updateBots', e

        for i in range(3):
            for p in playerPts:
                dists[i] += abs(p[0] - botSpawnPoints[i][0])
            dists[i] += random.random() * 5.0

        if dists[0] > dists[1] and dists[0] > dists[2]:
            pt = botSpawnPoints[0]
        elif dists[1] > dists[2]:
            pt = botSpawnPoints[1]
        else:
            pt = botSpawnPoints[2]

        pt = (pt[0] + 3.0 * (random.random() - 0.5),
              pt[1],
              2.0 * (random.random() - 0.5) + pt[2])

        total = 0.0
        for t in self._botSpawnTypes.items():
            total += t[1][0]
        r = random.random() * total

        total = 0
        for t in self._botSpawnTypes.items():
            total += t[1][0]
            if r <= total:
                spazType = t[0]
                break

        self._bots.spawnBot(spazType, pos=pt, spawnTime=1000)

        for t in self._botSpawnTypes.items():
            t[1][0] += t[1][1]
            t[1][1] += t[1][2]

    def _updateScores(self):
        self._scoreBoard.setTeamValue(self.teams[0], self._score.get(), maxScore=None)

    def _spawn_bot_fireworks(self, pos):
        # 击杀 bot 后烟花特效（纯视觉）
        if pos is None:
            return
        for _i in range(3):
            v = (random.uniform(-6, 6), random.uniform(3, 10), random.uniform(-6, 6))
            bs.emitBGDynamics(position=pos, velocity=v, count=35,
                              scale=1.2, spread=0.4, chunkType='spark')
        l = bs.newNode('light', attrs={'position': pos, 'heightAttenuated': False,
                                       'radius': 0.2, 'color': (1.2, 0.8, 0.2)})
        bsUtils.animate(l, 'intensity', {0: 0, 80: 1.8, 280: 0})
        bsUtils.animate(l, 'radius', {0: 0.2, 120: 1.8, 320: 0.2})
        bs.gameTimer(350, l.delete)

    def _do_mega_streak_blast(self, pos, killerPlayer):
        # 五连杀特效：超大爆炸 + 闪电，但对玩家无效（仅打 bot）
        if pos is None:
            return

        # 视觉大爆炸（纯特效，避免使用 explosion node 触发旧引擎半径伤害路径）
        for _i in range(4):
            bs.emitBGDynamics(position=pos,
                              velocity=(random.uniform(-2, 2), random.uniform(0.5, 3.5), random.uniform(-2, 2)),
                              count=40, scale=2.0, spread=1.0, chunkType='spark')
        bs.emitBGDynamics(position=pos, velocity=(0, 1, 0), count=90,
                          scale=1.8, spread=0.9, chunkType='rock')

        # 闪电感（瞬时强光）
        light = bs.newNode('light', attrs={'position': pos, 'heightAttenuated': False,
                                           'radius': 0.1, 'color': (0.7, 0.8, 1.6)})
        bsUtils.animate(light, 'intensity', {0: 0, 30: 6.0, 80: 0.0, 110: 4.0, 170: 0.0})
        bsUtils.animate(light, 'radius', {0: 0.1, 30: 6.0, 170: 0.1})
        bs.gameTimer(220, light.delete)
        bs.shakeCamera(6.0)

        # 只伤 bot，不伤玩家；范围约两倍 TNT，伤害近似双倍 TNT
        radius = 5.8
        for b in self._bots.getLivingBots():
            try:
                if not b.exists() or not b.isAlive():
                    continue
                p = b.node.position
                dx = p[0] - pos[0]
                dy = p[1] - pos[1]
                dz = p[2] - pos[2]
                dist2 = dx * dx + dy * dy + dz * dz
                if dist2 > radius * radius:
                    continue
                # engine-stable bot-only impulse/hit (avoid radius>0 + vmag crash on 1.4)
                b.node.handleMessage(bs.HitMessage(
                    pos=pos,
                    velocity=(dx * 1.8, max(2.0, dy * 1.2 + 3.0), dz * 1.8),
                    magnitude=4200,
                    velocityMagnitude=0,
                    radius=0,
                    srcNode=None,
                    sourcePlayer=killerPlayer,
                    forceDirection=(dx, 0.5, dz),
                    hitType='explosion',
                    hitSubType='megaStreak'))
            except Exception:
                pass

    def doEnd(self, outcome):
        if outcome == 'defeat':
            self.fadeToRed()
        # 关键：coop + score + playerInfo 会接到在线分数系统
        self.end(delay=2000, results={
            'outcome': outcome,
            'score': self._score.get(),
            'playerInfo': self.initialPlayerInfo
        })

    def handleMessage(self, m):
        if isinstance(m, bs.PlayerSpazDeathMessage):
            player = m.spaz.getPlayer()
            if player is None:
                bs.printError('FIXME: getPlayer() should no longer ever be returning None')
                return
            if not player.exists():
                return
            self.scoreSet.playerLostSpaz(player)
            bs.gameTimer(100, self._checkRoundOver)

        elif isinstance(m, bs.PlayerScoredMessage):
            self._score.add(m.score)
            self._updateScores()

        elif isinstance(m, bs.SpazBotDeathMessage):
            pts, importance = m.badGuy.getDeathPoints(m.how)
            try:
                target = m.badGuy.node.position
            except Exception:
                target = None

            # 打死 bot 放烟花
            self._spawn_bot_fireworks(target)

            if m.killerPlayer is not None and m.killerPlayer.exists():
                try:
                    self.scoreSet.playerScored(m.killerPlayer, pts, target=target, kill=True,
                                               screenMessage=False, importance=importance)
                    bs.playSound(self._dingSound if importance == 1 else self._dingSoundHigh, volume=0.6)
                except Exception, e:
                    print 'EXC on last-stand SpazBotDeathMessage', e

                # 五连杀触发特大爆炸(仅对bot有效)
                k = str(id(m.killerPlayer))
                now = bs.getGameTime()
                info = self._killStreak.get(k, {'count': 0, 'last': 0})
                if now - info['last'] <= 5000:
                    info['count'] += 1
                else:
                    info['count'] = 1
                info['last'] = now
                if info['count'] >= 5:
                    info['count'] = 0
                    self._do_mega_streak_blast(target, m.killerPlayer)
                self._killStreak[k] = info
            else:
                self._score.add(pts)

            self._updateScores()
        else:
            super(DoubleFinalLastStandGame, self).handleMessage(m)

    def _onGotScoresToBeat(self, scores):
        self._showStandardScoresToBeatUI(scores)

    def endGame(self):
        self._bots.finalCelebrate()
        bs.gameTimer(1, bs.WeakCall(self.doEnd, 'defeat'))
        bs.playMusic(None)

    def _checkRoundOver(self):
        if not any(player.isAlive() for player in self.teams[0].players):
            self.endGame()
