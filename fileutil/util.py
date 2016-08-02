'''
Created on 22 apr 2016

@author: antonio
'''

import random as r;
from tempfile import mkstemp;
from shutil import move;
from os import close;
from networkx import gaussian_random_partition_graph,write_edgelist,write_weighted_edgelist;
import fileinput;


def addWeight(source,destination):
    '''
    @param source : file path
    @param destinattion : file path

    '''
    tmp,absPath = mkstemp();
    with open(absPath,'w') as new_file:
        with open(source) as s:
            for line in s:
                splitted = line.rstrip().split();
                try:
                    n1 = int(splitted[0])
                    n2 = int(splitted[1]);
                    weight = r.random();
                    new_file.write("{} {} {} \n".format(n1,n2,weight));
                except ValueError:
                    pass;
    close(tmp);
    move(absPath,destination);


def addWeightInPlace(source):
    '''
    Aggiunge i pesi direttamente nel file di input

    '''
    for line in fileinput.input(source, inplace=True):
        splitted = line.split();
        try:
            n1 = int(splitted[0]);
            n2 = int(splitted[1])
            w = r.random();
            print "{} {} {}".format(n1,n2,w);
        except:
            pass;


def createRandomGraph(nodes,numOfCommunity,shape=10,pIn=0.5,pOut=0.25):
    return gaussian_random_partition_graph(nodes,numOfCommunity,shape,pIn,pOut, directed=True);

def writeGraph(graph,filePath,weighted=True):
    with open(filePath,'w') as f:
        if not weighted:
            write_edgelist(graph,f);
        else:
            write_weighted_edgelist(graph,f);

def addWeighToGraph(graph):
    for x in graph:
        NBRS=graph.neighbors(x);
        for nbr in NBRS:
            graph.edge[x][nbr]['weight'] = r.random();

if __name__ == '__main__':
    G = createRandomGraph(500, 2, 10, 0.2, 0.5);
    addWeighToGraph(G);
    writeGraph(G, '../graphs/generated100.txt');
