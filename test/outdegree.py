'''
Created on 02 mag 2016

@author: antonio
'''
import unittest
import algorithm.graphandler2 as gh;
import algorithm.heuristics as he;


class Test(unittest.TestCase):


    def setUp(self):
        print 'setting up';
        self.RGH = gh.RealGraphHandler('../graphs/instagram.txt',randomSeed=100,weigthed=False);

    @unittest.skip('ok')
    def testIC(self):
        L = [0];
        self.GH.TimedIndependentCascade(L, 1, gh.Campaign.Bad);
        if self.GH.G.node[0].has_key('active'):
            self.fail("Grafo modificato");
        print L;
        for x in L:
            if L.count(x)>1:
                self.fail("{} appears more than once".format(x));
        for x in L:
            if self.GH.G.node[x].has_key(gh.NodeState.State):
                self.fail("il grafo e' stato modificato");
            
    @unittest.skip('ok')
    def testMC(self):
        self.GH.MultiCampaign([41], [0]);
        print self.GH.GL;
        print self.GH.BL;
        print self.GH.SVD;
        
        for x in self.GH.BL:
            if x in self.GH.GL:
                self.fail("{} contenuto in entrambe le liste".format(x))
        for x in self.GH.BL:
            if self.GH.BL.count(x)>1:
                self.fail("{} appears more than once".format(x));
        for x in self.GH.GL:
            if self.GH.GL.count(x)>1:
                self.fail("{} appears more than once".format(x));
        if len(self.GH.SVD)>len(self.GH.GL):
            self.fail("come cazzo e' possibile");
        
        for x in self.GH.SVD:
            if x not in self.GH.GL:
                self.fail("come cazzo e' possibile");
    
    
    @unittest.skip('ok')
    def testAlghoritm(self):
        greedy = he.GreedyHeuristic(self.RGH.getSimulator());
        BL = [0];
        SAVED,GL = self.RGH.alghoritm(BL, 1, 2, greedy);
        print GL;
        print BL;
        print SAVED;
        
    
    def testLargestInfected(self):
        li = he.LargestInfected(self.RGH,run=2);
        L = li([0,1],2);
        print L;
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()