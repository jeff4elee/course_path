import json
import networkx as nx
from networkx.readwrite import json_graph
import flask
from dag_analyzer import dfs, course_catalog

G = nx.DiGraph()

print dfs(course_catalog["CSE12"])

def determine_path(course):

	course_path = dfs(course)

#	path = "Root: " + course[0] + ' - ' + course[1]

	G.add_node(course[0], name=course[0])

	#print_path(course_path[course[0]], 4)
	return generate_path(course[0], course_path[course[0]])

def generate_path(parent, dict_path):

	if type(dict_path) is str:
		return

	if type(dict_path) is list:
		for item in dict_path:
			try:
				G.add_node(item, name=item)
				G.add_edge(parent, item)

				course = course_catalog[item.upper().replace(" ", "")]
				generate_path(item, dfs(course))
			except:
				continue

	else:
		
#		G.add_edges_from([(parent, key) for key in dict_path.iterkeys()])

		for key in dict_path.iterkeys():

			G.add_node(key, name=key)
			G.add_edge(parent, key)
	
			generate_path(key, dict_path[key])

course_path = determine_path(course_catalog["CSE100"])


# write json formatted data
d = json_graph.node_link_data(G) # node-link format to serialize
# write json
json.dump(d, open('force/force.json','w'))
print('Wrote node-link JSON data to force/force.json')

# Serve the file over http to allow for cross origin requests
app = flask.Flask(__name__, static_folder="force")

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)
print('\nGo to http://localhost:8000/force.html to see the example\n')
app.run(port=8000)