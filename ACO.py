"""
Ant Colony Optimization algorithm
    - PHEROMONE (model and vaporization)
    - Decision making 
"""

import numpy as np

n = np.array(5) # number of ants

cost_matrix = np.array([[0,  5,  15, 4],
                        [5,  0,  4,  8],
                        [15, 4,  0,  1],
                        [4,  8,  1,  0]])

pheromone_matrix = np.array([[0,  4,  10, 3],
                             [4,  0,  1,  2],
                             [10, 1,  0,  1],
                             [3,  2,  1,  0]])

# ro vaporization weight (0 means no vaporization)
ro = 0.3      

# modification of pheromone level at given place 
# DELTA_TAU(parameter is length of path)
def delta_tau(length):
    return 1/length 

# pheromon level
def new_tau(tau):
    sum_delta_tau = 0
    for i in range(len(pheromone_matrix)):
        for j in range(pheromone_matrix.shape[i]):
            sum_delta_tau += pheromone_matrix[i,j]
    return (1-ro)*tau + sum_delta_tau

# for i in range(n):
#     L =       