import random, math, pathlib, copy, time, os
from natsort import natsorted
from statistics import mean
from statistics import stdev
from math import floor
import statistics
StartTime = time.time()
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
clust25 = [8, 8, 10, 16, 16, 16, 16, 21 ,21, 25, 25]
clust26 = [9, 9, 11, 17, 17, 17, 17, 21, 21, 26, 26]
clust27 = [9, 9, 11, 17, 17, 17, 17, 22, 22, 27, 27]
clust28 = [9, 9, 11, 17, 17, 17, 17, 23, 23, 28, 28]
clust29 = [10, 10, 12, 18, 18, 18, 18, 23, 23, 29, 29]
clust30 = [10, 10, 12, 18, 18, 18, 18, 24, 24, 30, 30]
clust40 = [12, 12, 18, 24, 24, 24, 24, 32, 32, 40, 40]

def dooverflow(part, target=None):
    if part.name.lower()[-2:] == "hd":
        return "Mech Destroyed"
    elif part.name.lower()[-2] == "l":
        if part.name.lower()[-1] == "t":
            return target.ct
        else:
            return target.lt
    elif part.name.lower()[-2] == "r":
        if part.name.lower()[-1] =="t":
            return target.ct
        else:
            return target.rt
    elif part.name.lower()[-2] == "c":
        return "Mech Destroyed"
    else:
        print("OVERFLOW ERROR")
        return

def RollLocation(Float=True, HasCrit=False, Debug=False):
    Roll1 = random.randint(1, 6)
    if Debug:
        print(Roll1)
    Roll2 = random.randint(1, 6)
    if Debug:
        print(Roll2)
    Location = Roll1+Roll2
    if Debug:
        print(Location)
    if Location == 12:
        return "HD", HasCrit
    elif Location > 9:
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
            return RollLocation(True, True)

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

    def __init__(self, name, slots=1, isdamaged=False, isengine=False, isgyro=False):
        self.name = name
        self.slots = slots
        self.isdamaged = isdamaged
        self.hasexpanded = False
        self.isengine = isengine
        self.isgyro = isgyro

class HeatSink:
    def __init__(self, name, sinking = 1, slots = 1, isdamaged = False):
        self.name = name
        self.hasexpanded = False
        self.slots = slots
        self.isdamaged = isdamaged
        self.sinking = sinking

class AmmoBin(MechUtility):
    def __init__(self, name, ammonum, slots=1, isexplosive = True, damageperammo = 2, isdamaged=False):
        self.name = name
        self.slots = slots
        self.ammonum = int(ammonum)
        self.isdamaged = isdamaged
        self.isexplosive = isexplosive
        self.damageperammo = damageperammo
        self.location = ()
    def parthit(self, mek):
        if self.isexplosive and not self.ammonum == 0:
            explosiondamage = self.ammonum*self.damageperammo
            self.isdamaged = True
            print("BOOM!")
            return explosiondamage
        else:
            self.isdamaged = True
            return 0
class MechPart:

    def __init__(self, name, armour, structure, slot1=None, slot2=None, slot3=None, slot4=None, slot5=None, slot6=None, isdestroyed=False, ishead=False):
        self.name = name
        self.armour = armour
        self.structure = structure
        self.slot1 = slot1
        self.slot2 = slot2
        self.slot3 = slot3
        self.slot4 = slot4
        self.slot5 = slot5
        self.hasweps = False
        self.slot6 = slot6
        self.isdestroyed = isdestroyed
        self.ishead = ishead
        self.blasters = []
        self.hasammo = False
        self.ammoslots = []
        self.qdir = list(a for a in dir(self) if not a.startswith('__'))
        self.slotqdir = natsorted(list(a for a in dir(self) if a.startswith("slot")))
        #self.multislot()
        #self.listweps()
        self.slshit = []

    def listweps(self):
        for attr in self.slotqdir:
            attrvalue = getattr(self, attr)
            if isinstance(attrvalue, Weapon):
                self.blasters.append(attr)
                self.hasweps = True
            if isinstance(attrvalue, AmmoBin):
                self.ammoslots.append(attr)
                self.hasammo = True
        #print(self.ammoslots)

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
        if self.armour > 0:
            self.armour -= dmg
            if self.armour < 0:
                overspill = abs(self.armour)
                self.armour = 0
                self.structure -= overspill
                #print(f"{self.name} took {dmg-overspill} damage! {self.name}'s armour was stripped and the structure took {overspill} damage!")
                critnum = docriticals()
                if critnum > 0: mekself.critsthisturn+=1
                crit(self, critnum, mekself)
                if self.structure <= 0:
                    self.isdestroyed = True
                    if abs(self.structure) > 0:
                        overspill = abs(self.structure)
                        return overspill
                    return 0
                else:
                    return 0
            else:
                #print(f"{self.name} took {dmg} armour damage!")
                return 0
        elif not self.armour > 0:
            self.structure -= dmg
            #print(f"{self.name} took {dmg} structure damage!")
            critnum = int(docriticals())
            crit(self, critnum, mekself)
            if self.structure > 0:
                return 0
            if self.structure == 0:
                self.isdestroyed = True
                return 0
            if self.structure < 0:
                self.isdestroyed = True
                overspill = abs(self.structure)
                self.structure = 0
                return overspill




