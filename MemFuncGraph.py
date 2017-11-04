import math
import random

import matplotlib.pyplot as pplt
import networkx
import numpy as np


class MemFuncGraph(networkx.Graph):
    def __init__(self, graphsize=30, graph=None, exp=0.0):
        networkx.Graph.__init__(self)

        if graph is None:
            self.b = networkx.barabasi_albert_graph(graphsize, 3)
        else:
            self.b = graph
        # self.b = networkx.grid_graph([5,5])
        # self.b = networkx.cycle_graph(size)

        for n in self.b.nodes_iter():
            self.add_node(2 * n, type='f')
            self.add_node(2 * n + 1, type='m')
            self.add_edge(2 * n, 2 * n + 1, weight=1.0)

        for n, nbr in self.b.edges_iter():
            n_f_0 = (self.degree(2 * n) == 1)
            n_m_0 = (self.degree(2 * n + 1) == 1)
            nbr_f_0 = (self.degree(2 * nbr) == 1)
            nbr_m_0 = (self.degree(2 * nbr + 1) == 1)
            if n_f_0:
                n_target = 2 * n  # (n,'f')
                nbr_target = 2 * nbr + 1  # (nbr,'m')
            elif nbr_f_0:
                n_target = 2 * n + 1  # (n, 'm')
                nbr_target = 2 * nbr  # (nbr, 'f')
            elif n_m_0:
                n_target = 2 * n + 1  # (n,'m')
                nbr_target = 2 * nbr  # (nbr,'f')
            elif nbr_m_0:
                n_target = 2 * n  # (n,'f')
                nbr_target = 2 * nbr + 1  # (nbr,'m')
            elif random.random() < 0.5:
                n_target = 2 * n  # (n,'f')
                nbr_target = 2 * nbr + 1  # (nbr,'m')
            else:
                n_target = 2 * n + 1  # (n, 'm')
                nbr_target = 2 * nbr  # (nbr, 'f')
            if exp != 0.0:
                w = np.random.exponential(scale=1.0) ** exp / math.factorial(int(math.ceil(exp)))
            else:
                w = 1.0
            self.add_edge(n_target, nbr_target, weight=w)

    def draw(self):
        placement = True
        shapeMap = dict()
        shapeMap['f'] = 'o'
        shapeMap['m'] = 's'
        colorMap = dict()
        colorMap['f'] = 'r'
        colorMap['m'] = 'y'

        for np in self.nodes(data="True"):
            if 'loc' not in np[1]:
                placement = False

        if not placement:
            nodePos = networkx.layout.spring_layout(self)
        else:
            nodePos = dict()
            for n in self.nodes():
                nodePos[n] = self.node[n]['loc']
        pplt.axis('equal')
        pplt.axis('off')
        # For each node class...
        for t in ['f', 'm']:
            # ...filter and draw the subset of nodes with the same symbol in the positions that are now known through the use of the layout.
            nl = [sNode[0] for sNode in filter(lambda x: x[1]["type"] == t, self.nodes(data=True))]
            networkx.draw_networkx_nodes(self, nodePos,
                                         node_color=colorMap[t],
                                         node_shape=shapeMap[t],
                                         node_size=10,
                                         linewidths=0.5,
                                         nodelist=nl)

            #       for aShape in nodeShapes:
            # ...filter and draw the subset of nodes with the same symbol in the positions that are now known through the use of the layout.
            #           networkx.draw_networkx_nodes(G, nodePos, node_shape=aShape, nodelist=[sNode[0] for sNode in
            #                                                                                filter(lambda x: x[1]["s"] == aShape,
            #                                                                                       G.nodes(data=True))])

        # Finally, draw the edges between the nodes
        networkx.draw_networkx_edges(self, nodePos, width=0.15)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    inst = MemFuncGraph(size=12)

    # networkx.draw(inst.b)
    inst.draw()
    plt.show()
    networkx.draw(inst)
    plt.show()
