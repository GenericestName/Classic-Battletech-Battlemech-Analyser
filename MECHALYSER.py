import random, math, pathlib, copy, time, os
from natsort import natsorted
from statistics import mean, median
from statistics import stdev
from math import floor
import statistics
StartTime = time.time()


def dooverflow(part, target=None):
    # print(f"Overflowing from {part.name}")
    if part is target.hd:
        if target.causeofdeath == "":target.causeofdeath = "HKill"
        return "Mech Destroyed"
    elif part.name.lower()[-2] == "l":
        if part is target.lt:
            return target.ct
        elif part is target.ll or part is target.la:
            return target.lt
    elif part.name.lower()[-2] == "r":
        if part is target.rt:
            return target.ct
        elif part is target.rl or part is target.ra:
            return target.rt
    elif part is target.ct:
        if target.causeofdeath == "":target.causeofdeath = "CTKill"
        return "Mech Destroyed"
    else:
        print("OVERFLOW ERROR")
        return

def RollLocation(Float=False, HasCrit=False, Debug=False):
    Location = random.randint(1, 6) + random.randint(1, 6)
    if Location == 12:
        return "HD", HasCrit
    elif Location == 10 or Location == 11:
        return "LA", HasCrit
    elif Location == 9:
        return "LL", HasCrit
    elif Location == 8:
        return "LT", HasCrit
    elif Location == 7:
        return "CT", HasCrit
    elif Location == 6:
        return "RT", HasCrit
    elif Location == 5:
        return "RL", HasCrit
    elif Location == 4 or Location == 3:
        return "RA", HasCrit
    elif Location == 2:
        if not Float or Float and HasCrit:
            return "CT", HasCrit
        elif Float and not HasCrit:
            return RollLocation(False, True)

print(f"{time.time()}")



class Pilot:
    def __init__(self, name="Mechwarrior", pskill=5, gskill=4, isunconscious=False, hits=0):
        self.hits = hits
        self.pskill = pskill
        self.gskill = gskill
        self.name=name
        self.isunconscious = isunconscious
        self.isdead = False
    def DoPilotDamage(self):
        roll = random.randint(1, 6) + random.randint(1, 6)
        self.hits += 1
        if self.isdead == True:
            return "Pilot is already dead"
        elif self.isunconscious == True:
            if self.hits >= 6:
                self.isdead = True
                return "Dead"
            return "Eepy Seepy"
        if self.hits == 6:
            self.isdead = True
            return "Pilot is dead, mech destroyed"
        elif self.hits == 5 and roll < 11:
            self.isunconscious = True
        elif self.hits == 4 and roll < 10:
            self.isunconscious = True
        elif self.hits == 3 and roll < 7:
            self.isunconscious = True
        elif self.hits == 2 and roll < 5:
            self.isunconscious = True
        elif self.hits == 2 and roll < 3:
            self.isunconscious = True


def docriticals():
    Roll = random.randint(1, 6) + random.randint(1,6)
    if Roll >= 12:
        return 3
    elif Roll == 10 or Roll == 11:
        return 2
    elif Roll == 8 or Roll == 9:
        return 1
    else:
        return 0
class MechUtility:

    def __init__(self, name, slots=1, isdamaged=False, isengine=False, isgyro=False, ids=[]):
        self.name = name
        self.slots = slots
        self.ids = ids
        self.isdamaged = isdamaged
        self.hasexpanded = False
        self.isengine = isengine
        self.isgyro = isgyro
        self.owner = None

    def parthit(self, crit):
        self.isdamaged = True
        return

class Engine(MechUtility):
    def __init__(self, name, slots=1, isdamaged=False, isengine=False, ids=[], owner=None):
        self.name = name
        self.slots = slots
        self.ids = ids
        self.isdamaged = isdamaged
        self.hasexpanded = False
        self.isengine = isengine
        self.owner = owner

    def parthit(self, crit):
        if self.isdamaged:
            return
        self.isdamaged = True
        a = getattr(self.owner, "owner")
        #print(f"{a.name} suffered an engine hit!")
        num = getattr(a, "enginehits")
        num +=1
        setattr(a, "enginehits", num)
        if getattr(a, "enginehits") >= 3:
            setattr(a, "isdead", True)
            #print(a.name, "Fucking died!")
            return
        return

class HeatSink:
    def __init__(self, name, sinking = 1, slots = 1, isdamaged = False, ids=[]):
        self.name = name
        self.hasexpanded = False
        self.slots = slots
        self.ids = ids
        self.isdamaged = isdamaged
        self.sinking = sinking

    def parthit(self, crit):
        self.isdamaged = 0
        self.sinking = 0
        return

class JumpJet(MechUtility):
    def __init__(self, name, slots=1, ids=[], jumping=1):
        self.name = name
        self.slots = int(slots)
        self.isdamaged = False
        self.ids = ids
        self.jumping = int(jumping)

    def parthit(self, crit):
        self.isdamaged = True
        self.jumping = 0
        return

class AmmoBin(MechUtility):
    def __init__(self, name, ammonum, slots=1, isexplosive = True, damageperammo = 2, isdamaged=False, ids=[]):
        self.name = name
        self.slots = slots
        self.ammonum = int(ammonum)
        self.isdamaged = isdamaged
        self.ids = ids
        self.isexplosive = isexplosive
        self.damageperammo = damageperammo
        self.location = ()
    def parthit(self, crit):
        if self.isexplosive and not self.ammonum == 0 and crit and not self.isdamaged:
            explosiondamage = self.ammonum*self.damageperammo
            self.ammonum = 0
            self.isdamaged = True
            #print("BOOM!")
            return explosiondamage
        else:
            self.ammonum = 0
            self.isdamaged = True
            self.damageperammo = 0
            return 0
class MechPart:

    def __init__(self, name, armour, structure, slot1=None, slot2=None, slot3=None, slot4=None, slot5=None, slot6=None, isdestroyed=False, ishead=False):
        self.name = name
        self.armour = armour
        self.structure = int(structure)
        self.slot1 = slot1
        self.slot2 = slot2
        self.slot3 = slot3
        self.slot4 = slot4
        self.slot5 = slot5
        self.hasweps = False
        self.slot6 = slot6
        self.isdestroyed = isdestroyed
        self.ishead = ishead
        self.hasengine = False
        self.eslots = []
        self.blasters = []
        self.hasammo = False
        self.ammoslots = []
        self.hasjets = False
        self.jetslots = []
        self.qdir = list(a for a in dir(self) if not a.startswith('__'))
        self.slotqdir = natsorted(list(a for a in dir(self) if a.startswith("slot")))
        #self.multislot()
        self.listweps()
        self.slshit = []
        self.owner = None
        #selt.slotstents = list(for i in range(len(self.slotqdir)))

    def dopartdestruction(self):
        self.armour = 0
        self.structure = 0
        self.isdestroyed = True
        for i in self.slotqdir:
            i = getattr(self, i)
            if type(i) is str or i is None:
                continue
            i.parthit(False)
        #print("Engine Hit due to Torso Destruction!")


    def declareownership(self):
        for i in self.slotqdir:
            a = getattr(self, i)
            if hasattr(a, "owner"):
                setattr(a, "owner", self)
                #print(f"{self.name} declared {i} ({a}) as its babbie!")
    def listweps(self):
        for attr in self.slotqdir:
            attrvalue = getattr(self, attr)
            if isinstance(attrvalue, Weapon):
                self.blasters.append(attr)
                self.hasweps = True
            if isinstance(attrvalue, AmmoBin):
                #print(attrvalue.name)
                self.ammoslots.append(attr)
                self.hasammo = True
            if isinstance(attrvalue, JumpJet):
                self.jetslots.append(attr)
                self.hasjets = True
            if isinstance(attrvalue, Engine):
                self.hasengine = True
                attrvalue.owner = self
                self.eslots.append(attr)

    def multislot(self, newdic={}):
        #if isinstance(self, MechPartBig):
           # return
        slotsdic = {}
        overflowdic = {}
        for attr_name in self.slotqdir:
            if len(newdic)==0:
                attrvalue = (getattr(self, attr_name))
                if isinstance(attrvalue, Weapon) or isinstance(attrvalue, MechUtility) and getattr(attrvalue, "slots") > 1 and getattr(attrvalue, "hasexpanded", False):
                    #print(f"{attr_name} is {attrvalue.name}")
                    slotsdic[attr_name] = attrvalue.slots
        if not len(slotsdic) == 0:
            for key, value in slotsdic.items():
                slotnum = int(key[4:])
                sl = getattr(self, key)
                xp = getattr(sl, "hasexpanded")
                if xp:
                    continue
                for i in range((slotnum) + 1, slotnum + int(value)):
                    higherslotname = f"slot{i}"
                    try:
                        if getattr(self, higherslotname) == None or (getattr(self, higherslotname) == getattr(self, key) and not getattr(self, higherslotname)):
                            setattr(self, higherslotname, getattr(self, key))
                            attrvalue = getattr(self, higherslotname)
                            #wepsadded.append(attrvalue)
                            attrvalue.hasexpanded = True
                            #print(f"{higherslotname} of {self.name} is now bound to that {attrvalue}!")
                    except AttributeError:
                        o = slotnum+int(value)-1-len(self.slotqdir)
                        #print(o)
                        #
                        a = getattr(self, key)
                        #print(a)
                        overflowdic[a] = o
        if len(newdic) != 0:
            for key, value in newdic.items():
                slotstoadd = []
                for idx, attr in enumerate(self.slotqdir):
                    slotnum = idx+1
                    aval = getattr(self, attr)
                    if aval is None or (aval.name == key.name and aval != key):
                        for i in range(value):
                            add = f"slot{slotnum + i}"
                            if add not in slotstoadd:
                                slotstoadd.append(add)
                        break
                    else: continue
                for slot in slotstoadd:
                    setattr(self, slot, key)
                    a = getattr(self, slot)
                    setattr(a, "hasexpanded", True)

        return overflowdic


    def TakeDamage(self, dmg, hascrit=False, mekself=None):
        overspill = 0
        if dmg <= 0 or self.isdestroyed or self.owner.isdead:
            return 0
        if self.armour > 0:
            # print(f"{self.name} has {self.armour} armour left, and is taking {dmg} damage!")
            self.armour -= dmg
            if self.armour < 0:
                #print(f"Overspilling {abs(self.armour)} from {dmg} attack!")
                dmg = abs(self.armour)
                self.armour = 0
            else:
                return 0
        if self.armour <= 0:
            if self.structure <= 0:
                #print("Weird")
                if self.structure < 0:
                    #print("Weirder")
                    print(self.structure, dmg, self.name)
            self.structure -= dmg
            # print(f"{self.name} is taking {dmg} struc dmg!")
            #print(f"{self.name} took {dmg} structure damage!")
            critnum = int(docriticals())
            if self.structure > 0:
                if critnum > 0:
                    crit(self, critnum, mekself)
                return 0
            if self.structure == 0:
                self.isdestroyed = True
                if critnum > 0:
                    crit(self, critnum, mekself)
                return 0
            if self.structure < 0:
                dmg = abs(self.structure)
                self.isdestroyed = True
                if self is self.owner.hd or self is self.owner.ct:
                    self.isdestroyed = True
                    self.owner.isdead = True
                    return 0
                if critnum > 0:
                    crit(self, critnum, mekself)
                self.structure = 0
                #print(overspill)
                return dmg




