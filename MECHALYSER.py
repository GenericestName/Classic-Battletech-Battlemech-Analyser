import random, math, pathlib, copy, time
from statistics import mean
from statistics import stdev
import statistics
StartTime = time.time()

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
        self.isengine = isengine
        self.isgyro = isgyro

class HeatSink:
    def __init__(self, name, sinking = 1, slots = 1, isdamaged = False):
        self.name = name
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
        self.multislot()
        self.blasters = []
        self.listweps()
        self.slotshit = []

    def listweps(self):
        for attr in dir(self):
            attrvalue = getattr(self, attr)
            if isinstance(attrvalue, Weapon):
                self.blasters.append(attr)
                self.hasweps = True
    def multislot(self):
        #if isinstance(self, MechPartBig):
           # return
        slotsdic = {}
        for attr_name in dir(self):
            if not attr_name.startswith("__") and not attr_name == "structure":
                attrvalue = (getattr(self, attr_name))
                if isinstance(attrvalue, Weapon) and getattr(attrvalue, "slots") > 1 or isinstance(attrvalue, MechUtility) and getattr(attrvalue, "slots") > 1:
                    #print(f"{attr_name} is {attrvalue.name}")
                    slotsdic[attr_name] = attrvalue.slots
        if not len(slotsdic) == 0:
            for key, value in slotsdic.items():
                slotnum = int(key[4:])
                for i in range((slotnum) + 1, slotnum + int(value)):
                    higherslotname = f"slot{i}"
                    if getattr(self, higherslotname) == None:
                        setattr(self, higherslotname, getattr(self, key))
                        attrvalue = getattr(self, higherslotname)
                        #print(f"{higherslotname} of {self.name} is now bound to that {attrvalue.name}!")


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
        self.slotshit = []
        self.hasweps = False
        self.multislot()
        self.listweps()

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
class Autocannon(Weapon):
    def __init__(self, name, srange, mrange, lrange, dmg, heat, damage_type = None, BV=0, slots=1, targetmod=0, minrange=0, ammo = None, cluster = None, isexplosive=False, xplodmg=0):
        self.name = name
        self.minrange = minrange
        self.srange = srange
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
        self.sinkingcalculator()
        self.walkspeed = walkspeed
        self.runspeed = self.maxrunspeed
        self.heatmalus = 0
        self.causeofdeath = ""
        self.pos = 0
        self.weplist = []
        self.dmgthisturn = 0
        self.tmm = 0
        self.critsthisturn = 0
        self.wepsgetter()

    def shutdown(self, target, guaranteed):
        pass
    def move(self, evading=False, enemy=None):
        lranges = []
        mranges = []
        sranges = []
        runtmm = 0
        jumptmm = 0
        if evading:
            if 2 < self.runspeed < 5:
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
    def wepsgetter(self):
        for attr in dir(self):
            attrval = getattr(self, attr)
            if isinstance(attrval, MechPart) and getattr(attrval, 'hasweps'):
                for shots in attrval.blasters:
                    wep = getattr(attrval, shots)
                    exec(f"self.weplist.append('{attrval.name.lower()[-2:]} {shots}')")


    def resolvedamage(self, dmg, location, hascrit=False):
        if self.hd.isdestroyed:
            self.isdead = True
            self.causeofdeath = "HKill"
            return
        if self.ct.isdestroyed:
            self.isdead = True
            self.causeofdeath = "CTKill"
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
        #elif 30 > self.heat >

    def barrage(self, target, alphastrike=False, heatneutral=False, range=1):
        self.dmgthisturn = 0
        self.movementmod = 1
        guns2fire = {}
        range = (self.pos)-(target.pos)
        for attr in dir(self):
            attrval = getattr(self, attr)
            if isinstance(attrval, MechPart) and getattr(attrval, 'hasweps'):
                for shots in attrval.blasters:
                    wep = getattr(attrval, shots)#:3
                    a = targetcalc(range, wep, self.pilot.gskill, False, self.currentheatmod, self.movementmod, self, target)
                    guns2fire[f"{attrval.name.lower()[-2:]} {shots}"] = wep.ratio*a
                sorted_guns2fire = sorted(guns2fire.items(), key=lambda x: x[1], reverse=True)
                guns2fire = dict(sorted_guns2fire)
        #print(guns2fire)
        for key in guns2fire:
            loc = key[0:2].lower()
            slot = key[-6:].strip()
            loc =getattr(self, loc)
            wep= getattr(loc, slot)#:3#
            if wep.heat + self.heat - self.sinking < 8 and not alphastrike and not wep.hasfired and not wep.isdamaged and not heatneutral:
                exec(f"fire(range, wep, self.pilot.gskill, False, self.currentheatmod, self.movementmod, self, target)")
                wep.hasfired = True
            elif wep.heat+self.heat-self.sinking >= 8 and not alphastrike and not wep.hasfired and not wep.isdamaged and not heatneutral:
                #print(f"Leaving {wep.name} off to save heat!")
                continue
            if heatneutral:
                if (wep.heat + self.heat - self.sinking) > 4 and not alphastrike and not wep.hasfired and not wep.isdamaged and heatneutral:
                    exec(f"fire(range, wep, self.pilot.gskill, False, self.currentheatmod, self.movementmod, self, target)")
                    wep.hasfired = True
                    if wep.hit:
                        self.dmgthisturn += wep.dmg
                    continue
            if alphastrike:
                if (wep.heat + self.heat - self.sinking) > 29 and alphastrike and not heatneutral and not wep.hasfired and not wep.isdamaged:
                    exec(f"fire(range, wep, self.pilot.gskill, False, self.currentheatmod, self.movementmod, self, target)")
                    wep.hasfired = True
                    if wep.hit:
                        self.dmgthisturn += wep.dmg
                    continue
            else:
                continue

        for attr in dir(self): #Resetting weapons to unfired state for next turn
            attrval = getattr(self, attr)
            if isinstance(attrval, MechPart) and getattr(attrval, 'hasweps'):
                for shots in attrval.blasters:
                    exec(f"attrval.{shots}.hasfired = False")
                    exec(f"attrval.{shots}.hashit = False")
        self.heatresolution()

    def sinkingcalculator(self):
        heatsinkssinking = 0
        for attr in dir(self):
            attrval = getattr(self, attr)
            if isinstance(attrval, MechPart):
                for attrvals in dir(attrval):
                    attrvalue = (getattr(attrval, attrvals))
                    if isinstance(attrvalue, HeatSink) and not attrvalue.isdamaged:
                        heatsinkssinking += attrvalue.sinking
        self.sinking = self.basesinking + heatsinkssinking - (self.gyrohits * 5)

    def weightclasscalc(self):
        if self.tonnage <= 15:
            self.weightclass = "Proto"
        if self.tonnage <= 35:
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





