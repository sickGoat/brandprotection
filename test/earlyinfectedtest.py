'''
Created on 16 mag 2016

@author: antonio
'''
import unittest

import algorithm.graphandler2 as gh;
import algorithm.heuristics as h;
from algorithm.graphandler2 import GraphHandler


class Test(unittest.TestCase):


    def setUp(self):
        print 'setting up';
        self.RGH = gh.RealGraphHandler('../graphs/generated50.txt',randomSeed=100,weigthed=True);
        self.h = h.EarlyInfected();
        self.h.setGraphHandler(self.RGH);
        self.seed = 1;
        # come seed prendo sempre il nodo piu influente
        self.BL = [ x for x,y in sorted(self.RGH.G.out_degree().items(),key=lambda x:x[1],reverse=True)][:self.seed];
        
    def test1(self):
        SAVED,GL = self.RGH.alghoritm(self.BL, 2, 2, self.h);
        print "Nodi salvati:{}\nNodi buoni:{}".format(GL,SAVED);
        for x in self.BL:
            if x in GL:
                self.fail("{} in entrambe le liste BL GL".format(x));
            if x in SAVED:
                self.fail("{} in entrembe le liste BL SAVED".format(x));
            
        for x in SAVED:
            if self.RGH.canTry(x, GraphHandler.badC) or self.RGH.canTry(x,GraphHandler.goodC):        
                self.fail("{} non e' stato salvato".format(x));
                
        
        for x in GL:
            if self.RGH.isActiveFor(x,GraphHandler.badC):
                self.fail("{}:{} non e' stato attivato dalla campagna malevola".format(x,self.RGH.G.node[x]));
        
        for x in GL:
            if x in SAVED and  (not self.RGH.isActiveFor(x,GraphHandler.goodC) or self.RGH.G.node[x][GraphHandler.badTry]==False):
                self.fail("{}:{}".format(x,self.RGH.G.node[x]));
        
        for x in SAVED:
            if x not in GL:
                self.fail("come cazzo e' possibile");
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()