class MechPartBig(MechPart):
    def __init__(self, name, armour, reararmour, structure, slot1=None, slot2=None, slot3=None, slot4=None, slot5=None, slot6=None, slot7=None, slot8=None, slot9=None, slot10=None, slot11=None, slot12=None):
        self.reararmour = reararmour
        self.name = name
        self.armour = armour
        self.structure = int(structure)
        self.slot1 = slot1
        self.slot2 = slot2
        self.slot3 = slot3
        self.slot4 = slot4
        self.slot5 = slot5
        self.slot6 = slot6
        self.isdestroyed = False
        self.slot7 = slot7
        self.slot8 = slot8
        self.slot9 = slot9
        self.slot10 = slot10
        self.slot11 = slot11
        self.slot12 = slot12
        self.blasters = []
        self.slshit = []
        self.hasammo = False
        self.ammoslots = []
        self.jetslots = []
        self.hasjets = False
        self.hasweps = False
        self.hasengine = False
        self.eslots = []
        self.qdir = list(a for a in dir(self) if not a.startswith('__'))
        self.slotqdir = list(a for a in dir(self) if a.startswith("slot"))
        self.slotqdir = natsorted(self.slotqdir)
        self.owner = None
        #self.multislot()
        #self.listweps()

    '''def multislot(self):
        slotsdic = {}
        for attr_name in dir(self):
            if not attr_name.startswith("__") and not attr_name == "structure":
                attrvalue = (getattr(self, attr_name))
                if isinstance(attrvalue, Weapon) and getattr(attrvalue, "slots") > 1 or isinstance(attrvalue, MechUtility) and getattr(attrvalue, "slots") > 1:
                    print(f"{attr_name} is {attrvalue.name}")
                    slotsdic[attr_name] = attrvalue.slots
        if not len(slotsdic) == 0:
            for key, value in slotsdic.items():
                slotnum = int(key[4:])
                for i in range((slotnum) + 1, slotnum + int(value)):
                    higherslotname = f"slot{i}"
                    if getattr(self, higherslotname) == None:
                        setattr(self, higherslotname, getattr(self, key))
                        attrvalue = getattr(self, higherslotname)
                        print(f"{higherslotname} of {self.name} is now bound to that {attrvalue.name}!")
        else:
            return

        )
        for i in range((slotnum)+1, slotnum+(int(attrvalue.slots))):
        higherslotname = f"slot{i}"
        if getattr(self, higherslotname) == None:
        exec(f"self.{higherslotname} = copy.copy(self.{attr_name})")
        print(f"{higherslotname} in {self.name} is now {attrvalue.name}!")'''
class Weapon(object):

    def __init__(self, name, srange, mrange, lrange, dmg, heat, damage_type = None, BV=0, slots=1, targetmod=0, minrange=0, isexplosive=False, xplodmg=0, ids=[]):
        self.name = name
        self.minrange = minrange
        self.srange = srange
        self.mrange = mrange
        self.lrange = lrange
        self.dmg = dmg
        self.hasexpanded = False
        self.heat = heat
        self.ratio = 0
        self.BV = BV
        self.slots = slots
        self.targetmod = targetmod
        self.damage_type = damage_type
        self.isexplosive = isexplosive
        self.hasfired = False
        self.ratiocalc(dmg, heat)
        self.isdamaged = False
        self.hit = False
        self.ids = ids
    
    def parthit(self, crit):
        self.dmg = 0
        if self.isexplosive and not self.isdamaged:
            self.isdamaged = True
            return self.xplodmg
        self.isdamaged = True
        if self.isexplosive and self.isdamaged:
            self.xplodmg = 0
            return self.xplodmg
    def shoot(self):
        if self.hasfired:
            #print("Fuc")
            return
        #print("PEW!")
        self.hasfired = True
        return self, self.heat
    def ratiocalc(self, dmg, heat):
        if not hasattr(self, "cluster"):
            try:
                self.ratio = (dmg/heat)+(dmg/100)
                return
            except ZeroDivisionError:
                self.ratio=0
        else:
            if getattr(self, "cluster") == 0 or getattr(self, "cluster") == None:
                try:
                    self.ratio = (dmg / heat)+(dmg/100)
                    return
                except ZeroDivisionError:
                    self.ratio = 0
            else:
                try:
                    self.ratio = (dmg*(self.cluster)/heat)+(dmg/100)
                    return
                except ZeroDivisionError:
                    self.ratio = 0
class Missile(Weapon):
    def __init__ (self, name, srange, mrange, lrange, dmg, heat, damage_type = None, BV=0, slots = 1, targetmod =0, minrange=0, ammo=None, cluster=None, clustermod = 0, grouping=None, streak=False, artemis4=False, artemis5=False, ids=None):
        super().__init__(name, srange, mrange, lrange, dmg, heat, damage_type, BV, slots, targetmod, minrange)
        if ids == None:
            self.ids = []
        self.artemis4 = artemis4
        self.minrange=minrange
        self.targetmod = targetmod
        self.slots = slots
        self.dmg = dmg
        self.srange = srange
        self.mrange =mrange
        self.lrange=lrange
        self.ammo = ammo
        self.artemis5 = artemis5
        self.hasexpanded = False
        self.streak = streak
        self.grouping = grouping
        self.cluster = cluster
        self.clustermod = clustermod
        self.hasfired = False
        self.ratiocalc(dmg, heat)
        self.isdamaged = False
        self.hit = False
        self.ids = ids

class Autocannon(Weapon):
    def __init__(self, name, srange, mrange, lrange, dmg, heat, damage_type = None, BV=0, slots=1, targetmod=0, minrange=0, ammo = None, cluster = None, isexplosive=False, xplodmg=0, grouping = None, ids=[]):
        self.name = name
        self.minrange = minrange
        self.srange = srange
        self.hasexpanded = False
        self.mrange = mrange
        self.lrange = lrange
        self.dmg = dmg
        self.heat = heat
        self.BV = BV
        self.slots = slots
        self.xplodmg = xplodmg
        self.targetmod = targetmod
        self.damage_type = damage_type
        self.isexplosive = isexplosive
        self.hasfired = False
        self.ammo = ammo
        self.cluster = cluster
        self.ratio=0
        self.ratiocalc(dmg, heat)
        self.isdamaged = False
        self.hit = False
        self.ids = ids
    def shoot(self):
        self.hasfired = True
        return self.dmg, self.ammo, self.cluster


class VariableWep(Weapon):
    def __init__(self, name, srange, mrange, lrange, dmg, heat, damage_type=None, BV=0, slots=1, targetmod=0, minrange=0, ammo=None, cluster=None, isexplosive=False, xplodmg=0, grouping=None, ids=[]):
        self.name = name
        self.minrange = minrange
        self.srange = srange
        self.hasexpanded = False
        self.mrange = mrange
        self.lrange = lrange
        self.dmg = dmg
        self.heat = heat
        self.BV = BV
        self.slots = slots
        self.xplodmg = xplodmg
        self.targetmod = targetmod
        self.damage_type = damage_type
        self.isexplosive = isexplosive
        self.hasfired = False
        self.ammo = ammo
        self.cluster = cluster
        self.ratio = 0
        self.ratiocalc(dmg, heat)
        self.isdamaged = False
        self.hit = False
        self.ids = ids
