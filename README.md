# tb2net

## Description

tb2net is a python script that converts UD Treebanks into dependency networks and extracts some network metrics.

## Requirements

**Programming language:** python3

**Modules and packages:** os, time, argparse, logging, random, pandas, igraph, numpy, sklearn

## Usage

### Content of the repository

In the repository you will find:

* **tb2net.py:** the actual script that you will use to convert a UD treebank into a dependency network and extract the topological indexes

* **treebank_handler.py:** a python script containing some classes and function to handle a UD treebank file (imported in tb2net.py)

* **dep_net_handler.py:** a python script containing some functions to induce a graph and extract some topological indexes

* **test.conllu:** an extrat from the Late Latin Charter Treebank (300 sentences)

* **data:** a folder containing all the treebanks analyzed in the study

### Tutorial

The first thing you should do to run the script is open a terminal and move to the directory where you stored the files. Then, you can run the script typing and executing the following line:

```bash
python tb2net.py -i test.conllu
```

In your terminal something similar to this result should appear:

```bash
======================================================================================================================================================

                                                                        tb2net                                                                        

======================================================================================================================================================



2021-04-28 21:26:51 - Reading conllu file...
2021-04-28 21:26:51 - Done
2021-04-28 21:26:51 - Creating nodes file and edges file...
2021-04-28 21:26:51 - Done
2021-04-28 21:26:51 - Creating the dependency network...
2021-04-28 21:26:51 - Done
2021-04-28 21:26:51 - Extracting topological indexes...
2021-04-28 21:26:51 - Done



Topological indexes extracted from the network induced from test.conllu:

Number of nodes: 969
Number of edges: 2556
Average degree: 5.275541795665634
Clustering coefficient: 0.07966858044217195
Average path length: 4.11258731417752
Network centralization: 0.10219901373422102
Diameter: 12
Gamma: 1.5353935271795616
R^2: 0.9212672593500402



2021-04-28 21:26:51 - Script executed without errors - Execution time: 0.52 seconds
Author: Luca Brigada Villa - Contact: lucabrigadavilla@gmail.com - Licensed under the MIT License
```

If you look at the directory, you will see that two new files were created after the execution of the script: **nodes.csv** and **edges.csv**. This two files contain the lists of the nodes of the network built upon the UD treebank. Such files may be imported in other softwares for network visualization and analysis. If you don't need them, you can delete them after the execution of the script.

At this stage, you can already see the values of the topological indexes in the terminal window (along with other information about the execution of the script). Although, it may be useful to store such information in a file in order to reuse it at a later stage. To do this, run the following line in the terminal:

```bash
python tb2net.py -i test.conllu -o results.txt
```

You will see the result in the terminal, but if you look in the directory, you will find a file called _results.txt_ in which the topological indexes of the network are stored.

#### Command line arguments

The script _tb2net.py_ can be executed with some arguments:

Argument | Description | Required
-------- | ----------- | --------
-i UD\_FILE, --input UD\_FILE | Takes the file at path UD\_FILE as input | Yes
-s SIZE, --size SIZE | if specified, reduce the treebank to the number of tokens equal to SIZE | No
-l, --lemma | if this option is specified, produce a lemma-based network, otherwise a word-based network | No
-n NODES\_FILE, --nodes NODES\_FILE | path where to create the node file (default: nodes.csv) | No
-e EDGES\_FILE, --edges EDGES\_FILE | path where to create the edges file (default: edges.csv) | No
- o METRICS\_FILE, --output METRICS\_FILE | path where to create the file in which the topological indexes are stored | No
-h, --help | Show the description and the usage of the script | No


## Contacts

### Luca Brigada Villa

University of Pavia (Italy)

Email: lucabrigadavilla@gmail.com

Twitter: [@bavagliladri](https://twitter.com/bavagliladri)

### Guglielmo Inglese

KU Leuven (Belgium)

Email: guglielmo.inglese@kuleuven.be

## License

© Luca Brigada Villa

Licensed under the [MIT License](LICENSE)

