import re
from itertools import chain
from more_itertools import unique_everseen
from query.unify import unify
from knowledge.goal import Goal

#__all__ = ["is_number", "is_variable", "rh_val_get", "unifiable_check", "lh_eval"] #used in unify module        
    
def rule_terms(rule_string):  ## getting list of unique terms
    s = re.sub(" ", "", rule_string)
    s = re.findall(r"\((.*?)\)", s)
    s = [i.split(",") for i in s]
    s = list(chain(*s))
    return list(unique_everseen(s))
    
def term_checker(expr):
    #if not isinstance(expr, Expr):
    #    expr = Expr(expr)
    terms = expr.terms[:]
    indx = [x for x,y in enumerate(terms) if y <= "Z"]
    for i in indx:
        ## give the same value for any uppercased variable in the same index
        terms[i] = "Var" + str(i)
    #return expr, "%s(%s)" % (expr.predicate, ",".join(terms))
    return indx, "%s(%s)" % (expr.predicate, ",".join(terms))
    
def get_path(db, expr, path):
    terms = db[expr.predicate]["facts"][0].lh.terms
    path = [{k: i[k] for k in i.keys() if k not in terms} for i in path]
    pathe = [] 
    for i in path:
        for k,v in i.items():
            pathe.append(v)
    return set(pathe)

def answer_handler(answer):
    if len(answer) == 0: 
        answer.append("No")  ## if no answers at all return "No" 
        return answer
    
    elif len(answer) > 1:
        if any(ans != "Yes" for ans in answer):
            answer = [i for i in answer if i != "Yes"]
        elif all(ans == "Yes" for ans in answer):
            return answer_handler([])
            
    return answer
       
def parent_inherits(rl, rulef, currentgoal, Q):
    for f in range(len(rulef)): ## loop over corresponding rules
        ## take only the ones with the same predicate and same number of terms
        if len(rl.terms) != len(rulef[f].lh.terms):
            continue
        ## a father goal is the rule we need to search inheriting the domain of the grandfather    
        father = Goal(rulef[f], currentgoal)
        ## unify current rule fact lh with father rhs to get grandfather domain inherited
        uni = unify(rulef[f].lh, rl,
                    father.domain, ## saving in father domain
                    currentgoal.domain) ## using current goal domain (query input)
        if uni: Q.push(father) ## if unify succeeds add father to queue to be searched
        
def child_assigned(rl, rulef, currentgoal, Q):   
    if len(currentgoal.domain) == 0 or all(i not in currentgoal.domain for i in rl.terms):
        for f in range(len(rulef)): ## loop over corresponding facts
            ## take only the ones with the same predicate and same number of terms
            if len(rl.terms) != len(rulef[f].lh.terms):
                continue
            ## a child goal from the current fact with current goal as parent    
            child = Goal(rulef[f], currentgoal)
            ### if there is nothing to unify then push to the queue directly
            Q.push(child)
    else:
        key = currentgoal.domain.get(rl.terms[rl.index])
        if not key or rulef[0].rhs:
            first, last = (0, len(rulef))
        else:
            first, last = fact_binary_search(rulef, key)
        for f in range(first, last): ## loop over only corresponding facts
            ## take only the ones with the same predicate and same number of terms
            if len(rl.terms) != len(rulef[f].lh.terms):
                continue
            ## a child goal from the current fact with current goal as parent    
            child = Goal(rulef[f], currentgoal)
            ## unify current rule fact lh with current goal rhs to get child domain
            uni = unify(rulef[f].lh, rl,
                        child.domain, ## saving in child domain
                        currentgoal.domain) ## using current goal domain
            if uni: Q.push(child) ## if unify succeeds add child to queue to be searched
            
def child_to_parent(child, Q): # which is the current goal
    parent = child.parent.__copy__() #to ensure that parent's domain is different without affecting children's
    unify(parent.fact.rhs[parent.ind], ## unify parent goals
          child.fact.lh,  ## with their children to go step down
          parent.domain,
          child.domain)
    parent.ind += 1 ## next rh in the same goal object (lateral move) 
    Q.push(parent) ## add the parent to the queue to be searched


def fact_binary_search(facts, key):
    # search for the indices of the key in the facts heap
    # start to get last occurrence index at the right side
    right = 0
    length = len(facts)
    while right < length:
        middle = (right + length) // 2
        f = facts[middle]
        if key < f.lh.terms[f.lh.index]:
            length = middle
        else: 
            right = middle + 1
    # now first occurence at the left side
    left = 0
    length = right - 1
    while left < length:
        middle = (left + length) // 2
        f = facts[middle]
        if key > f.lh.terms[f.lh.index]: 
            left = middle + 1
        else: 
            length = middle
    
    if left == right == 0: # if facts aren't sorted with index 0
        left, right = (0, len(facts))
            
    return left, right #- 1
    