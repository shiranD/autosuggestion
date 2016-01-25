"""
   Extract rep text fileds. Sort. Build a prefix tree. 
   Save the fst to an fst object
"""
import json
import fst

rep_text = []
file_directory = "../Data_Engineer_ASAPP_Challenge/sample_conversations.json"
json_data=open(file_directory).read()
data = json.loads(json_data)
for msg in data["Issues"]:
    for cstmr in msg["Messages"]:
        if cstmr["IsFromCustomer"] is False:
            rep_text.append(cstmr["Text"].lower())
            
rep_text = sorted(rep_text)
# extract words for syms

# build prefix tree
#rep_text = ["I'm", "I'm at", "I want", "what are","what he", "where?"]
syms = fst.SymbolTable()
prompt_main = fst.Acceptor(syms)

for pmt in rep_text:
    prompt = fst.Acceptor(syms)    
    for i, ch in enumerate(pmt):
        prompt.add_arc(i, i+1, ch, 1)
    prompt[i+1].final = True
    
    prompt_main.set_union(prompt)
    prompt_main.remove_epsilon()
    prompt_main = prompt_main.determinize()
    prompt_main.minimize()    
    prompt_main = prompt_main.push_weights(final=False)
    
# write to dot and draw
names = ["prfx_tree"]
obj = [prompt_main]
for name, o in zip(names, obj):
    with open(name+".dot", "w") as f:
        f.write(o.draw())
    with open(name+".fst", "w") as f:
        o.write(name+".fst")
    
sym = prompt_main.isyms
sym.write("syms")