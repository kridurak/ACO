import os
import random
import sys
import numpy as np
from scipy.spatial import distance

class Ant:

    def __init__(self, position_start, position_finish, pheromon_amount):
        self.position_start = position_start
        self.position_finish = position_finish
        self.pheromon_amount = pheromon_amount

        self.position_actual = position_start
        self.position_last = (position_start[0], position_start[1] - 1)

        self.to_finish = True
        self.find_finish = False

        self.history_to_finish = []
        self.to_finish_distance = 0

        self.compas = tuple(
            [self.position_last[0] - self.position_actual[0], self.position_last[1] - self.position_actual[1]])

        # cmd_y = np.array([0, -1, -1, -1, 0, 1, 1, 1])
        # cmd_x = np.array([-1, -1, 0, 1, 1, 1, 0, -1])

        cmd_y = np.array([-1, -1, -1,   0, 0, 0,   1, 1, 1])
        cmd_x = np.array([-1, 0, 1,     -1, 0, 1,  -1, 0, 1])
        self.array_command = np.array([cmd_y, cmd_x])

        self.last_array_command_index = 4

        self.distance_matrix = np.array([   [1.5, 1, 1.5],
                                            [1  , 0, 1],
                                            [1.5, 1, 1.5],
                                            ], np.int32)
        a = 1
        b = 0.1

        self.movement_mask = np.array([
                                        # 0
                                        [
                                            [a, a, a],
                                            [a, 0, b],
                                            [a, b, b],
                                        ],
                                        # 1
                                        [
                                            [a, a, a],
                                            [a, 0, a],
                                            [b, b, b],
                                        ],
                                        # 2
                                        [
                                            [a, a, a],
                                            [b, 0, a],
                                            [b, b, a],
                                        ],
                                        # 3
                                        [
                                            [a, a, b],
                                            [a, 0, b],
                                            [a, a, b],
                                        ],
                                        # 4
                                        [
                                            [a, a, a],
                                            [a, 0, a],
                                            [a, a, a],
                                        ],
                                        # 5
                                        [
                                            [b, a, a],
                                            [b, 0, a],
                                            [b, a, a],
                                        ],
                                        # 6
                                        [
                                            [a, b, b],
                                            [a, 0, b],
                                            [a, a, a],
                                        ],
                                        # 7
                                        [
                                            [b, b, b],
                                            [a, 0, a],
                                            [a, a, a],
                                        ],
                                        # 8
                                        [
                                            [b, b, a],
                                            [b, 0, a],
                                            [a, a, a],
                                        ],

                                      ], np.float)

    def go(self, matrix_wall, matrix_pheromone):
        if self.to_finish:

            ### 1 nastavit kompas
            self.compas = tuple([self.position_actual[0] - self.position_last[0], self.position_actual[1] - self.position_last[1]])

            ## 2 MATRIX WALL Border
            matrix_wall = np.pad(matrix_wall, pad_width=1, mode='constant',  constant_values=1)

            pos_actual_pad = (self.position_actual[0]  + 1 , self.position_actual[1] + 1)
            ### 2 WALL MASK
            mask_wall = matrix_wall[pos_actual_pad[0]-1:pos_actual_pad[0]+2,pos_actual_pad[1]-1:pos_actual_pad[1]+2]

            ### 2.1 INVERTED MASK kde steny su 0 a mozne cesty  1 aby sme zabespecilia by nesiel tam kde nema
            mask_wall = np.where((mask_wall==0)|(mask_wall==1), mask_wall^1, mask_wall)

            ### 3 PHEROMONE MASK
            matrix_pheromone_pad = np.pad(matrix_pheromone.copy(), pad_width=1, mode='constant', constant_values=0)
            mask_pheromone = matrix_pheromone_pad[pos_actual_pad[0]-1:pos_actual_pad[0]+2,pos_actual_pad[1]-1:pos_actual_pad[1]+2]

            ### 4 MOVEMENT MASK
            mask_movement = self.movement_mask[self.last_array_command_index]

            ## 5 COST MATRIX
            # print(self.position_last)
            # print(self.position_actual)
            # print(mask_wall)
            # print(mask_pheromone)
            # print(mask_movement)
            cost_matrix = self.distance_matrix * mask_wall * mask_pheromone * mask_movement
            # print(cost_matrix)

            ## rozhodovanie
            ## matrix to array
            cost_array = cost_matrix.flatten()

            next_step_id = roulette_wheel(cost_array)

            # record step
            self.history_to_finish.append(self.position_actual)

            # append distance
            self.to_finish_distance += distance.euclidean(self.position_last, self.position_actual)

            # ulozenie aktaulenj polohy do minulej
            self.position_last = self.position_actual


            self.last_array_command_index = next_step_id
            self.position_actual = (self.position_actual[0] + self.array_command[0, next_step_id],
                                    self.position_actual[1] + self.array_command[1, next_step_id])

            # updatne pheromon
            matrix_pheromone[self.position_actual] += self.pheromon_amount

            ### KONTROLA: Ci sa nasiel do ciel
            if self.position_actual[0] == self.position_finish[0] and self.position_actual[1] == self.position_finish[1]:
                self.find_finish = True
                self.to_finish = False
        else:
            self.position_last = self.position_actual
            self.position_actual = self.history_to_finish.pop()
            # updatne pheromon
            matrix_pheromone[self.position_actual] += self.pheromon_amount * 100

            # KONTROLA: Ci sa vratil do startu -> prepisat ak je pole krokov spat prazdne
            if self.position_actual[0] == self.position_start[0] and self.position_actual[1] == self.position_start[
                1]:
                self.to_finish = True


def roulette_wheel(cost_array):
    # get probabilities
    total_cost = float(sum(cost_array))
    probabilities = [c / total_cost for c in cost_array]
    # print(total_cost, probabilities)
    # perform roulette
    r = random.uniform(min(probabilities), sum(probabilities))
    counter = 0
    for i in range(0, 9):
        counter += probabilities[i]
        # chceck when it hit probility for random number
        if r <= counter:
            if cost_array[i] != 0:
            # print(i)
                return i
        # else:
            # print(r, i)