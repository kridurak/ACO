import acopy
import tsplib95 as tsplib
import networkx as nx
import matplotlib.pyplot as plt

# Parameters:	
# rho (float) – percentage of pheromone that evaporates each iteration
# q (float) – amount of pheromone each ant can deposit
solver = acopy.Solver(rho=.03, q=1)

# Parameters:	
# alpha (float) – how much pheromone matters
# beta (float) – how much distance matters
colony = acopy.Colony(alpha=1, beta=3)

# Load map as problem from tsplib95
problem = tsplib.load('AntColonyOptim/problems/bayg29.tsp')
G = problem.get_graph()

# Draw TSP problem with NetworkX
nx.draw(G, with_labels=True, font_weight='bold')
plt.savefig("AntColonyOptim/Fig1.png")
plt.clf()

# Elite tracer
# to deposit an additional two times the amount of pheromone set the factor to 2
# elite = acopy.plugins.EliteTracer(factor=2)

# Darwin
# sigma value for the guassian distribution used to choose the next values
# darwin = acopy.plugins.Darwin(sigma=.25)

# Solving problem with limit 100 iterations
tour = solver.solve(G, colony, limit=50)
path = tour.path

H = nx.path_graph(G)
G.clear()
G.add_node(H)
for p in path:
    G.add_edge(*p)

# # Draw solved TSP problem with NetworkX
nx.draw(G, with_labels=True, font_weight='bold')
plt.savefig("AntColonyOptim/Fig2.png")

