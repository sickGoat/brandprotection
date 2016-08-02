'''
Created on 30 apr 2016

@author: antonio
'''
import operator as op;
import networkx as nx;
import sys;

from algorithm.graphandler2 import SimulatedIC,Campaign;
from networkx.exception import NetworkXNoPath



def sortDictionary(dictionary,positionKey,revOrder=True):
    return sorted(dictionary.items(),key=op.itemgetter(positionKey), reverse=revOrder)


class Heuristic(object):

    def setGraphHandler(self,GH):
        self.GH = GH;

    def __repr__(self, *args, **kwargs):
        return self.__class__.__name__;

class OutDegree(Heuristic):

    def __call__(self,L,k):
        '''
        Prendi i nodi col maggior out degree
        @param G : grafo
        @param L : nodi attivi
        @param k : budget
        '''
        G = self.GH.G;
        OD = [x for x in G.out_degree().items() if not self.GH.isActive(x[0])];
        OD.sort(key=op.itemgetter(1),reverse=True);

        return [x[0] for x in OD[0:k]];

class EarlyInfected(Heuristic):

    def __call__(self,L,k):
        '''
        Prendi i nodi con la maggiore
        probabilita' di essere infettati
        nel breve page rank
        @param G : grafo
        @param L : nodi attivi
        @param k : budget
        '''
        print "EarlyInfected ",k
        G = self.GH.G;
        EI = {};
        for n in L:
            nDict = G.edge[n];
            for key in nDict.keys():
                if not self.GH.isActive(key) and not EI.has_key(key):
                    #prendo il peso di tutti gli archi entranti in key che partono da nodi infetti
                    IN_WEIGHT = [z[self.GH.weight] for x,y,z in G.in_edges(key,data=True) if self.GH.isActiveFor(x,Campaign.Bad)];
                    #calcolo la probabilita' di attivazione
                    activationProb = self.GH.getActivationProbability(key,IN_WEIGHT);
                    EI[key] = activationProb;


        OD = [x[0] for x in sortDictionary(EI, 1, True)];

        return OD[0:k];

class LargestInfected(Heuristic):

    def __init__(self,run=10):
        Heuristic.__init__(self);
        self.run = run;

    def __call__(self,L,k):
        '''
        @param G : grafo
        @param L : subset campagna malevola
        @param k : budget
        @param run : run per la simulazione
        '''
        G = self.GH.G;
        LI = {};
        #dizionario che mantiene per ogni nodo
        #lo shortest path da un nodo del seed
        SPDICT = {};
        count = 0;
        minValue = sys.maxint;
        while count < self.run:
            SL = SimulatedIC(G, L, self.GH.weight);
            for n in SL:
                if SPDICT.has_key(n):
                    #per ogni nodo sullo sp incremento di 1 il valore
                    for x in SPDICT[n]:
                        LI[x] += 1;
                else:
                    #calcolo lo sp da un nodo in L (seed) a un nuovo nodo infettato in SL
                    for x in L:
                        try:
                            current = nx.shortest_path(G,x,n);
                        except NetworkXNoPath:continue;

                        if len(current) < minValue:
                            minValue = len(current);
                            minPath = current;
                        
                        if len(current)==2:
                            break;
                    #escludo il nodo inizialmente infetto
                    del minPath[:1];
                    SPDICT[n] = minPath;
                    for node in minPath:
                        if LI.has_key(node):
                            LI[node] += 1;
                        else:
                            LI[node] = 1;
                            
                    minValue = sys.maxint;
            count += 1;

        OD = [x[0] for x in sortDictionary(LI, 1, True)];

        return OD[0:k];


class GreedyHeuristic(Heuristic):
    '''
        Questa eruristica calcola il seed
        di partenza andando a scegliere
        i k nodi con il maggior contributo marginale
    '''

    def __init__(self,run=100):
        self.run = run;
        self.saved = 0;


    def __call__(self,L,k):
        '''
        @param: L : lista di nodi gia infetti
        @param  k : budget
        '''
        i = 0;
        maxGain = -sys.maxint;
        GOODSEED = [];
        while i < k:
            for node in self.GH.G:
                if node not in L and node not in GOODSEED:
                    GOODSEED.append(node);
                    marginalGain = self.marginalGain(L,GOODSEED,self.run);
                    if marginalGain > maxGain:
                        toAppend = node;
                        maxGain = marginalGain;
                    GOODSEED.remove(node);
            GOODSEED.append(toAppend);
            maxGain=-sys.maxint;
            self.saved += maxGain;
            i += 1;

        return GOODSEED;

    def marginalGain(self,BL,GL,run):
        '''
        @param: BL : badList
        @param: GL : goodList
        @param: n  : nodo di cui valutare il contributo marginale
        '''
        blSize = len(BL);
        glSize = len(GL);
        saved,count = 0,0;
        while count < run:
            self.GH.MultiCampaign(BL,GL);
            saved += len(self.GH.getSaved());
            #resetto le liste
            del BL[blSize:];
            del GL[glSize:];
            count +=1;

        savedMean = saved/float(run);

        return savedMean-self.saved;
