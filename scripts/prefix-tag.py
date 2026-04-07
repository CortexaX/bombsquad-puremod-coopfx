import time

import bs
from bsSpaz import *
import bsSpaz
import bsUtils
import random
import bsInternal
import membersID as MID
import threading
import json
import os
import rank


reload(rank)
class PermissionEffect(object):
    def __init__(self,position = (0,2,0),owner = None,kd=0.0,prefix = 'smoothy',prefixColor = (1,1,1),prefixAnim = {0:(1,1,1),500:(0.5,0.5,0.5)},prefixAnimate = True,particles = False,xyz=(0, 1.5, 0)):
        self.position = position
        self.owner = owner




        def a():
            self.emit()

        #particles
        if particles:
            self.timer = bs.Timer(10,bs.Call(a),repeat = True)

        #prefix
        m = bs.newNode('math', owner=self.owner, attrs={'input1': xyz, 'operation': 'add'})
        self.owner.connectAttr('position', m, 'input2')


        # n = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1, 0), 'operation': 'add'})
        # self.owner.connectAttr('position', n, 'input2')

        self._Text = bs.newNode('text',
                                      owner=self.owner,
                                      attrs={'text':prefix, #prefix text
                                             'inWorld':True,
                                             'shadow':1.2,
                                             'flatness':1.0,
                                             'color':prefixColor,
                                             'scale':0.0,
                                             'hAlign':'center'})
        # self._kd = bs.newNode('text',
        #                               owner=self.owner,
        #                               attrs={'text':'AYUSH', #prefix text
        #                                      'inWorld':True,
        #                                      'shadow':1.2,
        #                                      'flatness':1.0,
        #                                      'color':(0,2,1),
        #                                      'scale':0.0,
        #                                      'hAlign':'center'})

        m.connectAttr('output', self._Text, 'position')
        # n.connectAttr('output', self._kd, 'position')

        bs.animate(self._Text, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn

        #animate prefix
        if prefixAnimate:
            bsUtils.animateArray(self._Text, 'color',3, prefixAnim,True) #animate prefix color

    def emit(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0]-0.25+random.random()*0.5,self.owner.torsoPosition[1]-0.25+random.random()*0.5,self.owner.torsoPosition[2]-0.25+random.random()*0.5),
                              velocity=((-vel+(random.random()*(vel*2)))+self.owner.velocity[0]*2,(-vel+(random.random()*(vel*2)))+self.owner.velocity[1]*4,(-vel+(random.random()*(vel*2)))+self.owner.velocity[2]*2),
                              count=10,
                              scale=0.3+random.random()*1.1,
                              spread=0.1,
                              chunkType='sweat')
                              #emitType = 'stickers')
class kdpronoobtag(object):
    def __init__(self,position = (0,2,0),owner = None,kd=0.0,kills=0,prefix = ' ',prefixColor = (1,1,1),prefixAnim = {0:(1,1,1),500:(0.5,0.5,0.5)},prefixAnimate = False,particles = True):
        self.position = position
        self.owner = owner

        return


        def a():
            self.emit()

        #particles
        if kd>1.1:
            self.timer = bs.Timer(10,bs.Call(a),repeat = True)

        #prefix
        m = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.8, 0), 'operation': 'add'})
        self.owner.connectAttr('position', m, 'input2')
        if kd>1.1:      #customize here the criteria for being noob or pro     like change to kd>0.7  or kd>2.0 or making it more tough
            prefix='PRO!'
            prefixColor=(0,1,0)
        if kd<0.2:
            prefix='NOOB!'
            prefixColor=(1,0,0)
	if kills==0:
	    prefix='New'
	    prefixColor=(0,0,1)
        # n = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1, 0), 'operation': 'add'})
        # self.owner.connectAttr('position', n, 'input2')

        self._Text = bs.newNode('text',
                                      owner=self.owner,
                                      attrs={'text':prefix, #prefix text
                                             'inWorld':True,
                                             'shadow':0.7,
                                             'flatness':1.0,
                                             'color':prefixColor,
                                             'scale':0.2,
                                             'hAlign':'center'})


        m.connectAttr('output', self._Text, 'position')
        # n.connectAttr('output', self._kd, 'position')

        bs.animate(self._Text, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn

        #animate prefix
        if prefixAnimate:
            bsUtils.animateArray(self._Text, 'color',3, prefixAnim,True) #animate prefix color

    def emit(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0]-0.25+random.random()*0.5,self.owner.torsoPosition[1]-0.25+random.random()*0.5,self.owner.torsoPosition[2]-0.25+random.random()*0.5),
                              velocity=((-vel+(random.random()*(vel*2)))+self.owner.velocity[0]*2,(-vel+(random.random()*(vel*2)))+self.owner.velocity[1]*4,(-vel+(random.random()*(vel*2)))+self.owner.velocity[2]*2),
                              count=10,
                              scale=0.3+random.random()*1.1,
                              spread=0.2,
                              chunkType='sweat')
                              #emitType = 'stickers')


