from knowledge.fact import Fact
from knowledge.goal import Goal
from query.pq import FactHeap
from query.querizer import rule_query


class Interpreter(object):
    __id = 0
    def __init__(self, name = None):
        self.db = {}
        if not name:
            name = "_%d" % Interpreter.__id
        self.id = Interpreter.__id
        Interpreter.__id += 1
        self.name = name
        self._cache = {}
    
    ## the main function that adds new entries or append existing ones
    ## it creates "facts", "goals" and "terms" buckets for each predicate
    def add_kn(self, kn):
        for i in kn:
            i = Fact(i)
            ## rhs are stored as Expr here we change class to Goal
            g = [Goal(Fact(r.to_string())) for r in i.rhs]
            if i.lh.predicate in self.db:
                self.db[i.lh.predicate]["facts"].push(i)
                self.db[i.lh.predicate]["terms"].push(i.terms)
                self.db[i.lh.predicate]["goals"].push(g)
                #self.db[i.lh.predicate]["terms"].append(i.terms)
            else:
                self.db[i.lh.predicate] = {}
                self.db[i.lh.predicate]["facts"] = FactHeap()
                self.db[i.lh.predicate]["facts"].push(i)
                self.db[i.lh.predicate]["goals"] = FactHeap()
                self.db[i.lh.predicate]["goals"].push(g)
                self.db[i.lh.predicate]["terms"] = FactHeap()
                self.db[i.lh.predicate]["terms"].push(i.terms)
        # console.print(self.db)
                #self.db[i.lh.predicate]["goals"] = [g]
                #self.db[i.lh.predicate]["terms"] = [i.terms]
            
    def __call__(self, args):
        self.add_kn(args)

    ## query method will only call rule_query which will call the decorators chain
    ## it is only to be user intuitive readable method                                      
    def query(self, expr, cut = False, show_path = False):
        return rule_query(self, expr, cut, show_path)
        
    def rule_search(self, expr):
        if expr.predicate not in self.db:
            return "Rule does not exist!"
        else:
            res = []
            rule_f = self.db[expr.predicate]
            for f in range(len(rule_f["facts"])):
                if len(expr.terms) != len(rule_f["facts"][f].lh.terms):
                    continue
                res.append(rule_f["facts"][f])
        return res

    def __str__(self):
        return "Interpreter: " + self.name
        
    def clear_cache(self):
        self._cache.clear()

    __repr__ = __str__
    
    