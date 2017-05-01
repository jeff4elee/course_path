from catalog_scraper import extract_catalog_dict, write_catalog, read_catalog
import json
import networkx as nx
from networkx.readwrite import json_graph
import os.path


if(os.path.isfile('courses.csv')):

	course_catalog = read_catalog('courses.csv')

else:

	course_ids, course_titles, course_pre = extract_catalog_dict(record=True)
	write_catalog(course_ids, course_titles, course_pre, record=True)
	course_catalog = read_catalog('courses.csv')

courses = {}

"""
ids, titles, pres = extract_catalog_dict(record=False)
catalog_info = zip(ids, titles, pres)
course_catalog = {}

for x, y, z in catalog_info:
	course_catalog[x.lower().replace(" ", "")] = (x, y, z)

print course_catalog
"""

def insert_into_course(key, value):

	if not type(value) is dict:
		raise TypeError("Value is not a dictionary!")

	if key not in courses:
		courses[key] = value
	else:
		courses[key].update(value)

def dfs(course_info):
	"""
		dfs(course_info)
			course_info -> 3-tuple in the format (string, string, list of strings)

		updates the courses dictionary to include the specified course and its prereqs
	"""

	#gets the id of the course
	i = course_info[0]

	#check if the courses dict already has the course path defined
	if i in courses:
		return {i: courses[i]}

	#retrieve the list of preqres for the course
	pr = [p for p in course_info[2]]

	# memoization table, check if keys in dict already exists
	for p in course_info[2]:

		if(isinstance(p, list)):
			
			insert_into_course(i, {" or ".join(p): p})
			pr.remove(p)

		elif p in courses:

			insert_into_course(i, {p: courses[p]})
			pr.remove(p)	

	# check if there are no prereqs (empty list)
	if not course_info[2]:
		courses[i] = i
		return {i : i}

	#stack consisting of the prerequisites
	course_stack = [pr]

	#stack or dfs to reproduce a DAG
	while(course_stack):

		curr_p = course_stack.pop()

		#iterate through the id of each prereq in the list
		for curr_i in curr_p:
	
			#check if the id is in the courses dict or the course_catalog dict
			#courses keys are fromatted like 'CSE 100'
			#course_catalog keys are formatted like 'CSE100' <-- notice no space
			if curr_i not in courses and curr_i.upper().replace(" ", "") in course_catalog:
				
				#retrieve the course_info from the catalog with the matching id
				c_info = course_catalog[curr_i.upper().replace(" ", "")]

				#retrieve prereq dictionary of current prereq 
				prereqs = dfs(c_info)

				#merge the prereq dictionary to the courses's current prereq dict
				insert_into_course(i, prereqs)

			#memoization in action
			elif curr_i in courses:

				insert_into_course(i, {curr_i: courses[curr_i]})

			#edge case, courses catalog doesn't contain the prereq
			elif curr_i.upper().replace(" ", "") not in course_catalog:

				insert_into_course(i, {curr_i : curr_i})

	return {i: courses[i]}

def determine_path(course):

	course_path = dfs(course)

	path = "Root: " + course[0] + ' - ' + course[1]

	#print_path(course_path[course[0]], 4)
	return calculate_path(course_path[course[0]], 3, path)

def print_path(dict_path, spaces, str_format=None):

	if not str_format:
		str_format = "Child:"

	if type(dict_path) is str:
		return

	if type(dict_path) is list:
		for item in dict_path:
			try:
				course = course_catalog[item.upper().replace(" ", "")]
				print_path(dfs(course), spaces+3, "Or Root:")
			except:
				continue

	else:
		for key in dict_path.iterkeys():
			print " "*spaces + str_format, key
			print_path(dict_path[key], spaces+3)

def calculate_path(dict_path, spaces, path, str_format=None):
	"""
		calculate_path(dict_path, spaces, path, str_format=None)
			dict_path --> dictionary of the course and its prerequisites
			spaces --> spacing of the format
			path --> initial string to set before the path display
			str_format --> for the children!

		returns a string representation (used for html) of the specified
		dictionary path (a course and its prerequisites)
	"""

	if not str_format:
		str_format = "Child:"

	#str indicates no further path, so return the path as is
	if type(dict_path) is str:
		return path

	#list indicates 'or prerequisites'
	#parse and calculate each individual path with a special format
	if type(dict_path) is list:
		for item in dict_path:
			try:
				course = course_catalog[item.upper().replace(" ", "")]
				path += calculate_path(dfs(course), spaces, " ", "Or Root:")
			except:
				continue

	#regular dictionary path, continue recursively (dfs)
	else:
		for key in dict_path.iterkeys():
			path += "<br>" + "&emsp;"*spaces + str_format + " " + key
			path += calculate_path(dict_path[key], spaces+3, " ")

	return path

def generate_graph(course):

	G = nx.DiGraph()

	course_path = dfs(course)
#	path = "Root: " + course[0] + ' - ' + course[1]

	G.add_node(course[0], name=course[0], group="Root Course")

	def generate_path(G, parent, dict_path):

		if type(dict_path) is str:
			return

		if type(dict_path) is list:
			for item in dict_path:
				try:
					G.add_node(item, name=item, group="Or Courses")
	
					G.add_edge(parent, item)

					course = course_catalog[item.upper().replace(" ", "")]
					generate_path(G, item, dfs(course))
				except:
					continue

		else:
			
	#		G.add_edges_from([(parent, key) for key in dict_path.iterkeys()])

			for key in dict_path.iterkeys():

				G.add_node(key, name=key)
				G.add_edge(parent, key)
		
				generate_path(G, key, dict_path[key])

	#print_path(course_path[course[0]], 4)
	generate_path(G, course[0], course_path[course[0]])

	d = json_graph.node_link_data(G) # node-link format to serialize
	json.dump(d, open('home/static/force.json','w'))
