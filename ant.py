import os
import random
import sys
import numpy as np
from scipy.spatial import distance

class Ant:

    def __init__(self,start_position,position_finish,pheromon_amount):
        self.postion_start = start_position
        self.position_finish = position_finish
        self.position_actual = start_position
        self.position_last = (start_position[0] ,start_position[1] -1) #podmienak aby sa nerozhodoval pri starte dozadu
        self.to_finish = True
        self.pheromon_amount = pheromon_amount
        self.find_finish = False
        cmd_y = np.array([0, -1, -1, -1, 0, 1, 1, 1])
        cmd_x = np.array([-1, -1, 0, 1, 1, 1, 0, -1])
        self.array_command = np.array([cmd_y,cmd_x])
        self.history_to_finish = []
        self.compas = tuple([self.position_last[0] - self.position_actual[0], self.position_last[1] - self.position_actual[1]])
        self.to_finish_distance = 0



    def go(self,matrix_wall,matrix_pheromone):
        if self.to_finish:
            sys.stdout = open(os.devnull, 'w')  # disable prints in function
            self.compas = tuple(
                [self.position_actual[0] - self.position_last[0] ,self.position_actual[1] -  self.position_last[1]])

            # sekvencie prikazov pre pozrenie okolo seba

            cost = np.zeros(8, dtype=float)  # pripravene pre ulozenie vypoctu vzdialenosti
            cmd_count = 8  # pocet prikazov
            avaliable_step_array_index = []  # pole ke sa nahraju iba mozne kroky, nemozne su = posun na predhcadzajucu suradnicu (compas), pozicie kde je stena alebo koniec mapy
            print('ACTUAL POS ', self.position_actual)
            print('LAST POS', self.position_last)
            print("COMPAS ", self.compas)
            for id_com in range(0, cmd_count):
                ## vypocitavanie moznej poloy posunu
                tmp_pos_x = self.position_actual[1] + self.array_command[1, id_com]
                tmp_pos_y = self.position_actual[0] + self.array_command[0, id_com]
                print(tmp_pos_y, tmp_pos_x)

                # ak je mapa cista a nie je tam stena potom vypocita vahu moznej cesty a ulozit do pola
                print('CHECK INIT')
                if 0 <= tmp_pos_x < 10 and 0 <= tmp_pos_y < 10:
                    print('CHECK 1 PASS: WORLD')
                    if matrix_wall[tmp_pos_y, tmp_pos_x] == 0:
                        print('CHECK 2 PASS: WALL')
                        # todo: upravit aby interagovalo aj na suradnicu
                        if not (self.array_command[0, id_com] == self.compas[0] and self.array_command[1, id_com] ==
                                self.compas[1]):
                            print('CHECK 3 PASS: COMPAS -> last position return')
                            cost[id_com] = float(1 / distance.euclidean(self.position_actual, (tmp_pos_y, tmp_pos_x))) * \
                                           matrix_pheromone[tmp_pos_y, tmp_pos_x]
                            avaliable_step_array_index.append(id_com)
                            print('CHECK OK')

            print(avaliable_step_array_index)

            # record step
            self.history_to_finish.append(self.position_actual)

            #append distance
            self.to_finish_distance += distance.euclidean(self.position_last, self.position_actual)

            # ulozenie aktaulenj polohy do minulej
            self.position_last = self.position_actual

            # vypocitanie a urcenie dalsieho posunu
            next_step_id = roulette_wheel(avaliable_step_array_index, cost)
            # next_step_id = random.choice(avaliable_step_array_index)

            print("next_step_id", next_step_id)
            self.position_actual = (self.position_actual[0] + self.array_command[0, next_step_id],
                                    self.position_actual[1] + self.array_command[1, next_step_id])



            # updatne pheromon
            matrix_pheromone[self.position_actual] += self.pheromon_amount

            sys.stdout = sys.__stdout__
        else:
            self.position_last = self.position_actual
            self.position_actual = self.history_to_finish.pop()
            # updatne pheromon
            matrix_pheromone[self.position_actual] += self.pheromon_amount * 1000

        # if najdem ciel
        if self.position_actual[0] == self.position_finish[0] and self.position_actual[1] == self.position_finish[1]:
            # print(self.position_actual)
            self.find_finish = True
            self.to_finish = False
            # self.to_finish_distance = len(self.history_to_finish)


        if self.position_actual[0] == self.postion_start[0] and self.position_actual[1] == self.postion_start[1]:
            self.to_finish = True






def roulette_wheel(avaliable_step_array_index, cost):
    # get probabilities
    total_cost = float(sum(cost))
    probabilities = [c/total_cost for c in cost]
    # print(total_cost, probabilities)
    # perform roulette
    r = random.uniform(min(probabilities),sum(probabilities))
    counter = 0
    for i in range(0,len(avaliable_step_array_index)):
        counter += probabilities[avaliable_step_array_index[i]]
        # chceck when it hit probility for random number
        if r <= counter:
            print(i)
            return avaliable_step_array_index[i]
        else: print(r,i)