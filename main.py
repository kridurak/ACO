import numpy as np
from scipy.spatial import distance
from world import World

map_layer = np.array([  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
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
                 ant_count= 10,
                 pheromone_start_value=0.2,
                 alpha=0.5,
                 beta=0.5
                 )

my_world.render_world()

my_world.update_pheromone()


