import cgi
from autosgt import generate_suggestions

form = cgi.FieldStorage()
searchterm =  form.getvalue('searchbox')
generate_suggestions(searchterm)