class MechPartBig(MechPart):
    def __init__(self, name, armour, reararmour, structure, slot1=None, slot2=None, slot3=None, slot4=None, slot5=None, slot6=None, slot7=None, slot8=None, slot9=None, slot10=None, slot11=None, slot12=None):
        self.reararmour = reararmour
        self.name = name
        self.armour = armour
        self.structure = structure
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
        self.hasweps = False
        self.qdir = list(a for a in dir(self) if not a.startswith('__'))
        self.slotqdir = list(a for a in dir(self) if a.startswith("slot"))
        self.slotqdir = natsorted(self.slotqdir)
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

    def __init__(self, name, srange, mrange, lrange, dmg, heat, damage_type = None, BV=0, slots=1, targetmod=0, minrange=0, isexplosive=False, xplodmg=0):
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
    def shoot(self):
        if self.hasfired:
            #print("Fuc")
            return
        #print("PEW!")
        self.hasfired = True
        return self, self.heat
    def ratiocalc(self, dmg, heat):
        try:
            self.ratio = dmg/heat
            return
        except ZeroDivisionError:
            self.ratio=0
class Missile(Weapon):
    def __init__ (self, name, srange, mrange, lrange, dmg, heat, damage_type = None, BV=0, slots = 1, targetmod =0, minrange=0, ammo=None, cluster=None, clustermod = 0, grouping=None, streak=False, artemis4=False, artemis5=False):
        #super.__init__(self, name, srange, mrange, lrange, dmg, heat, damage_type, BV, slots, targetmod, minrange, ammo, cluster)
        self.artemis4 = artemis4
        self.artemis5 = artemis5
        self.hasexpanded = False
        self.streak = streak
        self.grouping = grouping
        self.cluster = cluster
        self.clustermod = clustermod
        super().__init__(name, srange, mrange, lrange, dmg, heat)

class Autocannon(Weapon):
    def __init__(self, name, srange, mrange, lrange, dmg, heat, damage_type = None, BV=0, slots=1, targetmod=0, minrange=0, ammo = None, cluster = None, isexplosive=False, xplodmg=0, grouping = None):
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
    def shoot(self):
        self.hasfired = True
        return self.dmg, self.ammo, self.cluster

