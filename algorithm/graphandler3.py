'''
Created on 02 mag 2016

@author: antonio
'''
import networkx as nx;
import listiterator as li;
import random as rand;
from aenum import Enum;

def SimulatedIC(G,L,label,randomSeed=100):
    originalSize = len(L);
    gen = rand.Random(randomSeed);
    for n in L:
        NBRS = G.neighbors(n);
        for nbr in NBRS:
            if nbr not in L:
                w = G.edge[n][nbr][label];
                r = gen.random();
                if r <= w:
                    L.append(nbr);

    #tronco le due liste
    RES = L[originalSize:];
    del L[originalSize:];

    return RES;


# Enum raprresentante gli stati di un nodo
class NodeState(Enum):
        Inactive = 0;
        Bad = 1;
        Good = 2;
    
class Campaign(Enum):
        Bad = 1;
        Good = 2;

# ********************** #
# Interfaccia comune a   #
# tutti gli handler      #
# ********************** #
class GraphHandler(object):
    
        
    weight = 'influence';
    state = 'state';
    shadowState = 'shadowState';
    time = 'time';

    def __init__(self, graphFilePath,randomSeed=None,weigthed=True):
        with open(graphFilePath) as f:
            if weigthed:
                self.G = nx.read_weighted_edgelist(f, create_using=nx.DiGraph(),nodetype=int);
                self.weight = 'weight';
            else:
                self.G = nx.read_edgelist(f, create_using=nx.DiGraph(),nodetype=int);
            self.random = rand.Random(randomSeed);
            self.randomSeed = randomSeed;


    def canTry(self,node,campaign):
        raise NotImplementedError;
    
    def activate(self,src,dst,campaign,time):
        raise NotImplementedError;
    
    def active(self,node,campaign,time):
        raise NotImplementedError;

    def isActive(self,node):
        raise NotImplementedError;
    
    def isActiveFor(self,node,campign):
        raise NotImplementedError;
    
    def isSaved(self,node):
        raise NotImplementedError;

    def attempt(self,node,nbr):
        edgeWeight = self.G.edge[node][nbr][self.weight];
        r = self.random.random();
        return edgeWeight>r;

    def getSimulator(self):
        raise NotImplementedError;

    def getActivationProbability(self,x,WL,run=1000):
        count,success=0,0;
        while count < run:
            for w in WL:
                if w > self.random.random():
                    success += 1;
                    break;
            count += 1;

        print "node:{} success:{} run:{} prob:{}".format(x,success,run,(float(success)/run));
        return success/float(run);

    def MultiCampaign(self,GL,BL,startingTime,startIndex):
        '''
        @param: GL : lista di nodi good
        @param: BL : lista di nodi bad
        @param: startingTime
        @return: t : tempo massimo (time step)
        '''
        badIt = li.Wrap(BL);
        #inizializzo la posizione dell'iteratore
        badIt.setPosition(startIndex);
        goodIt = li.Wrap(GL);
        t = startingTime;
        prevLengthG,nextLengthG = 0,len(GL);
        prevLengthB,nextLengthB = startIndex,len(BL);
        while badIt.hasNext() or goodIt.hasNext():
            #attivazione campagna buona
            try:
                count = nextLengthG - prevLengthG;
                while count > 0:
                    node = goodIt.next();
                    NBRS = self.G.neighbors(node);
                    for nbr in NBRS:
                        if self.canTry(nbr,Campaign.Good):
                            if self.attempt(node,nbr):
                                self.activate(node,nbr,Campaign.Good,t);
                                goodIt.append(nbr);

                    count -= 1;
                prevLengthG = nextLengthG;
                nextLengthG = len(goodIt.L);
            except StopIteration:pass;
            #attivazione campagna malevola
            try:
                count = nextLengthB - prevLengthB;
                while count > 0:
                    node = badIt.next();
                    NBRS = self.G.neighbors(node);
                    for nbr in NBRS:
                        if self.canTry(nbr,Campaign.Bad):
                            #if self.attempt(node, nbr):
                                self.activate(node,nbr,Campaign.Bad,t);
                                badIt.append(nbr);
                    count -= 1;
                prevLengthB = nextLengthB;
                nextLengthB = len(badIt.L);
            except StopIteration:pass;
            t += 1;
        
        return t;

    def TimedIndependentCascade(self,L,tStop,c):
        '''    
        @param: L : seed
        @param: tStop : time step massimi
        @param: c : campaign
        '''
        t = 1;
        it = li.Wrap(L);
        prevLength = 0;
        nextLength = len(it.L);
        while it.hasNext() and t<=tStop:
            count = nextLength - prevLength;
            while count > 0:
                node = it.next();
                #print "tryin with node {}".format(node);
                NBRS = self.G.neighbors(node);
                for nbr in NBRS:
                    if self.canTry(nbr,c):
                        #print "node {} trying to activate {}".format(node,nbr);
                        if self.attempt(node,nbr):
                            #print "node {} activate {}".format(node,nbr);
                            self.activate(node,nbr,c,t);
                            it.append(nbr);
                count -=1;
            prevLength = nextLength;
            nextLength = len(it.L);
            t += 1;
        
        return prevLength;

    def alghoritm(self,SEED,delay,k,heuristic):
        '''
        Esegue l'intero algoritmo e restituisce
        la lista di nodi salvati

        @param: SEED : lista di nodi attivi nella campagna malevola
        @param: delay : tempo necessario affinche ci si accorga della campagna malevola
        @param: k : budget a disposizione
        @param: heuristic : metodi di determinazione della lista di nodi di partenza per la campagna benevola
        @return: lista di nodi salvati
        @return: lista di good
        @return: lista di bad
        @return: tempo massimo
        '''
        #faccio partire il processo di diffusione per la campagna malevola
        for x in SEED: self.active(x,Campaign.Bad,0);

        startIndex = self.TimedIndependentCascade(SEED,delay,Campaign.Bad);
        print "[TIMED INDEPENDENT CASCADE] {}".format(SEED);

        #determino il seed di partenza per la campagna benevola
        GL = heuristic(SEED,k);
        for x in GL: self.active(x,Campaign.Good,delay);
        t = self.MultiCampaign(GL,SEED,delay,startIndex);
        return self.getSaved(),GL,self.getInfected(SEED),t;



