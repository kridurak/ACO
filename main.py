import numpy as np
from scipy.spatial import distance
from world import World

map_layer = np.array([  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    ], np.int32)

# create my world
my_world = World(matrix_wall=map_layer,
                 position_start=(4,0),
                 position_finish=(4,9),
                 ant_count= 5,
                 max_iterations= 100,
                 pheromone_start_value=1,
                 alpha=0.1,
                 beta=0.5
                 )

my_world.start()