class Battlemech:
    def __init__(self, name, head, la, ra, ll, rl, rt, lt, ct, pilot, walkspeed, tonnage, case1=False, case2=False):
        self.name = name
        self.hd = head
        self.la = la
        self.ra = ra
        self.ll = ll
        self.rl = rl
        self.rt = rt
        self.lt = lt
        self.ct = ct
        self.pilot = pilot
        self.maxwalkspeed = walkspeed
        self.maxrunspeed =int(math.ceil(walkspeed*1.5))
        self.tonnage = tonnage
        self.weightclass = ""
        self.weightclasscalc()
        self.enginerating = tonnage*walkspeed
        self.basesinking = int(self.enginerating/25)
        self.heat = 0
        self.heatunsinked = 0
        self.currentheatmod = 0
        self.isdead = False
        self.enginehits = 0
        self.gyrohits = 0
        self.case1 = case1
        self.case2 = case2
        self.sensorhits = 0
        self.isimmobile = False
        self.jumpspeed = 0
        self.movementmod=0
        self.sinking=0
        self.psrmalusperm = 0
        self.psrmalustemp = 0
        self.walkspeed = walkspeed
        self.runspeed = self.maxrunspeed
        self.heatmalus = 0
        self.causeofdeath = ""
        self.pos = 0
        self.weplist = []
        self.ammolist = []
        self.dmgthisturn = 0
        self.dmgpershot = []
        self.tmm = 0
        self.critsthisturn = 0
        self.qdir = list(a for a in dir(self) if not a.startswith('__'))
        self.hiphits = 0
        self.sinkingcalculator()
        self.parts = ["la", "ra", "ll", "rl", "rt", "lt", "ct"]
        #self.wepsandammogetter()
        self.motives = {}
        self.turn = 0
        self.multislot()

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
                self.lt.multislot(i)
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


    def shutdown(self, target, guaranteed):
        pass

    def move(self, evading=False, enemy=None):
        if not evading:
            self.movementmod=1
            self.heat +=1
        lranges = []
        mranges = []
        sranges = []
        runtmm = 0
        jumptmm = 0
        if evading:
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
            if self.jumpspeed > 0:
                pass
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
                    if not ammo.isdamaged:
                        #print(ammo)
                        exec(f"self.ammolist.append('{attrval.name.lower()[-2:]} {i}')")
        #self.weplist = [attr for attr in dir(self) if isinstance(getattr(self, attr), MechPart) and getattr(getattr(self, attr),'hasweps') and not getattr(getattr(self, attr), 'isdestroyed')]


    def resolvedamage(self, dmg, location, hascrit=False):
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
            self.la.structure = 0
            self.la.armour = 0
        if self.rt.isdestroyed:
            self.ra.isdestroyed = True
            self.ra.structure = 0
            self.ra.armour = 0
        if dmg == 0:
            return
        if location == self.hd:
            self.pilot.DoPilotDamage()
            if self.pilot.isdead:
                self.isdead = True
                self.causeofdeath = "PKill"
        o = location.TakeDamage(dmg, hascrit, self)
        if o > 0:
            newloc = dooverflow(location, self)
            #print(newloc)
            if newloc == "Mech Destroyed":
                self.isdead = True
                #print("Dead as fuck BROOOO")
            else:
                newloc = getattr(self, newloc.name.lower()[-2:])
                self.resolvedamage(o, newloc)
        self.motivecalc()

    def doammoexplosion(self, target):
        pass
    def heatresolution(self):
        self.sinkingcalculator()
        self.heat = self.heat - self.sinking
        self.walkspeed = self.maxwalkspeed - (int(self.heat/5))
        self.runspeed = math.ceil(self.walkspeed * 1.5)
        self.heatmalus = 0
        if self.heat == 30:
            self.shutdown()
        if self.heat < 0:
            self.heat = 0
        #elif 30 > self.heat >

    def barrage(self, target, alphastrike=False, heatneutral=False, range=1):
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
            a = targetcalc(range, wep, self.pilot.gskill, False, self.currentheatmod, self.movementmod, self, target)
            guns2fire[f"{loc} {slot}"] = wep.ratio*a
            sorted_guns2fire = sorted(guns2fire.items(), key=lambda x: x[1], reverse=True)
            guns2fire = dict(sorted_guns2fire)
        #print(guns2fire)
        for key in guns2fire:
            loc = key[0:2].lower()
            slot = key[-6:].strip()
            loc =getattr(self, loc)
            wep= getattr(loc, slot)#:3#
            shotht = wep.heat + self.heat - self.sinking
            if shotht < 8 and not alphastrike and not wep.hasfired and not wep.isdamaged and not heatneutral:
                exec(f"fire(range, wep, self.pilot.gskill, False, self.currentheatmod, self.movementmod, self, target)")
                wep.hasfired = True
            elif shotht >= 8 and not alphastrike and not wep.hasfired and not wep.isdamaged and not heatneutral:
                #print(f"Leaving {wep.name} off to save heat!")
                continue
            if heatneutral:
                if shotht < 4 and not alphastrike and not wep.hasfired and not wep.isdamaged and heatneutral:
                    exec(f"fire(range, wep, self.pilot.gskill, False, self.currentheatmod, self.movementmod, self, target)")
                    wep.hasfired = True
                    continue
            if alphastrike:
                if shotht < 29 and alphastrike and not heatneutral and not wep.hasfired and not wep.isdamaged:
                    exec(f"fire(range, wep, self.pilot.gskill, False, self.currentheatmod, self.movementmod, self, target)")
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
        self.sinking = self.basesinking + heatsinkssinking - (self.gyrohits * 5)

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
    def useammo(self, wep):
        #print("Using Ammo")
        firedgood = False
        for i in self.ammolist:
            loc =i[0:2].lower()
            slot = i[-6:].strip()
            loc = getattr(self ,loc)
            ammo = getattr(loc, slot)
            if ammo.name == wep.ammo and not getattr(loc, 'isdestroyed'):
                if ammo.ammonum > 0:
                    #print(ammo.ammonum)
                    #print(f"{wep.name} fired!")
                    ammo.ammonum-=1
                    #print(ammo.ammonum)
                    firedgood = True
                    return firedgood
                else:
                    continue
        return firedgood





