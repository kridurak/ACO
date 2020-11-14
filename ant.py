import random
import numpy as np
from scipy.spatial import distance

class Ant:

    def __init__(self,start_position):
        self.position_actual = start_position
        self.position_last = (start_position[0] ,start_position[1] -1) #podmienak aby sa nerozhodoval pri starte dozadu
        self.to_finish = True
        self.to_start = False
        self.compas = tuple([self.position_last[0] - self.position_actual[0] , self.position_last[1] - self.position_actual[1]])

    def go(self,matrix_wall,matrix_pheromone):
        # sekvencie prikazov pre pozrenie okolo seba
        cmd_y = np.array([0, -1, -1, -1, 0, 1, 1, -1])
        cmd_x = np.array([-1, -1, 0, 1, 1, 1, 0, -1])
        cost = np.zeros(8,dtype=float) #pripravene pre ulozenie vypoctu vzdialenosti
        cmd_count = len(cmd_x) #pocet prikazov
        avaliable_step_array_index = [] #pole ke sa nahraju iba mozne kroky, nemozne su = posun na predhcadzajucu suradnicu (compas), pozicie kde je stena alebo koniec mapy

        for id_com in range(0, cmd_count):
            ## vypocitavanie moznej poloy posunu
            tmp_pos_x = self.position_actual[1] + cmd_x[id_com]
            tmp_pos_y = self.position_actual[0] + cmd_y[id_com]
            # print(tmp_pos_y, tmp_pos_x)

            # ak je mapa cista a nie je tam stena potom vypocita vahu moznej cesty a ulozit do pola
            if matrix_wall[tmp_pos_y, tmp_pos_x] == 0 and (cmd_y[id_com] != self.compas[0] & cmd_x[id_com] != self.compas[1]) :
                # todo: upravit aby interagovalo aj na suradnicu
                if 0 <= tmp_pos_x < 9 and 0 <= tmp_pos_y < 9:
                    cost[id_com] = float(distance.euclidean(self.position_actual, (tmp_pos_y,tmp_pos_x))) * matrix_pheromone[tmp_pos_y,tmp_pos_x]
                    avaliable_step_array_index.append(id_com)


        # print(cost)
        # print(avaliable_step_array_index)

        # updatne pheromon
        matrix_pheromone[self.position_actual] += 1

        #ulozenie aktaulenj polohy do minulej
        self.position_last = self.position_actual

        #vypocitanie a urcenie dalsieho posunu
        next_step_id = random.choice(avaliable_step_array_index)
        self.position_actual = (self.position_actual[0] + cmd_y[next_step_id],self.position_actual[1] + cmd_x[next_step_id])




