import numpy as np
from ant import Ant
import pandas as pd
class World:

  def __init__(self, matrix_wall: np.ndarray, position_start: tuple, position_finish: tuple, ant_count: int , max_iterations: int, pheromone_start_value: float, alpha: float, beta: float):
    """

    :type matrix_wall: numpy.ndarray
    :param matrix_wall: toto je test premenna
    :param position_start:
    :param position_end:
    """
    self.matrix_wall = matrix_wall
    self.position_start = position_start
    self.position_finish = position_finish

    self.ant_count = ant_count
    self.max_iterations = max_iterations

    self.world_shape = matrix_wall.shape
    
    # setup init value of pheomone
    self.matrix_pheromone = np.zeros(self.world_shape)
    self.matrix_pheromone[self.matrix_pheromone == 0] = pheromone_start_value
    self.matrix_pheromone[self.matrix_wall == 1] = 0
    self.matrix_pheromone[self.position_start] = 0
    self.matrix_pheromone[self.position_finish] = 0

    # create and list
    self.array_ant = np.empty(self.ant_count,dtype=Ant)
    for idx in range(0,self.ant_count):
        self.array_ant[idx] = Ant(self.position_start)

    self.alpha = alpha
    self.beta = beta

    self.world_shape = matrix_wall.shape
    self.actual_iteration = 1

  def render_world(self):
    print('##### WORD RENDER #####')
    print('---- ITERATION: '+ str(self.actual_iteration) +' ------')
    print('---- START : ' + str(self.position_start) + ' ----')
    print('---- FINISH: ' + str(self.position_finish) + ' ----')
    print('---- NoANTs: ' + str(self.ant_count) + ' --------')

    matrix_print = np.copy(self.matrix_wall)

    matrix_ant = np.zeros(self.world_shape)
    for id_ant in range(0,self.ant_count):
      # print(self.array_ant[id_ant].position_actual)
      matrix_ant[self.array_ant[id_ant].position_actual] +=1


    matrix_print = matrix_print.astype(str)

    matrix_print[self.position_start] = 'S'
    matrix_print[self.position_finish] = 'F'

    matrix_print[matrix_print == '1'] = "X"
    matrix_print[matrix_print == '0'] = "  "

    matrix_ant = matrix_ant.astype(int)
    matrix_ant = matrix_ant.astype(str)
    matrix_ant[matrix_ant == '0'] = " "



    # print(np.core.defchararray.add(matrix_print, matrix_ant))
    # print(matrix_print)
    # print("###")
    print(matrix_ant)
    # print("###")
    # print(self.matrix_pheromone)


  def do_interation(self):
    #kazdy mravec musi vykonat funkciu go()
    for ant_idx in range(0,self.ant_count):
      self.array_ant[ant_idx].go(self.matrix_wall,self.matrix_pheromone)



  def start(self):
    print("Start iterations")
    self.render_world()
    while self.actual_iteration <= self.max_iterations:
       self.evaporate_pheromone()
       self.do_interation()
       self.render_world()
       self.actual_iteration += 1





  def evaporate_pheromone(self):
    self.matrix_pheromone = self.matrix_pheromone - self.alpha
    self.matrix_pheromone[self.matrix_pheromone < 0] = 0