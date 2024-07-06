from utils.utils import rule_terms
from typing import Self
import re
from knowledge.expr import Expr

class Fact:
    def __init__ (self: Self, fact):
        self._parse_fact(fact)
        
    def _parse_fact(self: Self, fact):
        fact = fact.replace(" ", "")
        self.terms = rule_terms(fact)
        if ":-" in fact: 
            if_ind = fact.index(":-")
            self.lh = Expr(fact[:if_ind])
            # print(f"lh: {self.lh} for fact: {fact}")
            replacements = {"),": ")AND", ");": ")OR"}  ## AND OR conditions placeholders
            replacements = dict((re.escape(k), v) for k, v in replacements.items()) 
            pattern = re.compile("|".join(replacements.keys()))
            rh = pattern.sub(lambda x: replacements[re.escape(x.group(0))], fact[if_ind + 2:])
            rh = re.split("AND|OR", rh)
            # print(f"rh: {rh} for fact: {fact}")
            self.rhs = [Expr(g) for g in rh] 
            rs = [i.to_string() for i in self.rhs]
            self.fact = (self.lh.to_string() + ":-" + ",".join(rs))
        else:   ## to store normal expr as facts as well in the database
            self.lh = Expr(fact)
            self.rhs = []
            self.fact = self.lh.to_string()
    
    ## returning string value of the fact
    def to_string(self: Self):
        return self.fact

    def __repr__ (self: Self) :
        return self.fact
        
    def __lt__(self: Self, other):
        return self.lh.terms[self.lh.index] < other.lh.terms[other.lh.index]
        