class Battlemech:
    def __init__(self, name, head, la, ra, ll, rl, rt, lt, ct, pilot, walkspeed, tonnage, case1=False, case2=False, doublesink=False, bv=0):
        self.name = name
        self.hd = head
        self.la = la
        self.ra = ra
        self.ll = ll
        self.rl = rl
        self.rt = rt
        self.lt = lt
        self.ct = ct
        self.bv = bv
        self.pilot = pilot
        self.maxwalkspeed = walkspeed
        self.maxrunspeed =int(math.ceil(walkspeed*1.5))
        self.tonnage = tonnage
        self.weightclass = ""
        self.weightclasscalc()
        self.enginerating = tonnage*walkspeed
        self.heat = 0
        self.heatunsinked = 0
        self.sinkingdoubled = False
        self.currentheatmod = 0
        self.isdead = False
        self.enginehits = 0
        self.gyrohits = 0
        self.case1 = case1
        self.case2 = case2
        self.sensorhits = 0
        self.isimmobile = False
        self.jumpspeed = 0
        self.movementmod = 0
        self.sinking=0
        self.doublesink = doublesink
        self.psrmalusperm = 0
        self.psrmalustemp = 0
        self.walkspeed = walkspeed
        self.runspeed = self.maxrunspeed
        self.heatmalus = 0
        self.causeofdeath = ""
        self.pos = 0
        self.weplist = []
        self.ammolist = []
        self.jetslist = []
        self.dmgthisturn = 0
        self.dmgpershot = []
        self.tmm = 0
        self.wepsfired = []
        self.critsthisturn = 0
        self.qdir = list(a for a in dir(self) if not a.startswith('__'))
        self.hiphits = 0
        self.basesinking = int(self.enginerating / 25)
        self.sinkingcalculator()
        self.parts = ["la", "ra", "ll", "rl", "rt", "lt", "ct", "hd"]
        #self.wepsandammogetter()
        self.motives = {}
        self.turn = 0
        self.multislot()
        self.setownership()

    def setownership(self):
        for i in self.parts:
            part = getattr(self, i)
            setattr(part, "owner", self)
            #print(f"{self.name} has now declared ownership over {i}!")
            part.declareownership()

    def printer(self):
        for i in self.parts:
            i = getattr(self, i)
            print(f"{i.name}\n Armour: {i.armour}\nStructure: {i.structure}")
        print(self.causeofdeath)

    def multislot(self):
        larm = self.la.multislot()
        rarm = self.ra.multislot()
        lleg = self.ll.multislot()
        rleg = self.rl.multislot()
        lls = [larm, lleg]
        rls = [rarm, rleg]
        for i in lls:
            if len(i) != 0:
                self.lt.multislot(i)
        for i in rls:
            if len(i) != 0:
                self.rt.multislot(i)
        lefttorso = self.lt.multislot()
        righttorso = self.rt.multislot()
        tls = [righttorso, lefttorso]
        for i in tls:
            if len(i) !=0:
                self.ct.multislot(i)
        a=self.ct.multislot()
        if len(a)!=0:
            raise(ValueError, "CT Can't multislot into something else! Muy problema!")
        for part in self.parts:
            #part = getattr(self, i)
            exec(f"self.{part}.listweps()")
        self.wepsandammogetter()


    def motivecalc(self):
        self.jumpspeed = 0
        self.walkspeed = self.maxwalkspeed
        hiphits = 0
        llhip = False
        rlhip = False
        if self.ll.isdestroyed and self.rl.isdestroyed:
            self.walkspeed = 0
            self.runspeed=0
            return
        elif self.ll.isdestroyed or self.rl.isdestroyed:
            self.walkspeed = 1
            self.runspeed = 1
        for key, value in self.motives.items():
            if key[3:] == "Hip":
                hiphits+=1
                self.walkspeed = math.ceil(self.maxwalkspeed/2)
                if key[0:2] == "rl":
                    rlhip = True
                else:
                    llhip = True
            if key[3:] == "Lower Leg" or key[3:] == "Upper Leg" or key[3:] == "Foot":
                if key[0:2] == "rl" and "rl Hip" in self.motives.items():
                    if self.motives.get("rl Hip") > value: continue
                    else:self.walkspeed -=1
                elif key[0:2] == "ll" and "ll Hip" in self.motives.items():
                    if self.motives.get("rl Hip") > value: continue
                    else:self.walkspeed -=1
                else:
                    self.walkspeed -=1
        if hiphits ==2:
            self.walkspeed = 0
            self.runspeed = 0
        self.runspeed = math.ceil(self.walkspeed*1.5)
        if hiphits == 1:
            self.runspeed = 1
        self.wepsandammogetter()


    def shutdown(self, target, guaranteed):
        pass

    def move(self, evading=False, enemy=None, isrunning=False):
        self.motivecalc()
        if not evading:
            if isrunning:
                self.movementmod = 2
                self.heat += 2
            else:
                self.movementmod=1
                self.heat +=1
        lranges = []
        mranges = []
        sranges = []
        runtmm = 0
        jumptmm = 0
        if evading:
            #print(self.name, self.jumpspeed, self.runspeed)
            if 3 > self.runspeed:
                runtmm = 0
            elif 2 < self.runspeed < 5:
                runtmm = 1
            elif 4 < self.runspeed < 7:
                runtmm = 2
            elif 6 < self.runspeed < 10:
                runtmm = 3
            elif 9 < self.runspeed < 18:
                runtmm = 4
            elif 17 < self.runspeed < 25:
                runtmm = 5
            elif self.runspeed > 24:
                runtmm = 6
            if 3 > self.jumpspeed:
                jumptmm = 0
            elif 2 < self.jumpspeed < 5:
                jumptmm = 1
            elif 4 < self.jumpspeed < 7:
                jumptmm = 2
            elif 6 < self.jumpspeed < 10:
                jumptmm = 3
            elif 9 < self.jumpspeed < 18:
                jumptmm = 4
            elif 17 < self.jumpspeed < 25:
                jumptmm = 5
            elif self.jumpspeed > 24:
                jumptmm = 6
            if self.jumpspeed > 0: jumptmm += 1
            if jumptmm > runtmm:
                self.tmm = jumptmm
            else:
                self.tmm = runtmm
        '''if not evading:
            distance = self.pos - enemy.pos
            for i in self.weplist:
                loc = i[:2]
                slot = i[-6:].strip()
                loc = getattr(self, loc)
                wep = getattr(loc, slot)
                lranges.append(wep.lrange)
                mranges.append(wep.mrange)
                sranges.append(wep.srange)
            if distance > max(lranges):
                print(wep)'''

        pass
    def wepsandammogetter(self):
        jlisto = []
        #print(list(a for a in dir(self) if not a.startswith('__')))
        #print(boingus)
        for attr in self.qdir:
            attrval = getattr(self, attr)
            if isinstance(attrval, MechPart) and getattr(attrval, 'hasweps') and not getattr(attrval, 'isdestroyed'):
                for shots in attrval.blasters:
                    wep = f'{attrval.name.lower()[-2:]} {shots}'
                    if wep not in self.weplist:
                        self.weplist.append(wep)
                #print(self.weplist)
                    #exec(f"self.weplist.append('{attrval.name.lower()[-2:]} {shots}')")
            if isinstance(attrval, MechPart) and getattr(attrval, 'hasammo') and not getattr(attrval, 'isdestroyed'):
                for i in attrval.ammoslots:
                    ammo = getattr(attrval, i)
                    if not ammo is None:
                        if not ammo.isdamaged:
                            #print(ammo)
                            #print(attrval.name, i)
                            exec(f"self.ammolist.append('{attrval.name.lower()[-2:]} {i}')")
                    if ammo is None:
                        #print(attrval.name, i, "None")
                        None
            if isinstance(attrval, MechPart) and getattr(attrval, "hasjets") and not getattr(attrval, "isdestroyed"):
                for i in attrval.jetslots:
                    jet = getattr(attrval, i)
                    if not jet or jet in jlisto: continue
                    if not jet.isdamaged:
                        self.jetslist.append(f'{attrval.name.lower()[-2:]} {i}')
                        self.jumpspeed += jet.jumping
                        jlisto.append(jet)
        #self.weplist = [attr for attr in dir(self) if isinstance(getattr(self, attr), MechPart) and getattr(getattr(self, attr),'hasweps') and not getattr(getattr(self, attr), 'isdestroyed')]


    def resolvedamage(self, dmg, location, hascrit=False):
        if self.isdead and self.causeofdeath != "":
            return
        if self.hd.isdestroyed:
            self.isdead = True
            self.causeofdeath = "HKill"
            return
        if self.ct.isdestroyed:
            self.isdead = True
            self.causeofdeath = "CTKill"
            return
        if self.lt.isdestroyed:
            self.la.isdestroyed = True
            self.la.dopartdestruction()
        if self.rt.isdestroyed:
            self.ra.isdestroyed = True
            self.ra.dopartdestruction()
        if dmg == 0:
            return
        if location == self.hd:
            self.pilot.DoPilotDamage()
            if self.pilot.isdead:
                self.isdead = True
                self.causeofdeath = "PKill"
        o = location.TakeDamage(dmg, hascrit, self)
        if getattr(location, "hasengine") and not location is self.ct and getattr(location, "isdestroyed"):
            location.dopartdestruction()
            if self.isdead and self.causeofdeath == "":
                self.causeofdeath = "TorsoEKill"
                return
            if self.isdead:
                return
        if o > 0:
            newloc = dooverflow(location, self)
            #print(newloc)
            if newloc == "Mech Destroyed":
                self.isdead = True
                if location == self.ct:
                    self.causeofdeath = "CTKill"
                elif location is self.hd:
                    self.causeofdeath = "HKill"
                return
                #print("Dead as fuck BROOOO")
            else:
                newloc = getattr(self, newloc.name.lower()[-2:])
                self.resolvedamage(o, newloc)
        self.motivecalc()

    def doammoexplosion(self, target):
        pass
    def heatresolution(self):
        if self.isdead: return
        self.currentheatmod = 0
        self.sinkingcalculator()
        # print(self.name, self.heat, self.sinking)
        self.heat = self.heat - self.sinking
        self.walkspeed = self.maxwalkspeed - (int(self.heat/5))
        self.runspeed = math.ceil(self.walkspeed * 1.5)
        self.heatmalus = 0
        if self.heat == 30:
            self.shutdown(self, True)
        if  7 < self.heat < 12:
            self.currentheatmod = 1
        elif 12 < self.heat < 17:
            self.currentheatmod = 2
        elif 16 < self.heat < 24:
            self.currentheatmod = 3
        elif 23 < self.heat:
            self.currentheatmod = 4
        if self.heat < 0:
            self.heat = 0
        #print(self.heat)
        #elif 30 > self.heat >

    def barrage(self, target, alphastrike=False, heatneutral=False, range=1, istest=False, allhit=False):
        self.wepsfired = []
        self.wepsandammogetter()
        #print(self.weplist)
        lsweps = []
        self.dmgpershot = []
        self.dmgthisturn = 0
        self.movementmod = 1
        guns2fire = {}
        range = (self.pos)-(target.pos)
        #for attr in dir(self):
            #attrval = getattr(self, attr)
            #if isinstance(attrval, MechPart) and getattr(attrval, 'hasweps') and not getattr(attrval, 'isdestroyed'):
               # for shots in attrval.blasters:
        for i in self.weplist:
            loc = i[0:2].lower()
            #print(loc)
            slot = i[-6:].strip()
            #print(slot)
            b =getattr(self, loc)
            wep= getattr(b, slot)
                    #wep = getattr(attrval, shots)#:3
            if wep not in lsweps: a = targetcalc(range, wep, self.pilot.gskill, False, self.currentheatmod, self.movementmod, self, target)
            if a == False: continue
            if wep not in lsweps:
                guns2fire[f"{loc} {slot}"] = wep.ratio*a
                lsweps.append(wep)
            else: continue
            sorted_guns2fire = sorted(guns2fire.items(), key=lambda x: x[1], reverse=True)
            guns2fire = dict(sorted_guns2fire)
        #print(guns2fire)
        for key in guns2fire:
            loc = key[0:2].lower()
            slot = key[-6:].strip()
            loc =getattr(self, loc)
            wep= getattr(loc, slot)#:3#
            if wep.lrange < range:
                continue
            if allhit and not wep.hasfired and not wep.isdamaged:
                dmgtester(wep, self, target, allhit)
                wep.hasfired = True
                continue
            if range==1 and not wep.hasfired and not wep.isdamaged:
                if istest:
                    dmgtester(wep, self, target)
                    wep.hasfired = True
                    continue
                fire(range, wep, self.pilot.gskill, False, self.currentheatmod, self.movementmod, self, target)
                wep.hasfired = True
                continue
            shotht = wep.heat + self.heat - self.sinking
            #print(wep.heat, self.heat, self.sinking, shotht)
            if shotht < 8 and not alphastrike and not wep.hasfired and not wep.isdamaged and not heatneutral:
                if istest:
                    dmgtester(wep, self, target)
                    wep.hasfired = True
                    continue
                exec(f"fire(range, wep, self.pilot.gskill, False, self.currentheatmod, self.movementmod, self, target)")
                if istest:
                    print("Firinig for real even tho is test!")
                wep.hasfired = True
                continue
            elif shotht >= 8 and not alphastrike and not wep.hasfired and not wep.isdamaged and not heatneutral:
                #print(f"Leaving {wep.name} off to save heat!")
                continue
            if heatneutral:
                if shotht < 4 and not wep.hasfired and not wep.isdamaged and heatneutral:
                    if istest:
                        dmgtester(wep, self, target)
                        wep.hasfired  =True
                        continue
                    exec(f"fire(range, wep, self.pilot.gskill, False, self.currentheatmod, self.movementmod, self, target)")
                    if istest:
                        print("Firinig for real even tho is test!")
                    wep.hasfired = True
                    continue
                if shotht > 3 or wep.hasfired:
                    continue
            if alphastrike:
                if shotht < 30 and alphastrike and not heatneutral and not wep.hasfired and not wep.isdamaged:
                    if istest:
                        dmgtester(wep, self, target)
                        wep.hasfired  =True
                        continue
                    exec(f"fire(range, wep, self.pilot.gskill, False, self.currentheatmod, self.movementmod, self, target)")
                    if istest:
                        print("Firinig for real even tho is test!")
                    wep.hasfired = True
                    continue
            else:
                continue

        for attr in self.qdir: #Resetting weapons to unfired state for next turn
            attrval = getattr(self, attr)
            if isinstance(attrval, MechPart) and getattr(attrval, 'hasweps'):
                for shots in attrval.blasters:
                    exec(f"attrval.{shots}.hasfired = False")
                    exec(f"attrval.{shots}.hashit = False")
        self.heatresolution()

    def sinkingcalculator(self):
        sinkslist = []
        if self.doublesink and not self.sinkingdoubled:
            self.basesinking = self.basesinking * 2
            self.sinkingdoubled = True
        heatsinkssinking = 0
        for attr in self.qdir:
            attrval = getattr(self, attr)
            if isinstance(attrval, MechPart) or isinstance(attrval, MechPartBig) and not getattr(attrval, 'isdestroyed'):
                for attrvals in attrval.slotqdir:
                    attrvalue = (getattr(attrval, attrvals))
                    if isinstance(attrvalue, HeatSink) and not attrvalue.isdamaged and not attrvalue in sinkslist:
                        #print(attrvals, attr)
                        sinkslist.append(attrvalue)
                        heatsinkssinking += attrvalue.sinking
        #print(sinkslist)
        self.sinking = self.basesinking + heatsinkssinking - (self.enginehits * 5)
        #print(self.name, self.sinking)

    def weightclasscalc(self):
        if self.tonnage <= 15:
            self.weightclass = "Proto"
        elif self.tonnage <= 35:
            self.weightclass = "Light"
        elif self.tonnage <= 55:
            self.weightclass = "Medium"
        elif self.tonnage <= 75:
            self.weightclass = "Heavy"
        elif self.tonnage <= 100:
            self.weightclass = "Assault"
        elif self.tonnage <= 130:
            self.weightclass = "Superheavy"
        else:
            return
    def useammo(self, wep=None, adding=False):
        # print("Using Ammo")
        firedgood = False
        # print(wep.name)
        for i in self.ammolist:
            loc =i[0:2].lower()
            slot = i[-6:].strip()
            loc = getattr(self ,loc)
            ammo = getattr(loc, slot)
            # print(ammo.name, wep.ammo)
            if not wep is None and ammo.name.strip() == wep.ammo.strip():
                if ammo.ammonum > 0:
                    # print(ammo.ammonum)
                    # print(f"{wep.name} fired!")
                    ammo.ammonum -= 1
                    #print(ammo.ammonum)
                    firedgood = True
                    return firedgood
            elif adding:
                ammo.ammonum+=1
            else:
                # print(ammo.name, "is not", wep.ammo)
                continue
        if adding:
            return
        return firedgood





