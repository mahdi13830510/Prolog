def is_variable(term):
    if is_number(term):
        return False
    elif term <= "Z" or term == "_":
        return True
    else:
        return False
    
def is_number(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

def rh_val_get(rh_arg, lh_arg, rh_domain):
    if is_variable(rh_arg):
        rh_val = rh_domain.get(rh_arg)
    else:
        rh_val = rh_arg
    
    return rh_val
  
def unifiable_check(nterms, rh, lh):
    if nterms != len(lh.terms): 
        return False
    if rh.predicate != lh.predicate: 
        return False
    
def lh_eval(rh_val, lh_arg, lh_domain):
    if is_variable(lh_arg):  #variable in destination
        lh_val = lh_domain.get(lh_arg)
        if not lh_val: 
            lh_domain[lh_arg] = rh_val
            #return lh_domain
        elif lh_val != rh_val:
            return False          
    elif lh_arg != rh_val: 
        return False

def unify(lh, rh, lh_domain = None, rh_domain = None):
    if rh_domain is None:
        rh_domain = {} #dict(zip(rh.terms, rh.terms))
    if lh_domain is None:
        lh_domain = {}
        
    nterms = len(rh.terms)
    if unifiable_check(nterms, rh, lh) is False:
        return False
    
    for i in range(nterms):
        rh_arg  = rh.terms[i]
        lh_arg = lh.terms[i]
        
        if lh_arg == "_": 
            continue
        
        rh_val = rh_val_get(rh_arg, lh_arg, rh_domain)
        
        if rh_val:    # fact or variable in search
            if lh_eval(rh_val, lh_arg, lh_domain) is False:
                return False
    
    return True
    
