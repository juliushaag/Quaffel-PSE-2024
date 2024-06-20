from django.db import models
from hardware_controller.models import HardwareProfile


#TODO do this from a conf file maybe even in the settings
class SimulatorProfile(models.Model):

  name = models.CharField(max_length=50)

  version = models.CharField(max_length=50)


class SimulationRun(models.Model):
  
  # ENV

  hardware_profile = models.ForeignKey(HardwareProfile, on_delete=models.CASCADE)

  simulator_name = models.ForeignKey(SimulatorProfile, on_delete=models.CASCADE)

  # CONF

  shots = models.IntegerField()

  qubits = models.IntegerField()

  depth = models.IntegerField()


  # STATUS

  finished = models.BooleanField(default=False) # enums in orm ??

  expressability = models.FloatField()  # how to represent optional SimulationResult data ?

  entangelment_cap = models.FloatField()

  durations = models.FloatField(max_length=100)