# Mech Utility
heatsink = HeatSink("Single Heatsink", ids=["Heat Sink"])
isdoubleheatsink = HeatSink("Double Heatsink", 2, 3, ids=["ISDoubleHeatSink", "IS Double Heat Sink", "ISDouble Heat Sink"])
clandoubleheatsink = HeatSink("Double Heatsink", 2, 2, ids=["CLDoubleHeatSink", "Clan Double Heat Sink", "CLDouble Heat Sink"])
fusengine = Engine("Fusion Engine", 1, False, True, ids=["Fusion Engine"])
gyro = MechUtility("Gyro", 1, False, False, True, ids=["Gyro"])
jumpjet = JumpJet("Jump Jet", ids=["Jump Jet", "JumpJet"])
#MechUtils = {"Gyro":gyro, "Fusion Engine":fusengine, "Heat Sink":heatsink, "ISDouble Heat Sink":isdoubleheatsink, "CLDoubleHeatSink (omnipod)":clandoubleheatsink, "CLDoubleHeatSink":clandoubleheatsink}
MechUtils=[heatsink, isdoubleheatsink, clandoubleheatsink, fusengine, gyro, jumpjet]

# Ammo Bins
mgammo = AmmoBin("MG Ammo", 200, 1, True, 2, ids=["IS Ammo MG - Full", "ISMG Ammo (200)", "ISMG Ammo Full", "IS Machine Gun Ammo"])
mghalfammo = AmmoBin("MG Ammo", 100, 1, True, 2, ids=["IS Machine Gun Ammo - Half", "IS Ammo MG - Half", "ISMG Ammo (100)", "ISMG Ammo Half", "IS Machine Gun Ammo (1/2 ton)", "Half Machine Gun Ammo"])
ac2ammo = AmmoBin("AC2 Ammo", 45, 1, True, 2, ids=["IS Ammo AC/2", "ISAC2 Ammo", "IS Autocannon/2 Ammo"])
ac5ammo = AmmoBin("AC5 Ammo", 20, 1, True, 5, ids=["IS Ammo AC/5", "ISAC5 Ammo", "IS Autocannon/5 Ammo"])
ac10ammo = AmmoBin("AC10 Ammo", 10, 1, True, 10, ids=["IS Ammo AC/10", "ISAC10 Ammo", "IS Autocannon/10 Ammo"])
ac20ammo = AmmoBin("AC20 Ammo", 5, 1, True, 20, ids=["IS Ammo AC/20", "ISAC20 Ammo", "IS Autocannon/20 Ammo"])
gaussammo = AmmoBin("Gauss Rifle Ammo", 8, 1, False, 0, ids=["IS Gauss Ammo", "IS Ammo Gauss", "ISGauss Ammo", "IS Gauss Rifle Ammo", "ISGaussRifle Ammo", "Clan Gauss Ammo", "Clan Ammo Gauss", "CLGauss Ammo", "Clan Gauss Rifle Ammo"])
srm2ammo = AmmoBin("SRM2 Ammo", 50, 1, True, 4, ids=["IS Ammo SRM-2", "ISSRM2 Ammo", "IS SRM 2 Ammo", "Clan Ammo SRM-2", "CLSRM2 Ammo", "Clan SRM 2 Ammo"])
srm4ammo = AmmoBin("SRM4 Ammo", 25, 1, True, 8, ids=["IS Ammo SRM-4","ISSRM4 Ammo", "IS SRM 4 Ammo", "Clan Ammo SRM-4", "CLSRM4 Ammo", "Clan SRM 4 Ammo"])
srm6ammo = AmmoBin("SRM6 Ammo", 15, 1, True, 12, ids=["IS Ammo SRM-6","ISSRM6 Ammo", "IS SRM 6 Ammo", "Clan Ammo SRM-6", "CLSRM6 Ammo", "Clan SRM 6 Ammo"])
ssrm2ammo = AmmoBin("Streak SRM2 Ammo", 50, 1, True, 4, ids=["IS Streak SRM 2 Ammo", "IS Ammo Streak-2", "ISStreakSRM2 Ammo", "Clan Streak SRM 2 Ammo", "Clan Ammo Streak-2", "CLStreakSRM2 Ammo"])
ssrm4ammo = AmmoBin("Streak SRM4 Ammo", 25, 1, True, 8, ids=["IS Streak SRM 4 Ammo", "IS Ammo Streak-4", "ISStreakSRM4 Ammo", "Clan Streak SRM 4 Ammo", "Clan Ammo Streak-4", "CLStreakSRM4 Ammo"])
ssrm6ammo = AmmoBin("Streak SRM6 Ammo", 15, 1, True, 12, ids=["IS Streak SRM 6 Ammo", "IS Ammo Streak-6", "ISStreakSRM6 Ammo", "Clan Streak SRM 6 Ammo", "Clan Ammo Streak-6","CLStreakSRM6 Ammo"])
lrm5ammo = AmmoBin("LRM5 Ammo", 24, 1, True, 5, ids=["IS Ammo LRM-5", "ISLRM5 Ammo", "IS LRM 5 Ammo", "Clan Ammo LRM-5", "CLLRM5 Ammo", "Clan LRM 5 Ammo"])
lrm10ammo = AmmoBin("LRM10 Ammo", 12, 1, True, 10, ids=["IS Ammo LRM-10", "ISLRM10 Ammo", "IS LRM 10 Ammo", "Clan Ammo LRM-10","CLLRM10 Ammo", "Clan LRM 10 Ammo"])
lrm15ammo = AmmoBin("LRM15 Ammo", 8, 1, True, 15, ids=["IS Ammo LRM-15", "ISLRM15 Ammo", "IS LRM 15 Ammo", "Clan Ammo LRM-15","CLLRM15 Ammo", "Clan LRM 15 Ammo"])
lrm20ammo = AmmoBin("LRM20 Ammo", 6, 1, True, 20, ids=["IS Ammo LRM-20", "ISLRM20 Ammo", "IS LRM 20 Ammo", "Clan Ammo LRM-20","CLLRM20 Ammo", "Clan LRM 20 Ammo"])
MechAmmo = [mgammo, mghalfammo, ac2ammo, ac5ammo, ac10ammo, ac20ammo, gaussammo, srm2ammo, srm4ammo, srm6ammo, ssrm2ammo, ssrm4ammo, ssrm6ammo, lrm5ammo, lrm10ammo, lrm15ammo, lrm20ammo]
# Lasers
largelaser = Weapon("Large Laser", 5, 10, 15, 8, 8, "DE", 123, 2, ids=["Large Laser", "IS Large Laser", "ISLargeLaser"])
iserlargelaser = Weapon("ER Large Laser", 7, 14, 19, 8, 12, "DE", 163, 2 ,ids=["ISERLargeLaser", "IS ER Large Laser"])
clanerlargelaser = Weapon("ER Large Laser", 8, 15, 25, 10, 12, "DE", 248, ids=["CLERLargeLaser", "Clan ER Large Laser"])
isplargelaser = Weapon("Large Pulse Laser", 3, 7, 10, 9, 10, "P", 119, 2, -2, ids=["ISLargePulseLaser", "IS Pulse Large Laser", "IS Large Pulse Laser"])
clanplargelaser = Weapon("Large Pulse Laser", 6, 14, 20, 10, 10, "P", 265, 2, (-2), ids=["CLLargePulseLaser", "Clan Pulse Large Laser","Clan Large Pulse Laser"])
erplargelaser = Weapon("ER Large Pulse Laser", 7, 15, 23, 10, 13, "P", 272, 3, (-1), ids=["CLERLargePulseLaser", "Clan ER Pulse Large Laser","Clan ER Large Pulse Laser"])
mediumlaser = Weapon("Medium Laser", 3, 6, 9, 5, 3, "DE", 46, ids=["Medium Laser", "IS Medium Laser", "ISMediumLaser"])
heavymedlaser = Weapon("Heavy Medium Laser", 3, 6, 9, 10, 7, "DE", 76, 2, (+1), ids=["CLHeavyMediumLaser", "Clan Medium Heavy Laser"])
ispmediumlaser = Weapon("Medium Pulse Laser", 2, 4, 6, 6, 4, "P", 48, 1, (-2), ids=["ISMediumPulseLaser", "IS Pulse Med Laser", "IS Medium Pulse Laser"])
clanpmediumlaser = Weapon("Medium Pulse Laser", 4, 8, 12, 7, 4, "P", 111, 1, (-2), ids=["CLMediumPulseLaser", "Clan Pulse Med Laser", "Clan Medium Pulse Laser"])
isermediumlaser = Weapon("ER Medium Laser", 4, 8, 12, 5, 5, "DE", 62, ids=["ISERMediumLaser", "IS ER Medium Laser"])
clanermediumlaser = Weapon("ER Medium Laser", 5, 10, 15, 7, 5, "DE", 108, ids=["CLERMediumLaser", "Clan ER Medium Laser"])
erpmediumlaser = Weapon("ER Medium Pulse Laser", 5, 9, 14, 7, 6, "P", 117, 2, (-1), ids=["CLERMediumPulseLaser", "Clan ER Pulse Med Laser", "Clan ER Medium Pulse Laser"])
smalllaser = Weapon("Small Laser", 1, 2, 3, 3, 1, "DE", 9, ids=["Small Laser", "ISSmall Laser", "ISSmallLaser", "ClSmall Laser", "CL Small Laser", "CLSmallLaser"])
ispsmalllaser = Weapon("Small Pulse Laser", 1, 2, 3, 3, 2, "P", 12, 1, (-2), ids=["ISSmallPulseLaser", "IS Small Pulse Laser", "ISSmall Pulse Laser"])
clanpsmalllaser = Weapon("Small Pulse Laser", 2, 4, 6, 3, 2, "P", 24, 1, (-2), ids=["CLSmallPulseLaser", "Clan Pulse Small Laser", "Clan Small Pulse Laser"])
clanersmalllaser = Weapon("ER Small Laser", 2, 4, 6, 5, 2, "DE", 31, ids=["CLERSmallLaser", "Clan ER Small Laser"])
isersmalllaser = Weapon("ER Small Laser", 2, 4, 5, 3, 2, "DE", 17, ids=["ISERSmallLaser", "IS ER Small Laser"])
erpsmalllaser = Weapon("ER Small Pulse Laser", 2, 4, 6, 5, 3, None, 36, 1, (-1), ids=["CLERSmallPulseLaser", "Clan ER Pulse Small Laser", "Clan ER Small Pulse Laser", "ClanERSmallPulseLaser"])
Lasers = [largelaser, iserlargelaser, clanerlargelaser, isplargelaser, clanplargelaser, erplargelaser, mediumlaser, heavymedlaser, ispmediumlaser, clanpmediumlaser, isermediumlaser, clanermediumlaser, erpmediumlaser, smalllaser, ispsmalllaser, clanpsmalllaser, clanersmalllaser, isersmalllaser, erpsmalllaser]

