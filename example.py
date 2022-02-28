import cnp.util
import cnp.graph
import cnp.points

# Create simple set of points.
H = cnp.points.makeH()

# Make unit-length graph from points & display
G = cnp.graph.Graph(H)
G.show()

import sympy as sp
from sympy import S, I

for i in range(5):
    # Create a copy of H, rotated about (-1,0) slightly.
    Hr = cnp.points.rotated(H, offset=(-1 + 0*I), angle=2*sp.asin(1/sp.sqrt(12)))
    # And add it to our previous H
    H = cnp.points.add(H, Hr)

# Create unit length graph and draw
G = cnp.graph.Graph(H)
G.show()

print(len(H[0]))

# See if this graph is n-colourable
import cnp.sat
from cnp.sat import isColourable, genMinGraph, optimize

for i in range(2,6):
    print("Is colourable in", i, "colours?", isColourable(G, i))

# Find minimal subgraph that's still not 3 colourable
optimize(G, 3, extract_MUS=True)

G.show()


# Now for a more complicated example... Showing M can never have a tricolour
# central H
Mp = cnp.points.makeM()
M = cnp.graph.Graph(Mp)
M.show()
print(len(Mp[0]))

import networkx as nx

# Check the center hexagon, which makes up the first 7 nodes of M
H = cnp.graph.Graph((Mp[0][:7], Mp[1][:7]))
H.show()
print(Mp[0][:7])

#from cnp.sat import sameColourConstraint

# Create a new constraint, vertices 1, 3, and 5 must never all be the same colour.
tri_nodes = [1, 3, 5]
clauses = cnp.sat.sameColourConstraint(tri_nodes, num_colours=4)

no_constr = cnp.sat.isColourable(M, num_colours=4)
print("Colourable without constraints?", no_constr)
constr = cnp.sat.isColourable(M, num_colours=4, extra_clauses=clauses)
print("Colourable with constraints?   ", constr)


# Perform simple (i.e. fast) optimisation that maintains this constraint.

# Here, we pass required clauses we don't want to ignore, while we remove
# the other constraints to find smaller graphs.

node_count = len(M.G.nodes)
cnp.sat.optimize(M, num_colours=4, extract_MUS=False, required_cl=clauses, required_nodes=tri_nodes)
diff = node_count - len(M.G.nodes)

M.show()


# Check it still works
constr = cnp.sat.isColourable(M, num_colours=4, extra_clauses=clauses)
print("Colourable with constraints?   ", constr)


# Completely optimize - remove until we reach a point where removing any clause causes the resulting
# graph to be sat once again.

# Again we pass required nodes and clauses so we don't simply delete the important central H graph.
cnp.sat.optimize(M, num_colours=4, extract_MUS=True, required_cl=clauses,
                 required_nodes=tri_nodes, verbosity=2)


# Double check it's exactly unit length
nx.write_gpickle(M, "G-optimized.gpickle")
M.show()
print(M.checkNetXGraph())


