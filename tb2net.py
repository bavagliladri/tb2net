'''
File name: tb2net.py
Author: Luca Brigada Villa
Date created: 4/28/2021
Date last modified: 4/28/2021
Python Version: 3.7.3
'''

import os
import argparse
import logging
import time
import treebank_handler
import dep_net_handler


start_time = time.time()

print('=' * os.get_terminal_size().columns)
print()
print('tb2net'.center(os.get_terminal_size().columns))
print()
print('=' * os.get_terminal_size().columns)
print('\n\n')

logger = logging.getLogger('tb2net')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

# defining command line arguments
parser = argparse.ArgumentParser(description='tb2net is a python script that converts UD Treebanks into dependency'
                                             ' networks and extracts some network metrics.\n'
                                             'Author: Luca Brigada Villa - Contact: lucabrigadavilla@gmail.com -'
                                             ' Licensed under the MIT License',
                                 formatter_class=argparse.RawTextHelpFormatter)
required = parser.add_argument_group('required arguments')
required.add_argument('-i', '--input', action='store', dest='ud_file',
                    help='the ud_file in conllu format', required=True)
parser.add_argument('-s', '--size', action='store', dest='size', type=int,
                    help='the number of tokens to consider to build the network')
parser.add_argument('-l', '--lemma', action='store_true',
                    help='to produce a lemma-based network (default: word-based network)')
parser.add_argument('-n', '--nodes', action='store', dest='nodes_file',
                    help='the path where to save the file consisting of the list of the nodes')
parser.add_argument('-e', '--edges', action='store', dest='edges_file',
                    help='the path where to save the file consisting of the list of the edges')
parser.add_argument('-o', '--output', action='store', dest='metrics_file',
                    help='the path where to save the file containing network\'s metrics')
args = parser.parse_args()

ud_file = args.ud_file

word_based = not args.lemma

if args.nodes_file:
    nodes_file = args.nodes_file
else:
    nodes_file = 'nodes.csv'

if args.edges_file:
    edges_file = args.edges_file
else:
    edges_file = 'edges.csv'

# build treebank object
logger.info('Reading conllu file...')
tb = treebank_handler.build_tb(ud_file)
logger.info('Done')
# reduce the treebank to the desired size if required
if args.size:
    logger.info(f'Reducing the size of the treebank to {args.size} tokens...')
    tb.reduce2size(args.size)
    logger.info('Done')
# produce network files
logger.info('Creating nodes file and edges file...')
tb.net_files(word_based, nodes_file, edges_file)
logger.info('Done')
# build network
logger.info('Creating the dependency network...')
g = dep_net_handler.build_graph(nodes_file, edges_file, word_based)
logger.info('Done')
logger.info('Extracting topological indexes...')
indexes = dep_net_handler.export_metrics(g)
logger.info('Done')
# produce a file if required
if args.edges_file:
    logger.info('Writing topological indexes to file...')
    with open(args.metrics_file, 'w') as file:
        file.write(indexes)
    logger.info('Done')
# print with network indexes
print(f'\n\n\nTopological indexes extracted from the network induced from {ud_file}:\n')
print(f'{indexes}\n\n\n')

ex_time = time.time() - start_time
logger.info(f'Script executed without errors - Execution time: {round(ex_time, 2)} seconds')
print('Author: Luca Brigada Villa - Contact: luca.brigadavilla@unibg.it')