# PPCs
ppc = Weapon("PPC", 6, 12, 18, 10, 10, "DE", 176, 3, 0, 3, ids=["PPC", "Particle Cannon", "IS PPC", "ISPPC"])
iserppc = Weapon("ERPPC", 7, 14, 23, 10, 15, "DE", 228, 3, 0, 0, ids=["ISERPPC", "IS ER PPC"])
clanerppc = Weapon("ERPPC", 7, 14, 23, 15, 15, "DE", 412, 2, 0, 0, ids=["CLERPPC", "Clan ER PPC"])
heavyppc = Weapon("Heavy PPC", 6, 12, 18, 15, 15, "DE", 317, 4, 0, 3, ids=["Heavy PPC", "ISHeavyPPC", "ISHPPC"])
lightppc = Weapon("Light PPC", 6, 12, 18, 5, 5, "DE", 88, 2, 0, 3, ids=["Light PPC", "ISLightPPC", "ISLPPC"])
PPCs = [ppc, clanerppc, heavyppc, iserppc, lightppc]

# Ballistics
machinegun = Autocannon("Machine Gun", 1, 2, 3, 2, 0, "AI", 20, 1, 0, 0, "MG Ammo", ids=["Machine Gun", "IS Machine Gun", "ISMachine Gun", "ISMG", "CLMG", "Clan Machine Gun"])
ac2 = Autocannon("AC2", 8, 16, 24, 2, 1, "B", 37, 1, 0, 4, "AC2 Ammo", ids=["Autocannon/2", "IS Auto Cannon/2", "Auto Cannon/2", "AutoCannon/2", "AC/2", "ISAC2", "IS Autocannon/2"])
ac5 = Autocannon("AC5", 6, 12, 18, 5, 1, "B", 70, 4, 0, 3, "AC5 Ammo", ids=["Autocannon/5", "IS Auto Cannon/5", "Auto Cannon/5", "AC/5", "AutoCannon/5", "ISAC5", "IS Autocannon/5"])
ac10 = Autocannon("AC10", 5, 10, 15, 10, 3, "B", 123, 7, 0, 0, "AC10 Ammo", ids=["Autocannon/10", "IS Auto Cannon/10", "Auto Cannon/10", "AutoCannon/10", "AC/10", "ISAC10", "IS Autocannon/10"])
ac20 = Autocannon("AC20", 3, 6, 9, 20, 7, "B", 178, 10, 0, 0, "AC20 Ammo", ids=["Autocannon/20", "IS Auto Cannon/20", "Auto Cannon/20", "AutoCannon/20", "ISAC20", "IS Autocannon/20"])
isgaussrifle = Autocannon("Gauss Rifle", 7, 15, 22, 15, 1, "B", 320, 7, 0, 2, "Gauss Rifle Ammo", ids=["ISGaussRifle", "IS Gauss Rifle"], isexplosive=True)
clangaussrifle = Autocannon("Gauss Rifle", 7, 15, 22, 15, 1, "B", 320, 6, 0, 2, "Gauss Rifle Ammo", ids=["CLGaussRifle", "Clan Gauss Rifle"], isexplosive=True)
Ballistics = [machinegun, ac2, ac5, ac10, ac20, isgaussrifle, clangaussrifle]

# Missiles
srm2 = Missile("SRM 2", 3, 6, 9, 2, 2, "Cluster", 21, 1, 0, 0, "SRM2 Ammo", 2, 0, 1, False, False, ids=["SRM 2", "IS SRM-2", "ISSRM2", "IS SRM 2", "CLSRM2", "Clan SRM-2", "Clan SRM 2"])
isssrm2 = Missile("Streak SRM 2", 3, 6, 9, 2, 2, "Cluster", 30, 1, 0, 0, "Streak SRM2 Ammo", 2, 0, 1, True, False, False, ids=["ISStreakSRM2", "IS Streak SRM-2", "IS Streak SRM 2"])
clanssrm2 = Missile("Streak SRM 2", 4, 8, 12, 2, 2, "Cluster", 40, 1, 0, 0, "Streak SRM2 Ammo", 2, 0, 1, True, ids=["CLStreakSRM2", "Clan Streak SRM-2", "Clan Streak SRM 2"])
srm4 = Missile("SRM 4", 3, 6, 9, 2, 3, "Cluster", 39, 1, 0, 0, "SRM4 Ammo", 4, 0, 1, ids=["SRM 4", "IS SRM-4", "ISSRM4", "IS SRM 4", "CLSRM4", "Clan SRM-4", "Clan SRM 4"])
isssrm4 = Missile("Streak SRM 4", 3, 6, 9, 2, 3, "Cluster", 59, 1, 0, 0, "Streak SRM4 Ammo", 4, 0, 1, True, ids=["ISStreakSRM4", "IS Streak SRM-4", "IS Streak SRM 4"])
clanssrm4 = Missile("Streak SRM 4", 4, 8, 12, 2, 3, "Cluster", 59, 1, 0, 0, "Streak SRM4 Ammo", 4, 0, 1, True, ids=["CLStreakSRM4", "Clan Streak SRM-4", "Clan Streak SRM 4"])
issrm6 = Missile("SRM 6", 3, 6, 9, 2, 4, "Cluster", 59, 2, 0, 0, "SRM6 Ammo", 6, 0, 1, ids=["SRM 6", "IS SRM-6", "ISSRM6", "IS SRM 6"])
clansrm6 = Missile("SRM 6", 3, 6, 9,2,4, "Cluster", 59, 1, 0, 0, "SRM6 Ammo", 6, 0, 1, ids=["CLSRM6", "Clan SRM-6", "Clan SRM 6"])
isssrm6= Missile("Streak SRM 6", 3, 6, 9, 2, 4, "Cluster", 89, 2, 0, 0, "Streak SRM6 Ammo", 6, 0, 1, True, ids=["ISStreakSRM6", "IS Streak SRM-6", "IS Streak SRM 6"])
clanssrm6 = Missile("Streak SRM 6", 4, 8, 12, 2, 4, "Cluster", 118, 2, 0, 0, "Streak SRM6 Ammo", 6, 0, 1, True, ids=["CLStreakSRM6", "Clan Streak SRM-6", "Clan Streak SRM 6"])
islrm5 = Missile("LRM 5", 7, 14, 21, 1, 2, "Cluster", 45, 1, 0, 6, "LRM5 Ammo", 5, 0, 5, ids=["LRM 5", "IS LRM-5", "ISLRM5", "IS LRM 5"])
clanlrm5 = Missile("LRM 5", 7, 14, 21, 1, 2, "Cluster", 55, 1, 0, 0, "LRM5 Ammo", 5, 0, 5, ids=["CLLRM5", "Clan LRM-5", "Clan LRM 5"])
islrm10 = Missile("LRM 10", 7, 14, 21, 1, 4, "Cluster", 90, 2, 0, 6, "LRM10 Ammo", 10, 0, 5, ids=["LRM 10", "IS LRM-10", "ISLRM10", "IS LRM 10"])
clanlrm10 = Missile("LRM 10", 7, 14, 21, 1, 4, "Cluster", 109, 1, 0, 0, "LRM10 Ammo", 10, 0, 5, ids=["CLLRM10", "Clan LRM-10", "Clan LRM 10"])
islrm15 = Missile("LRM 15", 7, 14, 21, 1, 5, "Cluster", 136, 3, 0, 6, "LRM15 Ammo", 15, 0, 5, ids=["LRM 15", "IS LRM-15", "ISLRM15", "IS LRM 15"])
clanlrm15 = Missile("LRM 15", 7, 14, 21, 1, 5, "Cluster", 164, 2, 0, 0, "LRM15 Ammo", 15, 0, 5, ids=["CLLRM15", "Clan LRM-15", "Clan LRM 15"])
islrm20 = Missile("LRM 20", 7, 14, 21, 1, 6, "Cluster", 181, 5, 0, 6, "LRM20 Ammo", 20, 0, 5, ids=["LRM 20", "IS LRM-20", "ISLRM20", "IS LRM 20"])
clanlrm20 = Missile("LRM 20", 7, 14, 21, 1, 6, "Cluster", 236, 4, 0, 0, "LRM20 Ammo", 20, 0, 5, ids=["CLLRM20", "Clan LRM-20", "Clan LRM 20"])
MechMissiles = [srm2, isssrm2, clanssrm2, srm4, isssrm4, clanssrm4, issrm6, clansrm6, isssrm6, clanssrm6, islrm5, clanlrm5, islrm10, clanlrm10, islrm15, clanlrm15, islrm20, clanlrm20]
# 'Mech Bits
#awesomehead8q = MechPart("Awesome HD", 9, 3, "Life Support", "Sensors", "Cockpit", copy.deepcopy(smalllaser), "Sensors", "Life Support", False, True)
#awesomeleftleg8q = MechPart("Awesome LL", 33, 17, "Hip", "Upper Leg", "Lower Leg", "Foot", copy.deepcopy(heatsink), copy.deepcopy(heatsink))
#awesomerightleg8q = MechPart("Awesome RL", 33, 17, "Hip", "Upper Leg", "Lower Leg", "Foot", copy.deepcopy(heatsink), copy.deepcopy(heatsink))
#awesomerightarm8q = MechPartBig("Awesome RA", 24, 0, 13, "Shoulder", "Upper Arm", "Lower Arm", copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(ppc))
#awesomeleftarm8q = MechPartBig("Awesome LA", 24, 0, 13, "Shoulder", "Upper Arm", "Lower Arm", "Hand")
#awesomerighttorso8q = MechPartBig("Awesome RT", 24, 10, 17, copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(ppc))
#awesomelefttorso8q = MechPartBig("Awesome LT", 24, 10, 17, copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(ppc))
#awesomecentretorso8q = MechPartBig("Awesome CT", 30, 19, 25, copy.deepcopy(fusengine), copy.deepcopy(fusengine), copy.deepcopy(fusengine), copy.deepcopy(gyro), copy.deepcopy(gyro), copy.deepcopy(gyro), copy.deepcopy(gyro), copy.deepcopy(fusengine), copy.deepcopy(fusengine), copy.deepcopy(fusengine), copy.deepcopy(heatsink), copy.deepcopy(heatsink))
#thunderbolt5srightarm = MechPartBig("Thunderbolt RA", 20, 0, 10, "Shoulder", "Upper Arm", "Lower Arm", "Hand", copy.deepcopy(largelaser))

# Mechwarriors
genericmechwarrior = Pilot("David B.", 5, 2)

# Battlemechs
# awesome8q = Battlemech("Awesome 8Q", awesomehead8q, awesomeleftarm8q, awesomerightarm8q, awesomeleftleg8q, awesomerightleg8q, awesomerighttorso8q, awesomelefttorso8q, awesomecentretorso8q, genericmechwarrior, 3, 80)

mechbits = [MechUtils, PPCs, Lasers, MechMissiles, MechAmmo, Ballistics]

