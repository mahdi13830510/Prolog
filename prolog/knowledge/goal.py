from typing import Self, Dict
class Goal :
    def __init__ (self: Self, fact, parent = None, domain: Dict={}, ind = 0) :
        self.fact = fact
        self.parent = parent  ## parent goal which is a step above in the tree
        ## to keep the domain of the goal independent 
        ## as we will change domains a lot in the search
        self.domain = {}
        self.domain.update(domain)
        self.ind = ind
        
    def __copy__(self: Self):
        return Goal(self.fact, self.parent, self.domain, self.ind)    

    def __repr__ (self: Self) :
        return "Goal = %s, parent = %s" % (self.fact, self.parent)
        
    def __lt__(self: Self, other):
        return self.fact.lh.terms[self.fact.lh.index] < other.fact.lh.terms[other.fact.lh.index]
        