#Mech Utility
heatsink = HeatSink("Single Heatsink")
isdoubleheatsink = HeatSink("Double Heatsink", 2, 3)
clandoubleheatsink = HeatSink("Double Heatsink", 2, 2)
fusengine = MechUtility("Fusion Engine", 1, False, True, )
gyro = MechUtility("Gyro", 1, False, False, True)
MechUtils = {"Gyro":gyro, "Fusion Engine":fusengine, "Heat Sink":heatsink, "ISDouble Heat Sink":isdoubleheatsink, "CLDoubleHeatSink (omnipod)":clandoubleheatsink, "CLDoubleHeatSink":clandoubleheatsink}

#Ammo Bins
mgammo = AmmoBin("MG Ammo", 200, 1, True, 2)
mghalfammo = AmmoBin("MG Ammo", 100, 1, True, 2)
ac2ammo = AmmoBin("AC2 Ammo", 45, 1, True, 2)
ac5ammo = AmmoBin("AC5 Ammo", 20, 1, True, 5)
ac10ammo = AmmoBin("AC10 Ammo", 10, 1, True, 10)
ac20ammo = AmmoBin("AC20 Ammo", 5, 1, True, 20)
srm2ammo = AmmoBin("SRM2 Ammo", 50, 1, True, 4)
srm4ammo = AmmoBin("SRM4 Ammo", 25, 1, True, 8)
srm6ammo = AmmoBin("SRM6 Ammo", 15, 1, True, 12)
MechAmmo = {"IS Ammo SRM-6":srm6ammo, "IS Ammo SRM-4":srm4ammo, "IS Ammo SRM-2":srm2ammo, "IS Ammo MG - Full":mgammo, "IS Ammo MG - Half":mghalfammo}