def fire(range, shooter, skill, allhit=False, heatmod=0, movemod=0, firingmech=None, target=None, istest=False):
    #print(firingmech.turn)
    #print(shooter.name)
    hitloc = None
    hasheated = False
    target.turn+=0.00000001
    range = int(range)
    skill = getattr(firingmech, "pilot")
    skill = getattr(skill, "gskill")
    if shooter.hasfired:
        return
    shooter.hasfired = True
    if range <= shooter.minrange:
        rmod = (shooter.minrange - range)+1
    elif range <= shooter.srange:
        rmod = 0
    elif range <= shooter.mrange:
        rmod = 2
    elif range <= shooter.lrange:
        rmod = 4
    else:
        return "Impossible"
    if hasattr(shooter, 'ammo'):
        if getattr(shooter, 'ammo') != None:
            #print(shooter)
            hadammo = firingmech.useammo(shooter)
            if not hadammo:
                # print("Click!", shooter.name)
                return
            else:
                # print("Fired", shooter.name)
                None
        else:
            raise(f"{shooter.name} has attr ammo, but Ammo is set to None!")
    hittarget = skill + rmod + shooter.targetmod + heatmod + movemod + target.tmm
    if allhit:
        hittarget = 0
    roll = random.randint(1, 6) + random.randint(1, 6)
    # print(rmod, roll, hittarget, range, shooter.name, target.tmm, movemod, skill, firingmech.name, target.name)
    if not hasattr(shooter, "streak") or hasattr(shooter, "streak") and  not getattr(shooter, "streak"):
        firingmech.wepsfired.append(shooter.name)
        firingmech.heat += shooter.heat
        hasheated = True
    if roll >= hittarget:
        if isinstance(shooter, Missile) and getattr(shooter, "streak"):
            if shooter.streak == True:
                firingmech.wepsfired.append(shooter.name)
                firingmech.heat += shooter.heat
        #print("Hit!")
        #print("Hit with " + shooter.name + "!")
        if hasattr(shooter, 'cluster') and shooter.cluster != None:
            docluster(shooter.dmg, shooter, firingmech, target)
            shooter.hasfired = True
            return
        hitloc = RollLocation()
        loc = hitloc[0]
        loc = loc[-2:].lower()
        #print(loc)
        loc = getattr(target, loc)
        if type(loc) == "str":
            print(loc, "huh?")
        #print(loc.name, type(loc))
        if loc.isdestroyed:
            while isinstance(loc, MechPart) and loc.isdestroyed:
                loc = dooverflow(loc, target)
        shooter.hit = True
        firingmech.dmgthisturn += shooter.dmg
        firingmech.dmgpershot.append(shooter.dmg)
        target.resolvedamage(shooter.dmg, loc, hitloc[1])
        if not hasheated:
            firingmech.heat += shooter.heat
    else:
        #print(f"Miss with {shooter.name}!")
        return "Miss!"

def crit(target, critnum, mek):
    critoverflow = 0
    limbdeath = False
    crittablebits = 0
    mtbits = ["Empty", "Ferro-Fibrous", "ISCASEII", "IS CASE II", "CLCASEII", "Clan CASE II", "ISCASE", "IS Endo Steel","IS EndoSteel","IS Endo-Steel","IS Endo Steel Structure","IS EndoSteel Structure","IS Endo-Steel Structure", "Clan Endo Steel","Clan Endo-Steel","Clan EndoSteel","Clan Endo-Steel Structure","Clan EndoSteel Structure","Clan Endo Steel Structure"]
    if target == "Mech Destroyed":
        return
    for i in target.slotqdir:
        i = getattr(target, i)
        if i is None:
            continue
        if not i is None:
            if not type(i) is str:
                crittablebits += 1
                #print(i.name)
                #print(i.name, "is a thing", crittablebits)
                continue
            elif type(i) is str and not i in mtbits:
                crittablebits += 1
                #print(i)
                #print(i, "Is a thing", crittablebits)
                continue
    #print(target.name, "Has", crittablebits, "crittable bits!")
    if crittablebits == 0 and not target.isdestroyed:
        #print(f"{target.name} has no crittable stuff, moving on!")
        crit(dooverflow(target, mek), (critnum), mek)
        return
    if isinstance(target, str):
        return
    target.owner.critsthisturn += 1
    if critnum == 3:
        a = lambda l:target.name.lower()[-2:] == l
        if a('hd') or a('ll') or a('rl') or a('la') or a('ra'):
            # print("Wow")
            limbdeath = True
            target.isdestroyed = True
            if a('hd'):
                mek.isdead = True
                mek.causeofdeath = ('HKill')
                #print("Wowie")
            return
    if critnum > crittablebits:
        critnum = crittablebits
        #print(critnum, crittablebits, target.name)
    times = 0
    z=0
    while times < critnum:
        mek.turn +=0.0000000001
        loc = target.name.lower()[-2:]
        #print(z)
        if target.isdestroyed:
            critoverflow = critnum-times
            break
        if isinstance(target, MechPartBig):
            roll = random.randint(1, 12)
        else:
            roll = random.randint(1, 6)
        location = f"slot{roll}"
        a=getattr(target, location)
        if getattr(target, location) is None:
            if z > 100:
                if target.name.lower()[-2:] =="ct":
                    mek.isdead = True
                    mek.causeofdeath = "CTKill"
                    return
                break
            z+=1
            continue
        elif isinstance(a, str):
            if a == "Cockpit" and target is target.owner.hd:
                if target.structure <= 0:
                    mek.causeofdeath = "HKill"
                    mek.isdead = True
                    return
                mek.isdead = True
                mek.causeofdeath = "HKill"
                #print(f"COCKSHOT {mek.name}")
                return
            thing = loc + " " + a
            mek.motives[thing] = mek.turn
            setattr(target, location, None)
            times=times+1
            z += 1
            continue
        else:
            a = (getattr(target, location))
            #print(a.name)
            times = times+1
            #print(times)
            #print(z)
            z += 1
            if isinstance(a, MechUtility) or isinstance(a, HeatSink) or isinstance(a, JumpJet) or isinstance(a, Weapon) or isinstance(a, AmmoBin):
                if hasattr(a, "isexplosive") and getattr(a, "isexplosive"):
                    #print(f"Critting {a.name}!")
                    mek.resolvedamage(a.parthit(True), target)
                    setattr(target, "location", None)
                    if mek.isdead:
                        mek.causeofdeath = ("AmmoKill")
                        return
                else:
                    a.parthit(True)
                    #print(f"Critting {a.name}!")
                    setattr(target, "location", None)
                    if mek.isdead and mek.enginehits >= 3:
                        mek.causeofdeath = "EKill"
                        return
            #if isinstance(a, AmmoBin):
            #    mek.resolvedamage(a.parthit(True), target)
            #    if mek.isdead:
            #        mek.causeofdeath = ("AmmoKill")
            #print(getattr(a, 'isdamaged'))
            setattr(target, location, None)
            continue
    if limbdeath:
        print("Jimmy")
    if critoverflow > 0: crit(dooverflow(target, mek), (critoverflow), mek)


