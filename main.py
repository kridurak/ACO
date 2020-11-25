import numpy as np
from scipy.spatial import distance
from world import World

map_layer = np.array([  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    ], np.int32)

# create my world
my_world = World(matrix_wall=map_layer,
                 position_start=(4,0),
                 position_finish=(4,9),
                 ant_count= 100,
                 max_iterations= 500,
                 pheromone_start_value=0.5,
                 pheromon_amount=0.008,
                 rho=0.98
                 )

my_world.start()


