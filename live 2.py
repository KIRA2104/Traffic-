import traci

sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", "mynetwork.sumocfg"]
traci.start(sumoCmd)

while traci.simulation.getMinExpectedNumber() > 0:
    # Get vehicle count in each lane
    vehicles = traci.lane.getLastStepVehicleNumber("E1")

    # Change traffic light timing dynamically
    if vehicles > 10:
        traci.trafficlight.setPhase("TL1", 0)  # Green for East-West
    else:
        traci.trafficlight.setPhase("TL1", 2)  # Green for North-South

    traci.simulationStep()

traci.close()
