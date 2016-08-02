'''
Created on 16 mag 2016

@author: antonio
'''
import unittest

import algorithm.graphandler3 as gh;
import algorithm.heuristics as h;
from algorithm.graphandler2 import GraphHandler , NodeState, Campaign;

class Test(unittest.TestCase):


    def setUp(self):
        print 'setting up';
        self.RGH = gh.RealGraphHandler('../graphs/generated100.txt',randomSeed=100,weigthed=True);
        self.h = h.OutDegree();
        self.h.setGraphHandler(self.RGH);
        self.seed = 1;
        # come seed prendo sempre il nodo piu influente
        self.BL = [ x for x,y in sorted(self.RGH.G.out_degree().items(),key=lambda x:x[1],reverse=True)][:self.seed];
        
    def testSeedNotInfected(self):
        SAVED,GL,self.BL,t = self.RGH.alghoritm(self.BL, 0, 1, self.h);
        print "SAVED:{} GL:{} BL:{}".format(len(SAVED),len(GL),len(self.BL));
        for x in SAVED:
            print (x,self.RGH.G.node[x]);
        
#         for x in self.RGH.G:
#             print (x,self.RGH.G.node[x]);
        
#         for x in self.BL:
#             if self.RGH.G.node[x][GraphHandler.state] != NodeState.Bad.value:
#                 self.fail("{}:{}".format(x,self.RGH.G.node[x]));
#                 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    #SAVED:405 GL:410 BL:449