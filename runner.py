'''
Created on 14 mag 2016
Script per far partire la simulazione, occorre specificare
in input:
    file contentente il grafo
    euristica da utilizzare
    delay della campagna buona
    numerosita del seed della campagna malevola
    budget a disposizione per la campagna buona
    numero di run
    random seed
    weighted
@author: antonio
'''
import sys;
from algorithm import graphandler3
from algorithm import heuristics;
import random as r;
import time;

def convertMilliseconds(time):
    '''
    @param time: in millisecondi
    '''
    return None;

def saveResult(RESULT):
    '''
    @param RESULT : dizionario contenente risultati simulazione
    '''

    return None;

class SimulationParameter(object):

    def __init__(self,ARGS):
        self.filePath = ARGS[1];
        self.H = ARGS[2]
        self.delay = int(ARGS[3]);
        self.seed = int(ARGS[4]);
        self.k = int(ARGS[5]);
        self.run = int(ARGS[6]) if  int(ARGS[6])>0 else None;
        self.randomSeed = int(ARGS[7]) if int(ARGS[7])>0 else None;
        self.weighted = bool(int(ARGS[8]));

    def getHeuristic(self,GH):
        if self.H == 'O':
            heuristic = heuristics.OutDegree();
            heuristic.setGraphHandler(GH);
        if self.H == 'E':
            heuristic = heuristics.EarlyInfected();
            heuristic.setGraphHandler(GH);
        if self.H == 'L':
            heuristic = heuristics.LargestInfected(self.run);
            heuristic.setGraphHandler(GH);
        if self.H == 'G':
            heuristic = heuristics.GreedyHeuristic(self.run);
            heuristic.setGraphHandler(GH.getSimulator());

        return heuristic;

    def __str__(self, *args, **kwargs):
        return "File={} Euristica={} delay={} Seed={} K={} Run={} randomSeed={} weighted={}".format(self.filePath,self.H,self.delay,self.seed,self.k,self.run,self.randomSeed,self.weighted);



if __name__ == '__main__':
    params = SimulationParameter(sys.argv);
    print params;
    GH = graphandler3.RealGraphHandler(params.filePath,randomSeed=params.randomSeed,weigthed=params.weighted);
    H = params.getHeuristic(GH);
    # prendo come seed i nodi col maggior out degree
    BL = [ x for x,y in sorted(GH.G.out_degree().items(),key=lambda x:x[1],reverse=True)][:params.seed]; 
    t = time.time();
    SAVED,GL,BL,tMax = GH.alghoritm(BL, params.delay, params.k, H);
    t = (time.time()-t)/float(1000);
    print "%s,%s,%d,%d,%d,%d,%d,%d,%d,%d,%f" % (params.filePath, H, params.delay, tMax, params.seed, params.k, params.run, len(GL), len(BL), len(SAVED), t);
     
    
      