#Lasers
largelaser = Weapon("Large Laser", 5, 10, 15, 8, 8, "DE", 123, 2)
iserlargelaser = Weapon("ER Large Laser", 7, 14, 19, 8, 12, "DE", 163, 2)
clanerlargelaser = Weapon("ER Large Laser", 8, 15, 25, 10, 12, "DE", 248)
isplargelaser = Weapon("Large Pulse Laser", 3, 7, 10, 9, 10, "P", 119, 2, -2)
clanplargelaser = Weapon("Large Pulse Laser", 6, 14, 20, 10, 10, "P", 265, 2, (-2))
erplargelaser = Weapon("ER Large Pulse Laser", 7, 15, 23, 10, 13, "P", 272, 3, (-1))
mediumlaser = Weapon("Medium Laser", 3, 6, 9, 5, 3, "DE", 46)
ispmediumlaser = Weapon("Medium Pulse Laser", 2, 4, 6, 6, 4, "P", 48, 1, (-2))
clanpmediumlaser = Weapon("Medium Pulse Laser", 4, 8, 12, 7, 4, "P", 111, 1, (-2))
isermediumlaser = Weapon("ER Medium Laser", 4, 8, 12, 5, 5, "DE", 62)
clanermediumlaser = Weapon("ER Medium Laser", 5, 10, 15, 7, 5, "DE", 108)
erpmediumlaser = Weapon("ER Medium Pulse Laser", 5, 9, 14, 7, 6, "P", 117, 2, (-1))
smalllaser = Weapon("Small Laser", 1, 2, 3, 3, 1, "DE", 9)
ispsmalllaser = Weapon("Small Pulse Laser", 1, 2, 3, 3, 2, "P", 12, 1, (-2))
clanpsmalllaser = Weapon("Small Pulse Laser", 2, 4, 6, 3, 2, "P", 24, 1, (-2))
clanersmalllaser = Weapon("ER Small Laser", 2, 4, 6, 5, 2, "DE", 31)
isersmalllaser = Weapon("ER Small Laser", 2, 4, 5, 3, 2, "DE", 17)
erpsmalllaser = Weapon("ER Small Pulse Laser", 2, 4, 6, 5, 3, None, 36, 1, (-1))
Lasers = {"Large Laser":largelaser,"ISLarge Laser":largelaser, "Medium Laser":mediumlaser, "Small Laser":smalllaser, "ISSmallLaser":smalllaser, "ISMediumLaser":mediumlaser,"ISLargePulseLaser":isplargelaser}

#PPCs
ppc = Weapon("PPC", 6, 12, 18, 10, 10, "DE", 176, 3, 0, 3)
iserppc = Weapon("ERPPC", 7, 14, 23, 10, 15, "DE", 228, 3, 0, 0)
clanerppc = Weapon("ERPPC", 7, 14, 23, 15, 15, "DE", 412, 2, 0, 0)
heavyppc = Weapon("Heavy PPC", 6, 12, 18, 15, 15, "DE", 317, 4, 0, 3)
PPCs = {"PPC":ppc, "CLERPPC (omnipod)":clanerppc, "CLERPPC":clanerppc, "ISERPPC":iserppc}

#Ballistics
machinegun = Autocannon("Machine Gun", 1, 2, 3, 2, 0, "AI", 20, 1, 0, 0, "MG Ammo")
Ballistics = {"Machine Gun":machinegun}

#Missiles
srm2 = Missile("SRM 2", 3, 6, 9, 2, 2, "Cluster", 21, 1, 0, 0, "SRM2 Ammo", 2, 0, 1, False, False)
isssrm2 = Missile("Streak SRM 2", 3, 6, 9, 2, 2, "Cluster", 30, 1, 0, 0, "SRM2 Ammo", 2, 0, 1, True, False, False)
clanssrm2 = Missile("Streak SRM 2", 4, 8, 12, 2, 2, "Cluster", 40, 1, 0, 0, "SRM2 Ammo", 2, 0, 1, True)
srm4 = Missile("SRM 4", 3, 6, 9, 2, 3, "Cluster", 39, 1, 0, 0, "SRM4 Ammo", 4, 0, 1)
isssrm4 = Missile("Streak SRM 4", 3, 6, 9, 2, 3, "Cluster", 59, 1, 0, 0, "SRM4 Ammo", 4, 0, 1, True)
clanssrm4 = Missile("Streak SRM 4", 4, 8, 12, 2, 3, "Cluster", 59, 1, 0, 0, "SRM4 Ammo", 4, 0, 1, True)
issrm6 = Missile("SRM 6", 3, 6, 9, 2, 4, "Cluster", 59, 2, 0, 0, "SRM6 Ammo", 6, 0, 1)
MechMissiles = {"SRM 2":srm2, "SRM 4":srm4, "SRM 6":issrm6}
#'Mech Bits
awesomehead8q = MechPart("Awesome HD", 9, 3, "Life Support", "Sensors", "Cockpit", copy.deepcopy(smalllaser), "Sensors", "Life Support", False, True)
awesomeleftleg8q = MechPart("Awesome LL", 33, 17, "Hip", "Upper Leg", "Lower Leg", "Foot", copy.deepcopy(heatsink), copy.deepcopy(heatsink))
awesomerightleg8q = MechPart("Awesome RL", 33, 17, "Hip", "Upper Leg", "Lower Leg", "Foot", copy.deepcopy(heatsink), copy.deepcopy(heatsink))
awesomerightarm8q = MechPartBig("Awesome RA", 24, 0, 13, "Shoulder", "Upper Arm", "Lower Arm", copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(ppc))
awesomeleftarm8q = MechPartBig("Awesome LA", 24, 0, 13, "Shoulder", "Upper Arm", "Lower Arm", "Hand")
awesomerighttorso8q = MechPartBig("Awesome RT", 24, 10, 17, copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(ppc))
awesomelefttorso8q = MechPartBig("Awesome LT", 24, 10, 17, copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(heatsink), copy.deepcopy(ppc))
awesomecentretorso8q = MechPartBig("Awesome CT", 30, 19, 25, copy.deepcopy(fusengine), copy.deepcopy(fusengine), copy.deepcopy(fusengine), copy.deepcopy(gyro), copy.deepcopy(gyro), copy.deepcopy(gyro), copy.deepcopy(gyro), copy.deepcopy(fusengine), copy.deepcopy(fusengine), copy.deepcopy(fusengine), copy.deepcopy(heatsink), copy.deepcopy(heatsink))
thunderbolt5srightarm = MechPartBig("Thunderbolt RA", 20, 0, 10, "Shoulder", "Upper Arm", "Lower Arm", "Hand", copy.deepcopy(largelaser))

