import numpy as np
from ant import Ant
import pandas as pd
class World:

  def __init__(self, matrix_wall: np.ndarray, position_start: tuple, position_finish: tuple, ant_count: int , pheromone_start_value: float, alpha: float, beta: float):
    """

    :type matrix_wall: numpy.ndarray
    :param matrix_wall: toto je test premenna
    :param position_start:
    :param position_end:
    """
    self.matrix_wall = matrix_wall
    self.position_start = position_start
    self.position_finish = position_finish
    self.world_shape = matrix_wall.shape
    self.ant_count = ant_count

    # setup init value of pheomone
    self.matrix_pheromone = np.zeros(self.world_shape)
    self.matrix_pheromone[self.matrix_pheromone == 0] = pheromone_start_value
    self.matrix_pheromone[self.matrix_wall == 1] = 0
    self.matrix_pheromone[self.position_start] = 0
    self.matrix_pheromone[self.position_finish] = 0

    self.array_ant = np.empty(self.ant_count,dtype=Ant)
    # self.array_ant =self.array_ant+ Ant(self.position_start)

    self.alpha = alpha
    self.beta = beta

  def render_world(self):
    print('##### WORD RENDER #####')
    print('---- ITERATION: 0 ------')
    print('---- START : ' + str(self.position_start) + ' ----')
    print('---- FINISH: ' + str(self.position_finish) + ' ----')
    print('---- NoANTs: ' + str(self.ant_count) + ' --------')
    matrix_print = np.chararray(self.world_shape)
    matrix_print = self.matrix_wall.astype(str)

    matrix_print[self.position_start] = 'S'
    matrix_print[self.position_finish] = 'F'

    matrix_print[matrix_print == '1'] = "X"
    matrix_print[matrix_print == '0'] = " "

    print(matrix_print)

    print(self.matrix_pheromone)


  def update_pheromone(self):
    self.matrix_pheromone = self.matrix_pheromone * self.alpha