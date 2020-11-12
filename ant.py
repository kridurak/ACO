import numpy as np
import pandas as pd
class Ant:

  def __init__(self,start_position):
      self.position_actual = start_position
      self.position_last = start_position
      self.to_finish = True
      self.to_start = False

  # def go(self,matrix_wall,matrix_pheromone):
  #     # posunie sa skontroluje vsetky mozno posunutia vyhodnoti pomocov funkcie a nasledne sa rozhodne kde chce ist