#Mechwarriors
genericmechwarrior = Pilot("David B.", 5, 2)

#Battlemechs
#awesome8q = Battlemech("Awesome 8Q", awesomehead8q, awesomeleftarm8q, awesomerightarm8q, awesomeleftleg8q, awesomerightleg8q, awesomerighttorso8q, awesomelefttorso8q, awesomecentretorso8q, genericmechwarrior, 3, 80)

mechbits = [MechUtils, PPCs, Lasers, MechMissiles, MechAmmo, Ballistics]

def fire(range, shooter, skill, allhit=False, heatmod=0, movemod=0, firingmech=None, target=None):
    target.turn+=0.00000001
    range = int(range)
    skill = int(skill)
    if shooter.hasfired == True:
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
                #print("Click!")
                return
        else:
            raise(f"{shooter.name} has attr ammo, but Ammo is set to None!")
    hittarget = skill + rmod + shooter.targetmod + heatmod + movemod + target.tmm
    firingmech.heat += shooter.heat
    if allhit:
        hittarget = 0
    roll = random.randint(1, 6) + random.randint(1, 6)
    #print(rmod, roll, hittarget, range, shooter.name, target.tmm, movemod, skill)
    if roll >= hittarget:
        #print("Hit with " + shooter.name + "!")
        if hasattr(shooter, 'cluster') and shooter.cluster != None:
            docluster(shooter.dmg, shooter, firingmech, target)
            return
        hitloc = RollLocation()
        #print(shooter.dmg, "damage to enemy", hitloc[0] + "!")
        loc = hitloc[0]
        loc = loc[-2:].lower()
        #print(loc)
        loc = getattr(target, loc)
        shooter.hit = True
        firingmech.dmgthisturn += shooter.dmg
        firingmech.dmgpershot.append(shooter.dmg)
        target.resolvedamage(shooter.dmg, loc, hitloc[1])
    else:
        #print(f"Miss with {shooter.name}!")
        return "Miss!"

