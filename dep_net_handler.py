'''
File name: dep_net_handler.py
Author: Luca Brigada Villa
Date created: 4/28/2021
Date last modified: 4/28/2021
Python Version: 3.7.3
'''

import pandas as pd
from igraph import *
import math
import numpy as np
from sklearn.linear_model import LinearRegression


def centralization(n_nodes, max_degree, av_degree):
    # returns the network centralization as described in Horvath & Dong (2008)
    res = (n_nodes / (n_nodes - 2)) * ((max_degree - av_degree) / (n_nodes - 1))
    return res


def powerlaw(graph):
    # this function takes a graph as argument and returns the slope
    # of the degree distribution of the nodes and the R^2
    degrees = graph.degree()
    d = list(set([x for x in degrees if x != 0]))
    pk = []
    for k in d:
        p = degrees.count(k) / len(degrees)
        pk.append(math.log10(p))
    x = np.array([math.log10(deg) for deg in d]).reshape((-1, 1))
    y = np.array(pk)
    model = LinearRegression()
    model.fit(x, y)
    return -model.coef_[0], model.score(x,y)


def build_graph(nodes_file = 'nodes.csv', edges_file= 'edges.csv', word_based = True):
    # this function takes as argument the two csv files
    # consisting of the lists of the nodes and the edges
    # and returns a graph object
    edges = pd.read_csv(edges_file)
    nodes = pd.read_csv(nodes_file)
    e = [[row['parent_id'], row['child_id']] for index, row in edges.iterrows()]

    # generating graph from pandas dataframe
    if word_based:
        col_name = 'form'
    else:
        col_name = 'lemma'
    g = Graph(n=len(nodes.index), edges=e, directed=False,
              vertex_attrs={col_name: list(nodes[col_name].values),
                            'pos': list(nodes['pos'].values)},
              edge_attrs={'deprel': list(edges['deprel'].values)})
    return g


def export_metrics(graph):
    # takes a graph object as argument and returns a string containing the values of:
    # - number of edges
    # - number of vertices
    # - average degree
    # - clustering coefficient
    # - average path length
    # - network centralization
    # - diameter
    # - gamma
    # - rsq
    n_edges = graph.ecount()
    n_nodes = graph.vcount()
    av_degree = sum(graph.degree()) / n_nodes
    clust_coeff = graph.transitivity_avglocal_undirected()
    path_length = graph.average_path_length()
    nc = centralization(n_nodes, max(graph.degree()), av_degree)
    diameter = graph.diameter()
    pl = powerlaw(graph)
    gamma = pl[0]
    rsq = pl[1]
    result = f'Number of nodes: {n_nodes}\n' \
             f'Number of edges: {n_edges}\n' \
             f'Average degree: {av_degree}\n' \
             f'Clustering coefficient: {clust_coeff}\n' \
             f'Average path length: {path_length}\n' \
             f'Network centralization: {nc}\n' \
             f'Diameter: {diameter}\n' \
             f'Gamma: {gamma}\n' \
             f'R^2: {rsq}'
    return result
