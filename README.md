# autosuggestion
a code for autosuggesting suffix completion
build_fst.py is a code to construct the lm tree
html/index.html will eventually by the main page to write prefix in
html/cgi-bin/suggest_wrapper.py takes prefix from html to insert 
it to generate_suggestions.py found in autosgt.py
html/cgi-bin/autosgt.py generate a suggestion based on prefix.

While not optimally efficient (have ideas of how to reduce runtime) it should provide a suggestion given a prefix
based on the tree learned from sample.json