def crit(target, critnum, mek):
    critoverflow = 0
    if isinstance(target, str):
        return
    if critnum == 3:
        a = lambda l:target.name.lower()[-2:] == l
        if a('hd') or a('ll') or a('rl') or a('la') or a(r'a'):
            #print("Wow")
            target.isdestroyed = True
            if a('hd'):
                mek.isdead = True
                mek.causeofdeath = ('HKill')
                #print("Wowie")
            return
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
        if getattr(target, location) == None:
            if z > 50:
                if target.name.lower()[-2:] =="ct":
                    mek.isdead = True
                    mek.causeofdeath = "CTKill"
                    return
                break
            z+=1
            continue
        elif isinstance(a, str):
            if a == "Cockpit":
                mek.isdead = True
                mek.causeofdeath = "HKill"
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
            times=times+1
            #print(times)
            #print(z)
            z += 1
            setattr(a, 'isdamaged', True)
            if hasattr(a, 'isengine'):
                if getattr(a, 'isengine'):
                    mek.enginehits += 1
                    if mek.enginehits >=3:
                        mek.isdead = True
                        mek.causeofdeath = "EKill"
                        return
            if isinstance(a, AmmoBin):
                mek.resolvedamage(a.parthit(mek), target)
                if mek.isdead:
                    mek.causeofdeath = ("AmmoKill")
            #print(getattr(a, 'isdamaged'))
            setattr(target, location, None)
            continue
    crit(dooverflow(target, mek), (critoverflow), mek)