class kdtag(object):
    def __init__(self,position = (0,2,0),owner = None,kd=0.0,prefix = 'smoothy',prefixColor = (1,1,1),prefixAnim = {0:(1,1,1),500:(0.5,0.5,0.5)},prefixAnimate = False,particles = False):
        self.position = position
        self.owner = owner



        return


        #particles
        if particles:
            self.timer = bs.Timer(10,bs.Call(a),repeat = True)

        #prefix
        n = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.3, 0), 'operation': 'add'})
        self.owner.connectAttr('position', n, 'input2')




        self._Text = bs.newNode('text',
                                      owner=self.owner,
                                      attrs={'text':" K.D:"+str(kd), #prefix text
                                             'inWorld':True,
                                             'shadow':0.7,
                                             'flatness':1.0,
                                             'color':prefixColor,
                                             'scale':-0.8,
                                             'hAlign':'center'})


        n.connectAttr('output', self._Text, 'position')
        self._Text.scale = 0.01

        bs.animate(self._Text, 'scale', {0: 0.0, 1: 0.01})


        #animate prefix
        if prefixAnimate:
            bsUtils.animateArray(self._Text, 'color',3, prefixAnim,True) #animate prefix color



class ranktag(object):

    def __init__(self,position = (0,2,0),owner = None,prank=0,prefix = 'smoothy',prefixColor = (1,1,1),prefixAnim = {0:(1,1,1),500:(0.5,0.5,0.5)},prefixAnimate = False,particles = False):

        self.position = position
        self.owner = owner
        self.prank=prank
        self.type='spark'
        #prefix
        n = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.3, 0), 'operation': 'add'})
        self.owner.connectAttr('position', n, 'input2')


        self._Text = bs.newNode('text',
                                      owner=self.owner,
                                      attrs={'text':" #"+str(prank), #prefix text
                                             'inWorld':True,
                                             'shadow':0,
                                             'flatness':0,
                                             'color':prefixColor,
                                             'scale':0.0,
                                             'hAlign':'center'})


        n.connectAttr('output', self._Text, 'position')


        bs.animate(self._Text, 'scale', {0: 0.0, 1: 0.01}) #smooth prefix spawn

        #animate prefix
        if prefixAnimate:
            bsUtils.animateArray(self._Text, 'color',3, prefixAnim,True) #animate prefix color
        self._top5()
        self._top5_particles()



    def _top5(self):
        if self.prank<=5:
            n = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.5, 0), 'operation': 'add'})
            self.owner.connectAttr('position', n, 'input2')

            self._Text = bs.newNode('text',
                                    owner=self.owner,
                                    attrs={'text': " top5",  # prefix text
                                           'inWorld': True,
                                           'shadow': 0,
                                           'flatness': 0,
                                           'color': (1,1,1),
                                           'scale': 0.0,
                                           'hAlign': 'center'})

            n.connectAttr('output', self._Text, 'position')

            bs.animate(self._Text, 'scale', {0: 0.0, 1: 0.01})  # smooth prefix spawn
            bsUtils.animateArray(self._Text, 'color', 3, {0: (random.random(),random.random(),random.random()), 250: (random.random(),random.random(),random.random()),250*2:(random.random(),random.random(),random.random()),250*3:(random.random(),random.random(),random.random())}, True)  # animate prefix color
    def _top5_particles(self):

        if self.prank==1:

            self.timer = bs.Timer(10, bs.Call(self.emit_ice_metal), repeat=True)

            self.addLightColor((0.529, 0.804, 0.98))


        elif self.prank==2:
            self.type = 'ice'
            self.timer = bs.Timer(10, bs.Call(self.emit), repeat=True)
            self.addLightColor((0.529, 0.804, 0.98))
        elif self.prank==3:
            self.type = 'metal'
            self.timer = bs.Timer(10, bs.Call(self.emit), repeat=True)
            self.addLightColor((1, 0.1, 0.1))
        elif self.prank==4:
            self.timer = bs.Timer(10, bs.Call(self.emit_box_slime), repeat=True)
        elif self.prank==5:
            self.type = 'spark'
            self.timer = bs.Timer(10, bs.Call(self.emit), repeat=True)
            self.addLightColor((random.random(), random.random(), random.random()))
        elif self.prank==6:

            self.timer = bs.Timer(10, bs.Call(self.emit_smoke), repeat=True)

    @classmethod
    def getFactory(cls):
        """
        Returns a shared bs.BombFactory object, creating it if necessary.
        """
        activity = bs.getActivity()
        try:
            return activity._sharedBombFactory
        except Exception:
            f = activity._sharedBombFactory = BombFactory()
            return f

    def bomb_on_head(self,position=(0, 1, 0), velocity=(0, 0, 0),):
        factory = self.getFactory()
        materials = (factory.bombMaterial,
                     bs.getSharedObject('objectMaterial'))
        materials = materials + (factory.impactBlastMaterial,)
        if self.owner.exists():



            n = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 2.5, 0), 'operation': 'add'})
            self.owner.connectAttr('position', n, 'input2')
            m = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'model': factory.iceMineModel,
                'lightModel': factory.iceMineModel,
                'body': 'landMine',
                'shadowSize': 0.44,
                'colorTexture': factory.iceMineTex,
                'reflection': 'powerup',
                'reflectionScale': [1.0],
                'materials': materials})
            n.connectAttr('output', m, 'position')

    def addLightColor(self,color=(1, 1, 1)):

        n = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 0, 0), 'operation': 'add'})
        self.owner.connectAttr('position', n, 'input2')

        self.light = bs.newNode("light", owner=self.owner,attrs={"color": color,
                                                "heightAttenuated": False,
                                                "radius": 0.06})

        n.connectAttr('output',  self.light, 'position')

      #  bs.animate( self.light, 'scale', {0: 0.0, 1: 0.01})  # smooth prefix spawn

    def emit(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0]-0.25+random.random()*0.5,self.owner.torsoPosition[1]-0.25+random.random()*0.5,self.owner.torsoPosition[2]-0.25+random.random()*0.5),
                              velocity=((-vel+(random.random()*(vel*2)))+self.owner.velocity[0]*2,(-vel+(random.random()*(vel*2)))+self.owner.velocity[1]*4,(-vel+(random.random()*(vel*2)))+self.owner.velocity[2]*2),
                              count=10,
                              scale=0.3+random.random()*1.1,
                              spread=0.2,
                              chunkType=self.type)
                              #emitType = 'stickers')

    def emit_ice_metal(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0]-0.25+random.random()*0.5,self.owner.torsoPosition[1]-0.25+random.random()*0.5,self.owner.torsoPosition[2]-0.25+random.random()*0.5),
                              velocity=((-vel+(random.random()*(vel*2)))+self.owner.velocity[0]*2,(-vel+(random.random()*(vel*2)))+self.owner.velocity[1]*4,(-vel+(random.random()*(vel*2)))+self.owner.velocity[2]*2),
                              count=10,
                              scale=0.3+random.random()*1.1,
                              spread=0.2,
                              chunkType=random.choice(['ice','metal']))
    def emit_box_slime(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0]-0.25+random.random()*0.5,self.owner.torsoPosition[1]-0.25+random.random()*0.5,self.owner.torsoPosition[2]-0.25+random.random()*0.5),
                              velocity=((-vel+(random.random()*(vel*2)))+self.owner.velocity[0]*2,(-vel+(random.random()*(vel*2)))+self.owner.velocity[1]*4,(-vel+(random.random()*(vel*2)))+self.owner.velocity[2]*2),
                              count=10,
                              scale=0.3+random.random()*1.1,
                              spread=0.2,
                              chunkType=random.choice(['splinter','slime']))
    def emit_smoke(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0]-0.25+random.random()*0.5,self.owner.torsoPosition[1]-0.25+random.random()*0.5,self.owner.torsoPosition[2]-0.25+random.random()*0.5),
                              velocity=((-vel+(random.random()*(vel*2)))+self.owner.velocity[0]*2,(-vel+(random.random()*(vel*2)))+self.owner.velocity[1]*4,(-vel+(random.random()*(vel*2)))+self.owner.velocity[2]*2),
                              count=int(1.0+random.random()*4),
                              scale=0.5,
                              spread=0.1,
                              emitType='tendrils',tendrilType='smoke')
