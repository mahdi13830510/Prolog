import re
from knowledge.fact import Fact
from knowledge.goal import Goal

def prob_parser(domain, rule_string, rule_terms):
    if "is" in rule_string:
        s = rule_string.split("is")
        key = s[0]
        value = s[1]
    else:
        key = list(domain.keys())[0]
        value = rule_string
    for i in rule_terms:
        if i in domain.keys():
            value = re.sub(i, str(domain[i]), value)
    value = re.sub(r"(and|or|in|not)", r" \g<0> ", value) ## add spaces after and before the keywords so that eval() can see them
    return key, value

def prob_calc(currentgoal, rl, Q):
    ## Probabilities and numeric evaluation
    key, value = prob_parser(currentgoal.domain, rl.to_string(), rl.terms)
    ## eval the mathematic operation
    value = eval(value)
    if value is True: 
        value = currentgoal.domain.get(key)
        ## it is true but there is no key in the domain (helpful for ML rules in future)
        if value is None:
            value = "Yes"
    elif value is False:
        value = "No"
    currentgoal.domain[key] = value ## assign a new key in the domain with the evaluated value
    prob_child = Goal(Fact(rl.to_string()),
                      parent = currentgoal,
                      domain = currentgoal.domain)
    Q.push(prob_child)

def filter_eq(rule, currentgoal, Q):
    # apply inequality check
    currentgoal.domain = {k:v for k,v in currentgoal.domain.items() if currentgoal.domain[rule.terms[0]] != currentgoal.domain[rule.terms[1]]}

    prob_child = Goal(Fact(rule.to_string()),
                      parent = currentgoal,
                      domain = currentgoal.domain)
    Q.push(prob_child)