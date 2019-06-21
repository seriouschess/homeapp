class Map():
    def __init__ (self, startingsupply, SCVIdle):
        self.Minerals = 0
        self.Gas = 0
        self.supply = startingsupply #accounts for starting SCVs
        self.anticipated_supply = startingsupply #Used to determine when to build supply depots.
        self.supply_available = 0
        self.supplyCap = 200
        self.SCVIdle = SCVIdle  # scvs Idle
        self.Marines = 0
