'''
Created on 22 apr 2016

@author: antonio
'''

def Wrap(L):
    if type(L)!=type([]):
        raise ('Input Errato','argomento deve essere una lista');
    return ListWrapper(L);

class ListWrapper(object):
    
    def __init__(self,L):
        self.L = L;
        self.lastIndex = 0;
        
    def next(self):
        if self.lastIndex == len(self.L):
            raise StopIteration;
        item = self.L[self.lastIndex];
        self.lastIndex += 1;
        return item;
    
    def previous(self):
        if self.lastIndex == 0:
            return self.L[self.lastIndex];
        self.lastIndex -= 1;
        return self.L[self.lastIndex];
    
    def hasNext(self):
        return len(self.L)>self.lastIndex;
    
    def append(self,item):
        self.L.append(item);
        
    def setPosition(self,index):
        if index >= len(self.L):
            raise ValueError;
        self.lastIndex = index;
        
