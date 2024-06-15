from django.db import models

from source.model.simulation import simulation_profile_model
from source.model.simulation.simulation_query_model import SimulationQuery
from source.model.simulation.simulation_run_model import SimulationRunModel
from source.model.util.float_list_field import FloatListField


# This class represents a point of an api_simulation (a points has multiple results for different shots)
class SimulationPointModel(models.Model):
    # The api_simulation-program and version this point was made for
    _simulation_profile = models.ForeignKey(SimulationProfileModel, on_delete=models.CASCADE)

    # The state of the point if it is finished or not
    _finished = models.BooleanField(default=False)

    # The api_simulation run this point belongs to
    simulation_run = models.ForeignKey(SimulationRunModel, on_delete=models.CASCADE, related_name='points')

    # Amount of shots
    _shots = models.IntegerField()

    # Amount of qubits
    _qubits = models.IntegerField()

    # Depth of the circuit
    _depth = models.IntegerField()

    # List of the results
    _results = FloatListField()  # TODO: implement this class with max_length=?

    # TODO: getter


# Get the existing points for a query
def GetExistingPoints(query: SimulationQuery) -> [SimulationPointModel]:
    return None  # TODO: implement this function


# Get the non-existing points for a query
def GetNonExistingPoints(query: SimulationQuery) -> [SimulationPointModel]:
    return None  # TODO: implement this function