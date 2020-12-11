import numpy as np
# import cupy as np
from ant import Ant
from any_v2 import Ant
import pandas as pd
import time
import sys
import os
from tqdm import tqdm
from matplotlib import pyplot as plt
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%d_%m-%H_%M_%S")

if not os.path.exists('images/' + current_time):
    os.makedirs('images/' + current_time)


class World:

    def __init__(self, matrix_wall: np.ndarray, position_start: tuple, position_finish: tuple, ant_count: int,
                 max_iterations: int, pheromone_start_value: float, pheromon_amount: float, rho: float):
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
        self.pheromon_amount = pheromon_amount
        self.rho = rho
        self.world_shape = matrix_wall.shape

        # setup init value of pheomone
        self.matrix_pheromone = np.zeros(self.world_shape)

        self.matrix_pheromone[self.matrix_pheromone == 0] = pheromone_start_value
        self.matrix_pheromone[self.matrix_wall == 1] = 0

        self.matrix_pheromone[self.position_start] = 0
        self.matrix_pheromone[self.position_finish] = 9

        # create and list
        self.array_ant = np.empty(self.ant_count, dtype=Ant)
        for idx in range(0, self.ant_count):
            self.array_ant[idx] = Ant(self.position_start, self.position_finish, self.pheromon_amount)

        self.any_finish = False

        self.world_shape = matrix_wall.shape
        self.actual_iteration = 0
        self.minimal_distance_to_finish = 999999999

    def render_world(self):
        print('##### WORD RENDER #####')
        print('---- ITERATION: ' + str(self.actual_iteration) + ' ------')
        print('---- START : ' + str(self.position_start) + ' ----')
        print('---- FINISH: ' + str(self.position_finish) + ' ----')
        print('---- NoANTs: ' + str(self.ant_count) + ' --------')

        matrix_print = np.copy(self.matrix_wall)

        matrix_ant = np.zeros(self.world_shape)
        for id_ant in range(0, self.ant_count):
            # print(self.array_ant[id_ant].position_actual)
            matrix_ant[self.array_ant[id_ant].position_actual] += 1

        matrix_print = matrix_print.astype(str)

        matrix_print[self.position_start] = 'S'
        matrix_print[self.position_finish] = 'F'

        matrix_print[matrix_print == '1'] = "X"
        matrix_print[matrix_print == '0'] = " "

        matrix_ant = matrix_ant.astype(int)
        self.render_gui(matrix_ant)
        matrix_ant = matrix_ant.astype(str)
        matrix_ant[matrix_ant == '0'] = " "

        print(np.core.defchararray.add(matrix_print, matrix_ant))
        # print(matrix_print)
        # print("###")
        # print(matrix_ant)
        # print("###")
        # print(self.matrix_pheromone)

    def render_gui(self, matrix_ant):

        render_matrix = matrix_ant
        render_matrix[self.position_finish] = '-1'
        render_pheromone = self.matrix_pheromone
        render_pheromone[self.position_finish] = '-1'

        plt.close()
        tmp_mat = self.matrix_wall.astype(int)
        tmp_mat[self.matrix_wall == 1] = self.ant_count + 1

        matrix_ant_fig = matrix_ant + tmp_mat
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

        for (j, i), label in np.ndenumerate(matrix_ant_fig):
            if label == self.ant_count + 1:
                ax1.text(i, j, 'X', ha='center', va='center')
            else:
                ax1.text(i, j, label, ha='center', va='center')

        # ax1.text(self.position_finish[1],self.position_finish[0], 'F', ha='center', va='center')

        for (j, i), label in np.ndenumerate(self.matrix_pheromone):
            # print(label)
            if label == self.ant_count + 1:
                ax1.text(i, j, 'X', ha='center', va='center')
            else:
                ax2.text(i, j, np.round(label, 2), ha='center', va='center')

        ax1.imshow(matrix_ant_fig)
        ax1.set_title('matrix_ant')

        ax2.imshow(self.matrix_pheromone)
        ax2.set_title('matrix_pheromone')

        matrix_ant = matrix_ant.astype(str)
        matrix_ant[matrix_ant == '0'] = " "

        # plt.imshow(self.matrix_pheromone)
        plt.pause(0.01)
        plt.savefig(F'images/{current_time}/{self.actual_iteration}__{self.ant_count}m.png')
        # plt.show()

    def do_interation(self):
        # kazdy mravec musi vykonat funkciu go()
        for ant_idx in range(0, self.ant_count):
            self.array_ant[ant_idx].go(self.matrix_wall, self.matrix_pheromone)

            if self.array_ant[ant_idx].find_finish:
                if self.minimal_distance_to_finish > self.array_ant[ant_idx].to_finish_distance:
                    self.minimal_distance_to_finish = self.array_ant[ant_idx].to_finish_distance
                    self.array_ant[ant_idx].to_finish_distance = 0
                print(self.minimal_distance_to_finish, self.array_ant[ant_idx].to_finish_distance)
                self.array_ant[ant_idx].find_finish = False
                self.any_finish = True

    def start(self):
        print("Start iterations")
        self.render_world()
        self.actual_iteration = 1
        # while self.actual_iteration <= self.max_iterations:
        for self.actual_iteration in tqdm(range(self.actual_iteration, self.max_iterations)):
            self.evaporate_pheromone()
            self.do_interation()
            self.render_world()
            # self.actual_iteration += 1

        print(self.any_finish)
        print(self.minimal_distance_to_finish)

    def evaporate_pheromone(self):
        self.matrix_pheromone = self.matrix_pheromone * self.rho
        self.matrix_pheromone[self.matrix_pheromone < 0] = 0