_JSON_CACHE = {}
_JSON_CACHE_TS = {}


def _load_json_cached(path, default_data=None, cache_ttl=1.0):
    if default_data is None:
        default_data = {}

    now = time.time()
    last = _JSON_CACHE_TS.get(path, 0.0)
    if (now - last) < cache_ttl and path in _JSON_CACHE:
        return _JSON_CACHE[path]

    data = default_data
    if os.path.exists(path):
        try:
            with open(path) as f:
                loaded = json.loads(f.read())
            if isinstance(loaded, dict):
                data = loaded
        except Exception as e:
            print e
            data = default_data

    _JSON_CACHE[path] = data
    _JSON_CACHE_TS[path] = now
    return data


def custom_tag():
    return _load_json_cached('tag.json', {}, cache_ttl=0.5)

def __init__(self,color=(1,1,1),highlight=(0.5,0.5,0.5),character="Spaz",player=None,powerupsExpire=True):
        """
        Create a spaz for the provided bs.Player.
        Note: this does not wire up any controls;
        you must call connectControlsToPlayer() to do so.
        """
        #https://github.com/imayushsaini/Bombsquad-Mr.Smoothy-Admin-Powerup-Server
        # convert None to an empty player-ref


        if player is None: player = bs.Player(None)



        Spaz.__init__(self,color=color,highlight=highlight,character=character,sourcePlayer=player,startInvincible=True,powerupsExpire=powerupsExpire)
        self.lastPlayerAttackedBy = None # FIXME - should use empty player ref
        self.lastAttackedTime = 0
        self.lastAttackedType = None
        self.heldCount = 0
        self.lastPlayerHeldBy = None # FIXME - should use empty player ref here
        self._player = player
        self._player_color = self._player.getIcon()['tintColor']


        profiles = []
        profiles = self._player.getInputDevice()._getPlayerProfiles()

        cName=player.getName()


        clID = self._player.getInputDevice().getClientID()






        cl_str = []


        if cName[0]==' ' or cName=='':
            bsInternal._disconnectClient(int(player.getInputDevice().getClientID()))
            bsInternal._chatMessage("No white Space Name Allowed")
            bsInternal._chatMessage("kicking"+cl_str)

        playeraccountid=str(self._player.get_account_id())
        stats = _load_json_cached('stats2.json', {}, cache_ttl=1.0)
        if playeraccountid not in stats:
            killed=1
            kills=0
        else:
        	killed=stats[playeraccountid]['killed']
     		kills=stats[playeraccountid]['kills']
     		if(killed==0):
     			killed=1
     	kd=kills/round(killed,1)
     	kd=round(kd,3)
      	ranked=False
     	#print("kill",kills,"killed",killed,"kd",round(kd,3))

        ##v
        if profiles == [] or profiles == {}:
            profiles = bs.getConfig()['Player Profiles']
        reload(rank)
        if playeraccountid in rank.player:

          prank=rank.player.index(playeraccountid)+1
          ranked=True

        for p in profiles:
            try:
		if ranked:
		    ranktag(owner = self.node,prank=prank,prefix = " ",prefixAnim = {0: (0.85,0.852,0.85), 250: (0.59,0.598,0),250*2:(0.75,1,0),250*3:(0.9,0.17,0.028)},prefixAnimate =False, particles = False,prefixColor=self._player_color)
                kdpronoobtag(owner = self.node,kd=kd,kills=kills,prefix = " ",prefixAnim = {0: (0.85,0.852,0.85), 250: (0.59,0.598,0),250*2:(0.75,1,0),250*3:(0.9,0.17,0.028)},prefixAnimate =False, particles = False)
            	kdtag(owner = self.node,kd=kd,prefix = " ",prefixAnim = {0: (0.85,0.852,0.85), 250: (0.59,0.598,0),250*2:(0.75,1,0),250*3:(0.9,0.17,0.028)},prefixAnimate =False, particles = False)



                #if playeraccountid in MID.smoothy:
               #     PermissionEffect(owner = self.node,prefix = u'\ue048 Smoothy  \ue048',prefixAnim = {0: (0.5,0.011,0.605), 250: (1,0.411,0.3411),250*2:(1,0.591,0.811),250*3:(0.829,0.331,0.403)})
             #       break
                # do same to add more custom tags to owners or someone ..

                tag=custom_tag()
                if playeraccountid in tag:
                    if tag[playeraccountid]!=None:
                        PermissionEffect(owner=self.node, kd=kd, prefix=tag[playeraccountid],xyz=(0, 1.75, 0),
                                         prefixAnim={0: (random.random(),random.random(),random.random()), 250: (random.random(),random.random(),random.random()),250*2:(random.random(),random.random(),random.random()),250*3:(random.random(),random.random(),random.random())})
                        break
                if playeraccountid in MID.admins:
                    PermissionEffect(owner = self.node,kd=kd,prefix = u'\ue048 A.D.M.I.N \ue048',prefixAnim = {0: (0.5,0.011,0.605), 250: (1,0.411,0.3411),250*2:(1,0.591,0.811),250*3:(0.829,0.331,0.403)})
                    break
                if playeraccountid in MID.vips:
                    PermissionEffect(owner = self.node,kd=kd,prefix = u'\ue043 VIP \ue043',prefixAnim = {0: (0.9,0.611,0.705), 250: (1,0.311,0.5411),250*2:(0.7,0.591,0.811),250*3:(0.729,0.431,0.703)})
                    break

                if playeraccountid in MID.members:
                    PermissionEffect(owner = self.node,kd=kd,prefix = u" MEMBER ",prefixAnim = {0: (0.85,0.852,0.85), 250: (0.59,0.598,0),250*2:(0.75,1,0),250*3:(0.9,0.17,0.028)})
                    break
                #you can give  custom tag to anyone without giving any command permision
                # if playeraccountid in MID.anyname:
                #     PermissionEffect(owner = self.node,kd=kd,prefix = u" anyname ",prefixAnim = {0: (0.85,0.852,0.85), 250: (0.59,0.598,0),250*2:(0.75,1,0),250*3:(0.9,0.17,0.028)})
                #     break



            except Exception as e:
                import traceback
                print traceback.format_exc()

        # grab the node for this player and wire it to follow our spaz (so players' controllers know where to draw their guides, etc)
        if player.exists():
            playerNode = bs.getActivity()._getPlayerNode(player)
            self.node.connectAttr('torsoPosition',playerNode,'position')



bsSpaz.PlayerSpaz.__init__ = __init__




