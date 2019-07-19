#UNIT AND BUILDING CLASSES
#Buildings
#------TWO BASE TANK LIB BIO ALL IN TvP------

Unit =	{  #Right side information is [minerals, gas, buildtime, supply] This is a dictionary
  "Marine": [50, 0, 18, 1],
  "Reaper": [50, 50, 32, 1],
  "Marauder": [100, 25, 21, 2],
  "Ghost": [150, 125, 29, 2],
  "SCV": [50, 0, 12, 1]
}

class Building():
    def __init__(self,minerals, gas, buildTime): #build time is in seconds
        self.minerals = minerals
        self.gas = gas
        self.buildTime = buildTime
        self.complete = 0 #0 Means not started, 1 means building and 2 means complete
        self.builders = 0 #workers building the structure
        self.startTime = 0 #used for building buildings(self) and units
        self.done = True  #FOR PRODUCTION BUILDINGS ONLY!! When True, the building has finished production and is ready to produce something else.
        self.allowedTypes = () #defines which production units are allowed to be made out of a building, Tuple containing strings.

    def Build(self, GameTime, MapMinerals, MapGas, SCV_Count):
        if self.complete == 0 and MapMinerals >= self.minerals and MapGas >= self.gas and SCV_Count > 0: #Build Started
            self.startTime = GameTime - 1 #-1 because build gets started in this iteration of the loop.
            self.complete = 1 #Building
            self.builders = 1
            return (-self.minerals, -self.gas, -1) #MineralCount and SupplyCount.

        if self.complete == 1 and GameTime >= (self.startTime + self.buildTime): #Done Building
            self.complete = 2 #Done
            self.builders = 0
            self.startTime = 0
            return (0, 0, 1) #gives back the SCV used to build (3rd element)
        else: return (0, 0, 0) #Currently Building

    #     FOR PRODUCTION STRUCTURES ONLY!!!
    def BuildUnit(self, GameTime, MapMinerals, MapGas, MapSupplyDifference, UnitType): #Unit type must be a string from the dictionary at the top of this script.

        for x in self.allowedTypes: #check to make sure building can build requested UnitType
            if UnitType is x:
                break
            else:
                raise ValueError("Building unable to produce requested unit type")

        if self.done == True and MapMinerals >= Unit[UnitType][0] and MapGas >= Unit[UnitType][1] and MapSupplyDifference >= Unit[UnitType][3]:
            self.startTime = GameTime - 1 #-1 because build gets started in this iteration of the loop
            self.done = False
            return (0, -Unit[UnitType][0], -Unit[UnitType][1], Unit[UnitType][3]) #Modifies SCV count, MineralCount and SupplyCount.
        if self.done == False and GameTime >= (self.startTime + Unit[UnitType][2]):
            self.done = True
            return (1, 0, 0, 0)
        else: return (0, 0, 0, 0)

    def BuildTech(self):
        self.minerals += 50
        self.gas += 50
        self.buildTime += 18

    def BuildReactor(self):
        self.minerals += 50
        self.gas += 50
        self.buildTime += 50

class CommandCenter(Building):
    def __init__(self):
        Building.__init__(self, 400, 0, 71)
        self.supply = 10
        self.SCVbuildTime = 13
        self.MinCapacity = 16 #Maximum mineral capacity per command center.
        self.tasked_scvs = 0
        self.allowedTypes = ("SCV",) #comma after required for a single element tuple

    def saturate(self, scv_int):
        if  (self.MinCapacity - self.tasked_scvs) > 0: #capacity not full
            if scv_int + self.tasked_scvs <= self.MinCapacity: #scvs will not overfill capacity
                self.tasked_scvs += scv_int
                return 0
            else:
                self.tasked_scvs = self.MinCapacity
                return scv_int - (self.MinCapacity - self.tasked_scvs)  #scvs will overfill capacity
        else: return scv_int #capacity full, scvs rejected.

class SupplyDepot(Building):
    def __init__(self):
        Building.__init__(self, 100, 0, 21)
        self.supply = 8


class Refinery(Building):
    def __init__(self):
        Building.__init__(self, 75, 0, 21)
        self.gascapacity = 3
        self.tasked_scvs = 0

    def saturate(self, scv_int):
        if  self.gascapacity > self.tasked_scvs: #capacity not full
            if scv_int + self.tasked_scvs <= self.gascapacity: #scvs will not overfill capacity
                self.tasked_scvs += scv_int
                return 0
            else:
                self.tasked_scvs = self.gascapacity
                return scv_int - (self.gascapacity - self.tasked_scvs)  #scvs will overfill capacity.
        else: return scv_int #capacity full, scvs rejected.

class Barracks(Building):
    def __init__(self):
        Building.__init__(self, 150, 0, 46)
        self.allowedTypes = ("Marine", "Reaper", "Marauder", "Ghost")

class Factory(Building):
    def __init__(self):
        Building.__init__(self, 150, 100, 43)
class Starport(Building):
    def __init__(self):
        Building.__init__(self, 150, 100, 36)
class Armory(Building):
    def __init__(self):
        Building.__init__(self, 150, 100, 46)
class FusionCore(Building):
    def __init__(self):
        Building.__init__(self, 150, 150, 46)
