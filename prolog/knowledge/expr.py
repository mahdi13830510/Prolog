from typing import Self
import re

class Expr:
    def __init__ (self: Self, fact):
        self._parse_expr(fact)
            
    def _parse_expr(self: Self, fact):
        fact = fact.replace(" ", "")
        self.f = fact
        splitting = r"is|\*|\+|\-|\/|>=|<=|>|<|and|or|in|not"
        if "(" not in fact: 
            fact = "(" + fact + ")"
        pred_ind = fact.index("(")
        self.predicate = fact[:pred_ind]

        self.terms = fact[pred_ind:]
        to_remove = str.maketrans("", "", "() ")
        self.terms = self.terms.translate(to_remove)
        if self.predicate == "":
            self.terms = re.split(splitting, self.terms)
        else:
            self.terms = self.terms.split(",")
        self.string = self.f
        self.index = 0
    
    ## return string value of the expr in case we need it elsewhere with different type
    def to_string(self: Self):
        return self.string

    def __repr__ (self: Self) :
        return self.string
        
    def __lt__(self: Self, other):
        return self.terms[self.index] < other.terms[other.index]