def docluster(dmg=0, weapon=None, firingmech=None, target=None, istest=False, predet=None):
    clust2 = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
    clust3 = [1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3]
    clust4 = [1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4]
    clust5 = [1, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5]
    clust6 = [2, 2, 3, 3, 4, 4, 4, 5, 5, 6, 6]
    clust7 = [2, 2, 3, 4, 4, 4, 4, 6, 6, 7, 7]
    clust8 = [3, 3, 4, 4, 5, 5, 5, 6, 6, 8, 8]
    clust9 = [3, 3, 4, 5, 5, 5, 5, 7, 7, 9, 9]
    clust10 = [3, 3, 4, 6, 6, 6, 6, 8, 8, 10, 10]
    clust11 = [4, 4, 5, 7, 7, 7, 7, 8, 8, 11, 11]
    clust12 = [4, 4, 5, 8, 8, 8, 8, 10, 10, 12, 12]
    clust13 = [4, 4, 5, 8, 8, 8, 8, 11, 11, 13, 13]
    clust14 = [5, 5, 6, 9, 9, 9, 9, 11, 11, 14, 14]
    clust15 = [5, 5, 6, 9, 9, 9, 9, 12, 12, 15, 15]
    clust16 = [5, 5, 7, 10, 10, 10, 10, 13, 13, 16, 16]
    clust17 = [5, 5, 7, 10, 10, 10, 10, 14, 14, 17, 17]
    clust18 = [6, 6, 8, 11, 11, 11, 11, 14, 14, 18, 18]
    clust19 = [6, 6, 8, 11, 11, 11, 11, 15, 15, 19, 19]
    clust20 = [6, 6, 9, 12, 12, 12, 12, 16, 16, 20, 20]
    clust21 = [7, 7, 9, 13, 13, 13, 13, 17, 17, 21, 21]
    clust22 = [7, 7, 9, 14, 14, 14, 14, 18, 18, 22, 22]
    clust23 = [7, 7, 10, 15, 15, 15, 15, 19, 19, 23, 23]
    clust24 = [8, 8, 10, 16, 16, 16, 16, 20, 20, 24, 24]
    clust25 = [8, 8, 10, 16, 16, 16, 16, 21, 21, 25, 25]
    clust26 = [9, 9, 11, 17, 17, 17, 17, 21, 21, 26, 26]
    clust27 = [9, 9, 11, 17, 17, 17, 17, 22, 22, 27, 27]
    clust28 = [9, 9, 11, 17, 17, 17, 17, 23, 23, 28, 28]
    clust29 = [10, 10, 12, 18, 18, 18, 18, 23, 23, 29, 29]
    clust30 = [10, 10, 12, 18, 18, 18, 18, 24, 24, 30, 30]
    clust40 = [12, 12, 18, 24, 24, 24, 24, 32, 32, 40, 40]
    #clustdict = {2:clust2, 3:clust3, 4:clust4, 5:clust5, 6:}
    j=locals()
    roll = random.randint(1, 6) + random.randint(1, 6)
    roll+=weapon.clustermod
    if weapon.artemis4: roll +=2
    if weapon.artemis5: roll +=3
    if roll > 12: roll = 12
    if weapon.streak:roll = 12
    cluster = j[f"clust{weapon.cluster}"]
    ldict = {}
    #print(f"{weapon.cluster}")
    #print(cluster)
    if not predet is None and not weapon.streak: roll = predet
    roll -=2
    if not predet is None:
        return cluster[roll]*weapon.dmg
    #print(cluster[roll] // weapon.grouping)
    hitloc = RollLocation()
    loc = hitloc[0]
    loc = loc[-2:].lower()
    loc = getattr(target, loc)
    weapon.hit = True
    firingmech.dmgthisturn += cluster[roll]*weapon.dmg
    for i in range(cluster[roll]//weapon.grouping):
        hitloc = RollLocation()
        loc = hitloc[0]
        loc = loc[-2:].lower()
        loc = getattr(target, loc)
        #print(f"One missile from {weapon.name} hit target's {loc.name}!")
        firingmech.dmgpershot.append(dmg*weapon.grouping)
        target.resolvedamage((dmg*weapon.grouping), loc, hitloc[1])
    if cluster[roll]%weapon.grouping != 0:
        hitloc = RollLocation()
        loc = hitloc[0]
        loc = loc[-2:].lower()
        loc = getattr(target, loc)
        firingmech.dmgpershot.append(int(dmg * cluster[roll]%weapon.grouping))
        target.resolvedamage(int(dmg * cluster[roll]%weapon.grouping), loc, hitloc[1])


def targetcalc(range, shooter, skill, allhit=False, heatmod=0, movemod=0, firingmech=None, target=None, istest=False):
    rmod = 0
    if range <= shooter.minrange:
        rmod = (shooter.minrange - range)+1
        #print(rmod)
    elif shooter.minrange < range <= shooter.srange:
        rmod = 0
    elif range <= shooter.mrange:
        rmod = 2
    elif range <= shooter.lrange:
        rmod = 4
    else:
        return False
    hittarget = rmod + shooter.targetmod + firingmech.pilot.gskill + firingmech.currentheatmod + firingmech.movementmod + target.tmm
    if istest:
        target.tmm = 2
        hittarget = rmod + shooter.targetmod + firingmech.pilot.gskill + firingmech.currentheatmod + firingmech.movementmod + target.tmm
        print(hittarget, rmod, shooter.targetmod, firingmech.pilot.gskill, firingmech.currentheatmod, firingmech.heat,
              firingmech.movementmod, target.tmm)
    if target.isimmobile:
        hittarget -=4
    if hittarget <= 2:
        return 1
    elif hittarget == 3:
        return 35/36
    elif hittarget == 4:
        return 33/36
    elif hittarget == 5:
        return 30/36
    elif hittarget == 6:
        return 26/36
    elif hittarget == 7:
        return 21/36
    elif hittarget == 8:
        return 15/36
    elif hittarget == 9:
        return 10/36
    elif hittarget == 10:
        return 6/36
    elif hittarget == 11:
        return 3/36
    elif hittarget == 12:
        return 1/36
    else:
        return False

def dmgtester(shooter, firingmech, target, allhit=False):
    if shooter.hasfired:
        return
    shooter.hasfired = True
    range = abs(firingmech.pos - target.pos)
    if range <= shooter.minrange:
        rmod = (shooter.minrange - range)+1
    elif shooter.minrange < range <= shooter.srange:
        rmod = 0
    elif range <= shooter.mrange:
        rmod = 2
    elif range <= shooter.lrange:
        rmod = 4
    if hasattr(shooter, 'ammo'):
        if getattr(shooter, 'ammo') != None:
            #print(shooter)
            hadammo = firingmech.useammo(shooter)
            if not hadammo:
                # print("Click!", shooter.name)
                return
            else:
                # print("Fired", shooter.name)
                None
        else:
            raise(f"{shooter.name} has attr ammo, but Ammo is set to None!")
    a = targetcalc(range, shooter, 0, False, 0, 0, firingmech, target, True)
    wepdmg = shooter.dmg
    if hasattr(shooter, "cluster") and not getattr(shooter, "cluster") is None:
        if allhit:
            wepdmg = docluster(shooter.dmg, shooter, firingmech, target, True, 12)
        else:
            wepdmg = docluster(shooter.dmg, shooter, firingmech, target, True, 7)
    if allhit:
        a = 1
        firingmech.heat -= shooter.heat
        print(a)
    if a == False:
        return
    firingmech.wepsfired.append(shooter.name)
    print(a, a*wepdmg)
    firingmech.heat += shooter.heat
    firingmech.dmgthisturn += (a * wepdmg)
    #print(a*shooter.dmg)

#protagonist = copy.deepcopy(awesome8q)
#testsubject2= copy.deepcopy(awesome8q)
#enemy = copy.deepcopy(awesome8q)
#enemy2 = copy.deepcopy(awesome8q)
Turns = []
crits = []
endtmm = []
dmgpershot = []
avgdmgs = {}
for i in range(20):
    exec(f"turn{i+1}dmg = []")
print(time.time()-StartTime)

def partgen(part, data):
    if not isinstance(part, str): raise(TypeError, "Error in partgen Function, part is not str")
    #print(data)
    partslots = {}
    global mechbits
    mtbits = ["-Empty-", '-Empty-']
    for idx, item in enumerate(data):
        #print(idx, item)
        slnum = idx + 1
        slnum = "slot" + str(slnum)
        i=item
        if "(omnipod)" in item.lower():
            # print(item)
            item = item[:-10]
            # print(item)
        item = item.strip()
        # print(item)
        if not slnum in partslots.keys():
            for list in mechbits:
                for value in list:
                    if item in value.ids:
                        if part.lower() == "head":
                            print(part, item)
                        #print(value.name, value.slots, part)
                        partslots.update({slnum : copy.deepcopy(value)})
                        print(value.name, part)
                        if value.slots > 1:
                            if (int(slnum[4:])+value.slots)-len(data) > 0:
                                print("There's gonna be some overflow here!")
                                #print(int(slnum[4:])+value.slots)-len(data)
                            for i in range(value.slots-1):
                                slnumfutur = "slot" +(str(idx+i+2))
                                partslots.update({slnumfutur:None})
            if not slnum in partslots.keys():
                if i in mtbits:
                    partslots[slnum] = None
                else:
                    partslots[slnum] = i
            partslots["Part"] = part
        #print(partslots)
    #print(partslots["slot3"] is partslots["slot4"])
    #print(partslots)
    return partslots
def mechgen(name, file, isprotag=False):
    strt = time.time()
    global mechbits
    case1=False
    case2=False
    mtbits = ["-Empty-"]
    struc20 = [6, 5, 3, 4]
    struc25 = [8, 6, 4, 6]
    struc30 = [10, 7, 5, 7]
    struc35 = [11, 8, 6, 8]
    struc40 = [12, 10, 6, 10]
    struc45 = [14, 11, 7, 11]
    struc50 = [16, 12, 8, 12]
    struc55 = [18, 13, 9, 13]
    struc60 = [20, 14, 10, 14]
    struc65 = [21, 15, 10, 15]
    struc70 = [22, 15, 11, 15]
    struc75 = [23, 16, 12, 16]
    struc80 = [25, 17, 13, 17]
    struc85 = [27, 18, 14, 18]
    struc90 = [29, 19, 15, 19]
    struc95 = [30, 20, 16, 20]
    struc100 = [31, 21, 17, 21]
    strucdict = {100:struc100, 95:struc95, 90:struc90, 85:struc85, 80:struc80, 75:struc75, 70:struc70, 65:struc65, 60:struc60, 55:struc55, 50:struc50, 45:struc45, 40:struc40, 35:struc35, 30:struc30, 25:struc25, 20:struc20}
    armdict = {}
    hdslots = {}
    mechname = "James"
    mechfile = open(file, "r", errors="ignore")
    mechdata = mechfile.readlines()
    #if not mechdata[4] == "Config:Biped\n":
    #    raise Exception("Only Battlemechs please, no quads or tris!")
    #mechname = mechdata[2].removesuffix("\n")
    for idx, item in enumerate(mechdata):
        pos = mechdata.index(item)
        if item.lower().startswith("chassis:"):
            item = item.removeprefix("chassis:")
            mechnamepart1 = item[:-1]
            #print(mechnamepart1)
            continue
        if item.lower().startswith("model:"):
            item = item[6:-1]
            mechnamepart2 = item
            #print(mechnamepart2)
        if item.lower().startswith("mass"):
            tonnage = int(item.removesuffix("\n")[-2:])
            #print(tonnage)
            if tonnage == 0: tonnage = 100
            struc=strucdict[tonnage]
        if item.lower().startswith("heat sinks"):
            if "double" in item.lower():
                isdouble=True
                #print("Double")
            else:
                isdouble=False
                #print("Single")
            #print(struc)
        if item.lower().startswith("armor"):
            for i in range(11):
                arm = mechdata[pos+i+1].removesuffix("\n")
                armdict[mechdata[pos+i+1][0:3].strip().lower()] = arm[-2:]
            for key, value in armdict.items():
                a=value.find(":")
                if a != -1:
                    armdict[key] = value[a+1:]
            for key, v in armdict.items():
                armdict[key] = int(v)
            #print(armdict)
        if item.lower().startswith("head"):
            partdata = [mechdata[pos+i+1][0:-1] for i in range(6)]
            head = partgen("Head", partdata)
            #print(f"{mechname} head is {head}")
        if item.lower().startswith("center torso"):
            partdata = [mechdata[idx+i+1][0:-1] for i in range(12)]
            ct = partgen("Center Torso", partdata)
            #print(f"{mechname} ct is {ct}")
        if item.lower().startswith("right torso"):
            partdata = [mechdata[idx+i+1][0:-1] for i in range(12)]
            rt = partgen("Right Torso", partdata)
            #print(f"{mechname} rt is {rt}")
        if item.lower().startswith("left torso"):
            partdata = [mechdata[idx + i + 1][0:-1] for i in range(12)]
            lt = partgen("Left Torso", partdata)
            #print(f"{mechname} lt is {lt}")
        if item.lower().startswith("left arm"):
            partdata = [mechdata[idx + i + 1][0:-1] for i in range(12)]
            la = partgen("Left Arm", partdata)
            #print(f"{mechname} la is {la}")
        if item.lower().startswith("right arm"):
            partdata = [mechdata[idx+i+1][0:-1] for i in range(12)]
            ra = partgen("Right Arm", partdata)
            #print(f"{mechname} ra is {ra}")
        if item.lower().startswith("left leg"):
            partdata = [mechdata[idx + i + 1][0:-1] for i in range(6)]
            ll = partgen("Left Leg", partdata)
            #print(f"{mechname} ll is {ll}")
        if item.lower().startswith("right leg"):
            partdata = [mechdata[idx+i+1][0:-1] for i in range(6)]
            rl = partgen("Right Leg", partdata)
            #print(f"{mechname} rl is {rl}")
        if item.lower().startswith("walk mp"):
            #print(item[8:])
            walk = int(item[8:])
        if item.startswith("model:"):
            mechname = item[6:-1]
            #print(mechname)
    mechname = mechnamepart1 + " " + mechnamepart2
    if isprotag:
        t=0
        print("Please enter your 'Mech's 4/5 BV")
        while isprotag:
            BV = input("> ")
            try:
                BV = int(BV)
                break
            except ValueError:
                if t==0: print("Please make sure it's just a plain ol' integer.")
                elif t==1: print("Please just write a normal number, no commas or decimals, nothing like that")
                elif t==2: print("Come on man, you gotta be screwing with me.")
                elif t==3: print("Alright listen, it's not that fucking hard. Just write. A fucking. NUMBER.")
                elif t==4 and BV.lower() == "a fucking. number.":
                    print("Come on man, just- Fucking hell you knew what I meant.")
                    continue
                elif t==4: print("Do you know what a number is? Can you just not think of one? Well there's a number for you, 1. Use it.")
                elif t==5 and BV == "1.": print("You're a clever fucker, aren't you?")
                elif t==5:print("No? That one's not good enough, is it? Christ you're a twat.")
                elif t==6: print("You're still here? Really? Bugger me, do you have nothing else to do? Just check your bloody Battlemech already. It's serious business you know.")
                else: print("I'm not doing this anymore. You know what I want, just do it or leave.")
                t+=1
    else:
        BV = 20
    #print(armdict)
    mechfile.close()
    mechhead = MechPart(f"{mechname} HD", armdict["hd"], 3, head["slot1"], head["slot2"], head["slot3"], head["slot4"], head["slot5"], head["slot6"], False, True)
    mechll = MechPart(f"{mechname} LL", armdict["ll"], struc[3], ll["slot1"], ll["slot2"], ll["slot3"], ll["slot4"],ll["slot5"], ll["slot6"])
    mechrl = MechPart(f"{mechname} RL", armdict["rl"], struc[3], rl["slot1"], rl["slot2"], rl["slot3"], rl["slot4"],rl["slot5"], rl["slot6"])
    mechla = MechPartBig(f"{mechname} LA", armdict["la"], 0, struc[2], la["slot1"], la["slot2"], la["slot3"], la["slot4"], la["slot5"], la["slot6"], la["slot7"], la["slot8"], la["slot9"], la["slot10"], la["slot11"], la["slot12"])
    mechra = MechPartBig(f"{mechname} RA", armdict["ra"], 0, struc[2], ra["slot1"], ra["slot2"], ra["slot3"], ra["slot4"],ra["slot5"], ra["slot6"], ra["slot7"], ra["slot8"], ra["slot9"], ra["slot10"], ra["slot11"], ra["slot12"])
    mechlt = MechPartBig(f"{mechname} LT", armdict["lt"], armdict["rtl"], struc[1], lt["slot1"], lt["slot2"], lt["slot3"], lt["slot4"],lt["slot5"], lt["slot6"], lt["slot7"], lt["slot8"], lt["slot9"], lt["slot10"], lt["slot11"], lt["slot12"])
    mechrt = MechPartBig(f"{mechname} RT", armdict["rt"], armdict["rtr"], struc[1], rt["slot1"], rt["slot2"], rt["slot3"], rt["slot4"],rt["slot5"], rt["slot6"], rt["slot7"], rt["slot8"], rt["slot9"], rt["slot10"], rt["slot11"], rt["slot12"])
    mechct = MechPartBig(f"{mechname} CT", armdict["ct"], armdict["rtc"], struc[0], ct["slot1"], ct["slot2"], ct["slot3"], ct["slot4"], ct["slot5"], ct["slot6"], ct["slot7"], ct["slot8"], ct["slot9"], ct["slot10"], ct["slot11"], ct["slot12"])
    mech = Battlemech(mechname, mechhead, mechla, mechra, mechll, mechrl, mechrt, mechlt, mechct, genericmechwarrior, walk, tonnage, case1, case2, isdouble, BV)
    print(f"Initializing {mechname} took {time.time()-strt} seconds")
    return mech
def simulator(simulcnt, protag, atk, dfnd):
    poslist = [21, 18, 15, 14, 12, 10, 9, 7, 6, 5, 3, 1]
    wepsfired = {f"turn{i+1}":[] for i in range(12)}
    starttime=time.time()
    heatturn = {f"turn{i+1}":[] for i in range(12)}
    optcalcdmg = {f"turn{i+1}":[] for i in range(12)}
    basecalcdmg = {f"turn{i + 1}": [] for i in range(12)}
    hotcalcdmg = {f"turn{i + 1}": [] for i in range(12)}
    tmms = {f"tmm{i+1}": [] for i in range(12)}
    turnsdmg = {f"turn{i+1}":[] for i in range(12)}
    #print(turnsdmg)
    #print(tmms)
    avgdmgbase = []
    avgdmgopt = {f"Gunnery {i}":[] for i in range(6)}
    prevhtopt = {f"Gunnery {i}":0 for i in range(6)}
    avgdmgred = []
    avgdmgalpha = []
    dfndname = dfnd.name
    deathturn = []
    defdeathturn = []
    CoDs = {"HKill":0, "PKill":0, "EKill":0, "TorsoEKill":0, "CTKill":0, "AmmoKill":0, "Survived":0}
    defCoDs = {"HKill":0, "PKill":0, "EKill":0, "TorsoEKill":0, "CTKill":0, "AmmoKill":0, "Survived":0}
    dmgpershot = []
    critspergame = []
    protagonistbase = copy.deepcopy(protag)
    protagonistopt = copy.deepcopy(protag)
    protagonistred = copy.deepcopy(protag)
    protagonistalpha = copy.deepcopy(protag)
    defender = copy.deepcopy(dfnd)
    qtestmeks = [copy.copy(protagonistbase), copy.copy(protagonistopt), copy.copy(protagonistred), copy.copy(protagonistalpha)]
    for i in range(12):
        defender.move(True)
        protagonistbase.move()
        protagonistopt.move()
        protagonistred.move()
        protagonistalpha.move()
        protagonistbase.pos = poslist[i]
        protagonistopt.pos = poslist[i]
        protagonistred.pos = poslist[i]
        protagonistalpha.pos = poslist[i]
        print(protagonistbase.pos)
        protagonistbase.barrage(defender, False, True, istest=True)
        for i in range(6):
            protagonistopt.heat = prevhtopt[f"Gunnery {i}"]+1
            protagonistopt.pilot.gskill = i
            protagonistopt.barrage(defender, False, False, istest=True)
            prevhtopt[f"Gunnery {i}"] = protagonistopt.heat
            avgdmgopt[f"Gunnery {i}"].append(protagonistopt.dmgthisturn)
            if not i == 5:
                protagonistopt.useammo(None, True)
        protagonistred.barrage(defender, True, False, istest=True)
        protagonistalpha.barrage(defender, False, False, istest=True, allhit=True)
        avgdmgbase.append(protagonistbase.dmgthisturn)
        avgdmgred.append(protagonistred.dmgthisturn)
        avgdmgalpha.append(protagonistalpha.dmgthisturn)
        protagonistalpha.heat = 0
    for i in range(simulcnt):
        critsthisgame = 0
        if i % int(simulcnt/40) == 0: print(i)
        protagonist = copy.deepcopy(protag)
        attacker = copy.deepcopy(atk)
        attacker.pilot.gskill = 4
        defender = copy.deepcopy(dfnd)
        for i in range(12):
            protagonist.turn +=1
            protagonist.move(True)
            if i !=0: attacker.move(False, isrunning=True)
            tmms[f"tmm{i + 1}"].append(protagonist.tmm)
            attacker.turn+=1
            attacker.pos = poslist[i]
            attacker.barrage(protagonist)
            if protagonist.isdead:
                #protagonist.printer()
                deathturn.append(i+1)
                if protagonist.causeofdeath == '':
                    if protagonist.ct.structure <= 0:
                        protagonist.causeofdeath = "CTKill"
                    elif protagonist.hd.structure <=0:
                        protagonist.causeofdeath = "HKill"
                    elif protagonist.enginehits >= 3:
                        protagonist.causeofdeath = "EKill"
                    else:
                        print("Uh Oh, soemthing not giving cause of death")
                        protagonist.causeofdeath = "CTKill"
                CoDs[protagonist.causeofdeath] +=1
                break
        if not protagonist.isdead:
            CoDs["Survived"] += 1
        protagonist = copy.deepcopy(protag)
        for i in range(12):
            defender.critsthisturn = 0
            protagonist.turn +=1
            defender.move(True)
            if i !=0: protagonist.move(False)
            defender.turn+=1
            protagonist.pos = poslist[i]
            protagonist.barrage(defender)
            critsthisgame += defender.critsthisturn
            if protagonist.dmgthisturn != 0:
                turnsdmg[f"turn{i+1}"].append(protagonist.dmgthisturn)
            for j in protagonist.dmgpershot:
                if j != 0:
                    dmgpershot.append(j)
            #print(protagonist.dmgthisturn)
            wepsfired[f"turn{i+1}"] = protagonist.wepsfired
            heatturn[f"turn{i + 1}"].append(protagonist.heat)
            if defender.isdead:
                defdeathturn.append(i+1)
                # defender.printer()
                if defender.causeofdeath == '':
                    if defender.ct.structure <= 0:
                        defender.causeofdeath = "CTKill"
                    elif defender.hd.structure <=0:
                        defender.causeofdeath = "HKill"
                    elif defender.enginehits >= 3:
                        defender.causeofdeath = "EKill"
                    else:
                        print("Uh Oh, soemthing not giving cvause of death")
                        defender.causeofdeath = "CTKill"
                defCoDs[defender.causeofdeath] +=1
                #print(turnsdmg)
                #print(dmgpershot)
                break
        if not defender.isdead:
            defCoDs["Survived"] += 1
        critspergame.append(critsthisgame)
    totmeandmg = 0
    testmed = 0
    for k, v in tmms.items():
        try:
            tmms[k] = mean(v)
        except:
            tmms[k] = 0
    for k, v in turnsdmg.items():
        a=[]
        #print(k, v)
        for i in v:
            if i != 0:
                a.append(i)
            else:
                continue
                #print(a)
        #print(a)
        try:
            turnsdmg[k] = median(v)
        except statistics.StatisticsError:
            turnsdmg[k] = 0
        #print(turnsdmg[k])
        try:
            totmeandmg += median(v)
            testmed += mean(v)
        except statistics.StatisticsError:
            pass
    # print(f"Meantest: {testmed}")
    for k, v in heatturn.items():
        #print(k, v)
        try:
            heatturn[k] = mean(v)
        except statistics.StatisticsError:
            heatturn[k] = 0
    #print(dmgpershot)
    #print(a)
    print(f"Mean {protag.name} Death Turn : {mean(deathturn)}")
    print(CoDs)
    print(f"Survival {str(CoDs["Survived"]/simulcnt*100)[0:5]}%")
    print(f"TMMs : {tmms}")
    try:
        print(f"Damage per shot : {median(dmgpershot)}")
    except:
        pass
    print(f"Mean Damage per turn : {turnsdmg}")
    print(f"Total Mean DMG : {totmeandmg}")
    print(f"Base AVGDMG: {sum(avgdmgbase)}")
    for k, v in avgdmgopt.items():
        print(k, sum(avgdmgopt[k]))
    print(f"Red ABGDMG: {sum(avgdmgred)}")
    print(f"ALPHA DMG: {sum(avgdmgalpha)}")
    print(f"Crits per Game : {median(critspergame)}, {mean(critspergame)}, {critspergame}")
    print(f"Weapons fired each turn: {wepsfired}")
    print(f"Heat per turn {heatturn}")
    print(f"Mean {dfndname} Death Turn: {median(defdeathturn)}, {mean(defdeathturn)}")
    print(f"Causes of death for {dfndname}: {defCoDs}")
    print(f"Survival {str(defCoDs["Survived"]/simulcnt*100)[0:5]}%")
    print(f"Program ran in {time.time()-starttime} seconds!")
    print(protagonist.sinking)
    #print(mechdata)
files = os.listdir()
for i in files:
    if i.lower().endswith("protagonist.mtf"):
        protagonist = i
    if i.strip().lower().endswith("attacker.mtf"):
        attacker = i
    if i.lower().endswith("target.mtf"):
        target = i

'''for i in range(1):
    critsthisgame = 0
    #print(i)
    if i % 100 == 0: print(i)
    enemy2 = copy.deepcopy(awesome8q)
    enemy2.pos = 0
    protagonist = copy.deepcopy(awesome8q)
    poslist = [21, 18, 15, 14, 12, 10, 9, 7, 6, 5, 3, 1]
    for i in range(12):
        enemy2.turn +=1
        protagonist.turn+=1
        enemy2.move(True)
        protagonist.move(False)
        protagonist.pos = poslist[i]
        #print(f"Turn {i+1}")
        protagonist.barrage(enemy2)
        #print(enemy2.heat)
        critsthisgame+=enemy2.critsthisturn
        exec(f"turn{i+1}dmg.append(protagonist.dmgthisturn)")
        dmgpershot.extend(protagonist.dmgpershot)
        if enemy2.isdead:
            #print(f"Enemy was destroyed in {i+1} turns!")
            Turns.append(i+1)
            endtmm.append(enemy2.tmm)
            if enemy2.causeofdeath == '':
                enemy2.causeofdeath = "CTKill"
            exec(f"CoDs[enemy2.causeofdeath] +=1")
            break
    if not enemy2.isdead:
        CoDs["Survived"] +=1
        endtmm.append(enemy2.tmm)
    crits.append(critsthisgame)

for i in range(20):
    try:
        exec(f"avgdmgs['turn{i+1}'] = mean(turn{i+1}dmg)")
    except:
        continue
totdmg=0
for key, value in avgdmgs.items():
    totdmg+=float(value)
print(f"Total Average Damage was {totdmg}!")
print(f"{mean(crits)} crits per game.")
print(f"{mean(avgdmgs.values())} damage per round!")
print(f"{mean(dmgpershot)} average damage per hit!")
print(CoDs)
print(f"Killing took on average {mean(Turns)} turns! \n with a stdev of {stdev(Turns)}")
print(f"Average end TMM was {mean(endtmm)}")


#EndTime = time.time()
print(f"The program took {int(time.time()-StartTime)} seconds!")'''
atk = mechgen("Apples", attacker, False)
#print(atk.name)
#print(atk.weplist)
protag = mechgen("Silly Lad", protagonist, True)
#print(type(protag.ll.armour))
#print(protag.weplist)
#print(protag.la.slot3 is protag.la.slot4)
defender = mechgen("Fodder", target, False)


simulator(40, protag, atk, defender)
#print(islrm15.ratio)
#print("merry christmas!")
#print(atk.name, atk.ct.qdir)