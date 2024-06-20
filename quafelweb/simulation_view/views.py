from django.shortcuts import render

import plotly.express as px
from random import randint
from simulation_data.simulation import SimulationEnv, HardwareProfile

class SimulationView:

  @staticmethod
  def graph(x_label : str, y_label : str, x_data : list, y_data : list) -> str:
    return px.line(x=x_data, y=y_data, labels=[x_label, y_label]).to_html(full_html=False)

  def index(request):
    # Generate the plot
    # Pass the plot to the HTML template
    context = { 'graph_div' : SimulationView.graph("Y", "X", list(range(16)), [randint(0, 100) for _ in range(16)])}
    sim_evs = [ SimulationEnv(HardwareProfile())]

    SimulationView.render_view(request, sim_evs, sim_confs)
  
  def specific(request, qbit_start, qbit_end, depth_start, depth_end, evals_start, evals_end):
      ...


  def render_view(request, sim_envs : list[SimulationEnv], sim_confs : dict[str, list[int]]):
  
    context = { 'environments' : sim_envs }

    return render(request, 'index.html', context)
  