# *********************** #
# GraphHandler principale #
# *********************** #
class RealGraphHandler(GraphHandler):
    def isActive(self, node):
        return self.G.node[node].has_key(self.state) and self.G.node[node][self.state]!=NodeState.Inactive.value;
    
    def isActiveFor(self, node, campaign):
        return self.isActive(node) and self.G.node[node][self.state] == campaign.value;
    
    def canTry(self, node, campaign):
        if not self.isActive(node):
            return True;
        
        if campaign == Campaign.Bad:
            return not self.G.node[node].has_key(self.shadowState) or self.G.node[node][self.shadowState]!=campaign.value;
        
        return False;
        
    def activate(self,src,dst,campaign, time):
        if not self.isActiveFor(src,campaign) or self.isActive(dst):
            self.G.node[dst][self.shadowState] = campaign.value;
        else:
            self.G.node[dst][self.state] = campaign.value;
            self.G.node[dst][self.time] = time;
            if campaign == Campaign.Bad:
                self.G.node[dst][self.shadowState] = campaign.value;

    def active(self, node, campaign, time):
        self.G.node[node][self.state] = campaign.value;
        self.G.node[node][self.time] = time;
        if campaign == Campaign.Bad:
            self.G.node[node][self.shadowState] = campaign.value;

    
    def getSaved(self):
        return [x for x in self.G if self.isSaved(x)];
    
    def getInfected(self, L):
        for x in L:
            if not self.isActiveFor(x,Campaign.Bad):
                del L[L.index(x)];
        
        return L; 
    
    def isSaved(self,node):
        return self.G.node[node].has_key(self.shadowState) and (not self.isActive(node) or self.isActiveFor(node,Campaign.Good));
        
    def getSimulator(self):
        simulator = SimulationGraphHandler(randomSeed=self.randomSeed,G=self.G);
        simulator.weight = self.weight;
        return simulator;


# ******************************* #
# GraphHandler per le simulazioni #
# ******************************* #
class SimulationGraphHandler(GraphHandler):
    '''
    La classe non implementa gli stessi metodi
    con la differenza che non scrive sul grafo
    '''
    def __init__(self, graphFilePath = None, randomSeed = None,G = None):
        print "creating simulation handler"
        if graphFilePath != None:
            GraphHandler.__init__(self, graphFilePath,randomSeed)
        elif G != None:
            self.G = G;
            self.random = rand.Random(randomSeed);
        else:
            raise ('Cannot instantiate handler','specifies the right arguments');

        self.BL = []
        self.GL = [];
        self.SVD = set();

    def isActive(self,node):
        if node in self.GL:
		return True;
	else:
		return node in self.BL;

    def isActiveFor(self,node,campaign):
        if campaign == self.badC:
            return node in self.BL;
        elif campaign == self.goodC:
            return node in self.GL;

    def canTry(self,node,campaign):
        if campaign==self.badC:
            return node not in self.BL;

        return not self.isActive(node);

    def activate(self, node, campaign, time):
        pass;

    def save(self, node):
        self.SVD.add(node);

    def getSaved(self):
        return self.SVD;

    def MultiCampaign(self, BL, GL, startingTime=0):
        self.GL = GL;
        self.BL = BL;
        self.SVD = set();
        GraphHandler.MultiCampaign(self,self.BL,self.GL, startingTime)