#Mech Utility
heatsink = HeatSink("Single Heatsink")
isdoubleheatsink = HeatSink("Double Heatsink", 2, 3)
clandoubleheatsink = HeatSink("Double Heatsink", 2, 2)
fusengine = MechUtility("Fusion Engine", 1, False, True, )
gyro = MechUtility("Gyro", 1, False, False, True)

#Ammo Bins
mgammo = AmmoBin("MG Ammo", 100, 1)
ac10ammo = AmmoBin("AC10 Ammo", 10, 1, True, 10)

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

#PPCs
ppc = Weapon("PPC", 6, 12, 18, 10, 10, "DE", 176, 3, 0, 3)
iserppc = Weapon("ERPPC", 7, 14, 23, 10, 15, "DE", 228, 3, 0, 0)
clanerppc = Weapon("ERPPC", 7, 14, 23, 15, 15, "DE", 412, 2, 0, 0)
heavyppc = Weapon("Heavy PPC", 6, 12, 18, 15, 15, "DE", 317, 4, 0, 3)

#Ballistics
machinegun = Autocannon("Machine Gun", 1, 2, 3, 2, 0, "AI", 20, 1, 0, 0, "MG Ammo")

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
awesome8q = Battlemech("Awesome 8Q", awesomehead8q, awesomeleftarm8q, awesomerightarm8q, awesomeleftleg8q, awesomerightleg8q, awesomerighttorso8q, awesomelefttorso8q, awesomecentretorso8q, genericmechwarrior, 3, 80)



def fire(range, shooter, skill, allhit=False, heatmod=0, movemod=0, firingmech=None, target=None):
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
    hittarget = skill + rmod + shooter.targetmod + heatmod + movemod + target.tmm
    firingmech.heat += shooter.heat
    if allhit:
        hittarget = 0
    roll = random.randint(1, 6) + random.randint(1, 6)
    #print(rmod, roll, hittarget, range, shooter.name, target.tmm, movemod)
    if roll >= hittarget:
        #print("Hit with " + shooter.name + "!")
        hitloc = RollLocation()
        #print(shooter.dmg, "damage to enemy", hitloc[0] + "!")
        loc = hitloc[0]
        loc = loc[-2:].lower()
        #print(loc)
        loc = getattr(target, loc)
        shooter.hit = True
        firingmech.dmgthisturn += shooter.dmg
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


testsubject1= copy.deepcopy(awesome8q)
testsubject2= copy.deepcopy(awesome8q)
enemy = copy.deepcopy(awesome8q)
enemy2 = copy.deepcopy(awesome8q)


CoDs = {"HKill":0, "PKill":0, "EKill":0, "CTKill":0, "AmmoKill":0, "Survived":0}
Turns = []
crits = []
avgdmgs = {}
for i in range(20):
    exec(f"turn{i+1}dmg = []")
for i in range(100):
    critsthisgame = 0
    #print(i)
    if i % 100 == 0: print(i)
    enemy2 = copy.deepcopy(awesome8q)
    enemy2.pos = 0
    enemy = copy.deepcopy(awesome8q)
    for i in range(12):
        enemy2.move(True)
        if i == 0:
            enemy.pos = 21
        elif i == 1:
            enemy.pos = 18
        elif i == 2:
            enemy.pos = 15
        elif i == 3:
            enemy.pos = 14
        elif i == 4:
            enemy.pos = 12
        elif i == 5:
            enemy.pos = 10
        elif i == 6:
            enemy.pos = 9
        elif i == 7:
            enemy.pos = 7
        elif i == 8:
            enemy.pos = 6
        elif i == 9:
            enemy.pos = 5
        elif i == 10:
            enemy.pos = 3
        elif i == 11:
            enemy.pos = 1
        #print(f"Turn {i+1}")
        enemy.barrage(enemy2)
        critsthisgame+=enemy2.critsthisturn
        exec(f"turn{i+1}dmg.append(enemy.dmgthisturn)")
        if enemy2.isdead:
            #print(f"Enemy was destroyed in {i+1} turns!")
            Turns.append(i+1)
            if enemy2.causeofdeath == '':
                enemy2.causeofdeath = "CTKill"
            exec(f"CoDs[enemy2.causeofdeath] +=1")
            break
    if not enemy2.isdead:
        CoDs["Survived"] +=1
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
print(avgdmgs)
print(CoDs)
print(f"Killing took on average {mean(Turns)} turns! \n {stdev(Turns)}")



EndTime = time.time()
print(f"The program took {int(EndTime-StartTime)} seconds!")
