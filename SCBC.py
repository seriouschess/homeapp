
#===========================================================================
#                 STAR       CRAFT        BUILD        CALCULATOR!!!
#                     This module is for Terran macro builds
#===========================================================================

import UABC
import SCMap

class TerranSimulation():
    def __init__(self):
        pass
    @classmethod
    def run(cls):#, Marine_Goal):
        #1 second in game represents a main loop
        GameTime = 0
        mineralRate = 0.95
        gasRate = 1.01
        m = SCMap.Map(12, 12)
        #will output the following
        MinuteList = []

        #Starting Assets including 12 SCVs
        m.supplyCap = 200
        CommandCenters = []
        SupplyDepots = []
        Refineries = []
        Barracks = []
        CommandCenters.append(UABC.CommandCenter())

        while GameTime <= 300: #5 minutes  #int(m.Marines) < #
        #Decision Block
            if m.SCVIdle < 1: #Cheap easy way to determine when to build an SCV (not right though)
                scvCountChange, minCost, gasCost, supplyChange = CommandCenters[0].BuildUnit(GameTime, m.Minerals, m.Gas, m.supply_available - m.supply, "SCV")
                m.SCVIdle += scvCountChange
                m.Minerals += minCost
                m.Gas += gasCost
                m.supply += supplyChange

            m.anticipated_supply = len(CommandCenters) * 15 + len(SupplyDepots) * 8 #Calculated anticipated supply which only affects decision to build supply depots.
            if ((m.anticipated_supply - m.supply) < 4) and (m.supply < m.supplyCap) and m.Minerals >= 100: #builds supply depot when supply is about to run out. 4 has no special meaning.
                SupplyDepots.append(UABC.SupplyDepot())
            #if len(Refineries) < 1 and m.Minerals >= 75: #Builds refineries as soon as cost allows.
                #m.Minerals -= 75
                #Refineries.append(UABC.Refinery())
            #if len(Refineries) < 2 and len(Refineries) >= 1 and m.Minerals >= 75:
                #m.Minerals -= 75
                #Refineries.append(UABC.Refinery())

            for x in range(0, len(SupplyDepots)):  # decision to build 1st barracks based on complete depot
                if (SupplyDepots[x].complete == 2) and (len(Barracks) < 2):
                    Barracks.append(UABC.Barracks())


        #Execute frame and calculate resources.
            for x in range(0,len(SupplyDepots)):
                minCost, gasCost, scvCountChange  = SupplyDepots[x].Build(GameTime, m.Minerals, m.Gas, m.SCVIdle)
                m.Minerals += minCost
                m.Gas += gasCost
                m.SCVIdle += scvCountChange

            for x in range (0,len(CommandCenters)):
                m.Minerals += CommandCenters[x].tasked_scvs*mineralRate #Add to mineral count for the second.
                m.SCVIdle = CommandCenters[x].saturate(m.SCVIdle)  #Assigns mineral harvesters to the command center.


            m.supply_available = len(CommandCenters) * 15 #Calculates actual supply available. Must follow 'Build' SupplyDepots call.
            for x in range(0,len(SupplyDepots)):#This code is required to allow the creation of Idle Scvs
                if (SupplyDepots[x].complete == 2):
                    m.supply_available += SupplyDepots[x].supply


            for x in range (0,len(Refineries)):
                minCost, gasCost, scvCountChange, = Refineries[x].Build(GameTime, m.Minerals, m.Gas, m.SCVIdle)
                m.Minerals += minCost
                m.Gas += gasCost
                m.SCVIdle += scvCountChange
                if Refineries[x].complete == 2: #Use Refinery
                    m.SCVIdle = Refineries[x].saturate(m.SCVIdle)
                m.Gas += Refineries[x].tasked_scvs*gasRate #Add to gas count for the second.

            for x in range(0, len(Barracks)):
                minCost, gasCost, scvCountChange, = Barracks[x].Build(GameTime, m.Minerals, m.Gas, m.SCVIdle)
                m.Minerals += minCost
                m.Gas += gasCost
                m.SCVIdle += scvCountChange

                MarineAdd, minCost, gasCost, supplyChange = Barracks[x].BuildUnit(GameTime, m.Minerals, m.Gas,
                                                                                                 m.supply_available - m.supply,
                                                                                                 "Marine")
                m.Marines += MarineAdd
                m.supply += supplyChange
                m.Minerals += minCost
                m.Gas += gasCost

            if GameTime%60 == 0:
                MineralSCVcount = 0
                for x in range(0, len(CommandCenters)):
                    MineralSCVcount += CommandCenters[x].tasked_scvs
                GasSCVcount = 0
                #for x in range(0, len(Refineries)):
                    #GasSCVcount += Refineries[x].tasked_scvs
                try:
                    GasSCVcount += Refineries[0].tasked_scvs
                except:
                    pass #basically don't throw an error if there are no refineries.
                try:
                    GasSCVcount += Refineries[0].gascapacity
                except:
                    pass


                Minuteinfo = [ "Time: {}Minute".format(int(GameTime/60)), "Supply: {}".format(m.supply),
                 "Supply Available: {}".format(m.supply_available), "Total SCVs: {}".format(MineralSCVcount + GasSCVcount + m.SCVIdle),
                 "Minerals: {}".format(int(m.Minerals)), "Gas: {}".format(int(m.Gas)), "Marines: {}".format(int(m.Marines)) ]
                MinuteList += [Minuteinfo]

            GameTime += 1
        return MinuteList
