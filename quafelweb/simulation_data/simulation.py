from dataclasses import dataclass
from models import HardwareProfile, SimulatorProfile

@dataclass
class SimulationEnv:
  
  # this does not need to be stored, can this be a normal class
  hardware : HardwareProfile
  
  simulator : SimulatorProfile



@dataclass
class SimulationGroup:

  environments : set[SimulationEnv]

  qbits : set[int]

  depths : set[int]

  evals : set[int]