"""
   Extract three best suggestions given a prefix
"""
import fst
import operator
import json

def dfs(branch, sym):
    """
    This funciton extract all paths in fst.
    It discards repetitions and sorts by the path list
    by path weight.
    INPUT:
       branch is an fst
    OUTPUT:
        sym is the fst symbol system used for branch.

    """
    
    f_paths = []
    prev = ""
    for i, path in enumerate(branch.paths()):
        path_istring = ''.join(sym.find(arc.ilabel) for arc in path)
        path_weight = reduce(operator.mul, (arc.weight for arc in path))
        if prev != path_istring:
            f_paths.append((path_istring, path_weight.__float__()))
            #print('{} / {}'.format(path_istring[1:], path_weight))
        prev = path_istring
        
    # sort by weight given that one~tropw(0) zero~tropw(inf)
    ranked = sorted(f_paths, key=lambda w: w[1])
    return ranked[:3]
    

def bfs(stateid, allLM, sym):
    """
    This part extract and constuct the branch fst 
    in a bds apprach to later extract its paths easily.
    It numbers states from zero id regardless of state id
    in original tree.
    INPUT:
       state to begin create branch from
       allLM the big tree fst
       sym symbol system of allLM
    OUTPUT:
        branch, an fst of desired branch
    
    """
    
    branch = fst.Acceptor(syms = sym)
    stack = [stateid]
    st_encod = {}
    i = 0
    while stack:
        
        state = allLM[stack[0]]
        if i==0:
            sid = i
            i+=1
        else:
            sid = st_encod[state.stateid]
        
        for arc in state:
            nextst = arc.nextstate

            try:# encode states beginning from id 0
                st_encod[nextst]
            except:
                st_encod[nextst] = i
                i+=1            
            
            stack.append(nextst)
            label = sym.find(arc.ilabel)
            w = arc.weight
            branch.add_arc(sid, st_encod[nextst], label, w)
        stack = stack[1:]
    branch[i-1].final = True
    
    return branch
    
def generate_suggestions(prefix):
    """
    To extract suggestions the first step was to traverse the fst
    in fstfile following the charecters of the given prefix. From
    there the state of the final letter of prefix is saved and the next
    part constructs an fst of the branch the grows from the saved state.
    It is done in bds approach. Later, extract all paths from acceptor in
    a dfs manner is done with path weight calculation. Then all paths 
    are sorted by weights and the first three are jsoned.
    INPUT:
       a string
    OUTPUT:
       a json file with up to three values for Suggestion entry
    """    

    # toy example
    fstfile = "/Users/dudy/CSLU/summerIntern/src/all1.fst"
    sym = fst.read_symbols("/Users/dudy/CSLU/summerIntern/src/syms")
    lm = fst.read(fstfile)    
    
    # look for subtree given prefix
    for (state, ch) in zip(lm.states, prefix):
        for arc in state.arcs:
            if sym.find(arc.ilabel)==ch:
                stateid = arc.nextstate
                state = lm[stateid]
                break
            
    # construct desired subtree (bds)
    reduced = bfs(stateid, lm, sym)

    # read strings (dfs)
    top3 = dfs(reduced, sym)
    
    # take first three (if exists)
    suggest = []
    for (suffix, _) in top3:
        suggest.append(suffix)
    
    # dict it    
    result = {}
    result["Suggestions:"] = suggest
        
    # json it
    json_file = "../auto.json"
    with open(json_file, "w") as fp:
        json.dump(result, fp)
        
    

generate_suggestions("I")