def docluster(dmg=0, weapon=None, firingmech=None, target=None):
    roll = random.randint(1, 6) + random.randint(1, 6)
    roll+=weapon.clustermod
    if weapon.artemis4: roll +=2
    if weapon.artemis5: roll +=3
    if roll > 12: roll = 12
    if weapon.streak:
        roll = 12
    cluster = "a"
    ldict = {}
    exec(f"cluster = clust{weapon.cluster}", globals(), ldict)
    cluster = ldict['cluster']
    #print(cluster)
    roll -=2
    #print(cluster[roll] // weapon.grouping)
    hitloc = RollLocation()
    loc = hitloc[0]
    loc = loc[-2:].lower()
    loc = getattr(target, loc)
    weapon.hit = True
    for i in range(cluster[roll]//weapon.grouping):
        hitloc = RollLocation()
        loc = hitloc[0]
        loc = loc[-2:].lower()
        loc = getattr(target, loc)
        #print(f"One missile from {weapon.name} hit target's {loc.name}!")
        target.resolvedamage((dmg*weapon.grouping), loc, hitloc[1])
    if cluster[roll]%weapon.grouping != 0:
        hitloc = RollLocation()
        loc = hitloc[0]
        loc = loc[-2:].lower()
        loc = getattr(target, loc)
        target.resolvedamage(int(dmg * cluster[roll]%weapon.grouping), loc, hitloc[1])


def targetcalc(range, shooter, skill, allhit=False, heatmod=0, movemod=0, firingmech=None, target=None):
    if range <= shooter.minrange:
        rmod = (shooter.minrange - range)+1
        #print(rmod)
    elif range <= shooter.srange:
        rmod = 0
    elif range <= shooter.mrange:
        rmod = 2
    elif range <= shooter.lrange:
        rmod = 4
    else:
        rmod = 10000
    hittarget = rmod + shooter.targetmod + firingmech.pilot.gskill + heatmod + movemod + target.tmm
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
        return 0.000001


#protagonist = copy.deepcopy(awesome8q)
#testsubject2= copy.deepcopy(awesome8q)
#enemy = copy.deepcopy(awesome8q)
#enemy2 = copy.deepcopy(awesome8q)
CoDs = {"HKill":0, "PKill":0, "EKill":0, "CTKill":0, "AmmoKill":0, "Survived":0}
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
        if not slnum in partslots.keys():
            for dicts in mechbits:
                for key, value in dicts.items():
                    if key.lower() == item.lower():
                        partslots.update({slnum : copy.deepcopy(value)})
                        if value.slots > 1:
                            if (int(slnum[4:])+value.slots)-len(data) > 0:
                                print("There's gonna be some overflow here!")
                            for i in range(value.slots-1):
                                slnumfutur = "slot" +(str(idx+i+2))
                                partslots.update({slnumfutur:None})
            if not slnum in partslots.keys():
                if i in mtbits:
                    partslots[slnum] = None
                else:
                    partslots[slnum] = i
            partslots["Part"] = part
    #print(partslots["slot3"] is partslots["slot4"])
    #print(partslots)
    return partslots
def mechgen(name, file, isprotag=False):
    strt = time.time()
    global mechbits
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
    mechfile = open(file, "r")
    mechdata = mechfile.readlines()
    if not mechdata[4] == "Config:Biped\n":
        raise Exception("Only Battlemechs please, no quads or tris!")
    mechname = mechdata[2].removesuffix("\n")
    for idx, item in enumerate(mechdata):
        pos = mechdata.index(item)
        if item.lower().startswith("mass"):
            tonnage = int(item.removesuffix("\n")[-2:])
            #print(tonnage)
            struc=strucdict[tonnage]
            #print(struc)
        if item.lower().startswith("armor"):
            print(item)
            for i in range(11):
                arm = mechdata[pos+i+1].removesuffix("\n")
                armdict[mechdata[pos+i+1][0:3].strip().lower()] = arm[-2:]
            for key, value in armdict.items():
                a=value.find(":")
                if a != -1:
                    armdict[key] = value[a+1:]
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
            print(mechname)
    if isprotag:
        print("Please enter your 'Mech's BV")
        while isprotag:
            BV = input("> ")
            try:
                BV = int(BV)
                break
            except ValueError:
                print("Please make sure it's just a plain int")
    else:
        BV = 20
    #print(armdict)
    mechhead = MechPart(f"{mechname} HD", armdict["hd"], 3, head["slot1"], head["slot2"], head["slot3"], head["slot4"], head["slot5"], head["slot6"], False, True)
    mechll = MechPartBig(f"{mechname} LL", armdict["ll"], struc[3], ll["slot1"], ll["slot2"], ll["slot3"], ll["slot4"],ll["slot5"], ll["slot6"])
    mechrl = MechPartBig(f"{mechname} RL", armdict["rl"], struc[3], rl["slot1"], rl["slot2"], rl["slot3"], rl["slot4"],rl["slot5"], rl["slot6"])
    mechla = MechPartBig(f"{mechname} LA", armdict["la"], 0, struc[2], la["slot1"], la["slot2"], la["slot3"], la["slot4"], la["slot5"], la["slot6"], la["slot7"], la["slot8"], la["slot9"], la["slot10"], la["slot11"], la["slot12"])
    mechra = MechPartBig(f"{mechname} RA", armdict["ra"], 0, struc[2], ra["slot1"], ra["slot2"], ra["slot3"], ra["slot4"],ra["slot5"], ra["slot6"], ra["slot7"], ra["slot8"], ra["slot9"], ra["slot10"], ra["slot11"], ra["slot12"])
    mechlt = MechPartBig(f"{mechname} LT", armdict["lt"], armdict["rtl"], struc[1], lt["slot1"], lt["slot2"], lt["slot3"], lt["slot4"],lt["slot5"], lt["slot6"], lt["slot7"], lt["slot8"], lt["slot9"], lt["slot10"], lt["slot11"], lt["slot12"])
    mechrt = MechPartBig(f"{mechname} RT", armdict["rt"], armdict["rtr"], struc[1], rt["slot1"], rt["slot2"], rt["slot3"], rt["slot4"],rt["slot5"], rt["slot6"], rt["slot7"], rt["slot8"], rt["slot9"], rt["slot10"], rt["slot11"], rt["slot12"])
    mechct = MechPartBig(f"{mechname} CT", armdict["ct"], armdict["rtc"], struc[0], ct["slot1"], ct["slot2"], ct["slot3"], ct["slot4"], ct["slot5"], ct["slot6"], ct["slot7"], ct["slot8"], ct["slot9"], ct["slot10"], ct["slot11"], ct["slot12"])
    mech = Battlemech(mechname, mechhead, mechla, mechra, mechll, mechrl, mechrt, mechlt, mechct, genericmechwarrior, walk, tonnage)
    print(f"Initializing {mechname} took {time.time()-strt} seconds")
    return mech

    #print(mechdata)
files = os.listdir()
for i in files:
    if i.lower().endswith("protagonist.mtf"):
        protagonist = i
    if i.strip().lower().endswith("attacker.mtf"):
        attacker = i
    if i.lower().endswith("target.mtf"):
        target = i
Bingus = mechgen("Apples", attacker, False)
print(Bingus.name)
print(Bingus.weplist)


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
