from catalog_scraper import extract_catalog_dict, write_catalog

courses = {}

ids, titles, pres = extract_catalog_dict(record=False)

catalog_info = zip(ids, titles, pres)

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

		if p in courses:

			insert_into_course(i, {p: courses[p]})
			pr.remove(p)

	# check if there are no prereqs (empty list)
	if not course_info[2]:
		courses[i] = i
		return {i : i}

	course_stack = [pr]

	#stack or dfs to reproduce a DAG
	while(course_stack):

		curr_p = course_stack.pop()

		#iterate through the id of each prereq in the list
		for curr_i in curr_p:
	
			#check if the id is in the courses/ids
			if curr_i not in courses and curr_i in ids:
				
				#retrieve the course_info from the catalog with the matching id
				c_info = next(x for x in catalog_info if x[0] == curr_i)

				#retrieve prereq dictionary of current prereq 
				prereqs = dfs(c_info)

				#merge the prereq dictionary to the courses's current prereq dict
				insert_into_course(i, prereqs)

			#memoization in action
			elif curr_i in courses:

				insert_into_course(i, {curr_i: courses[curr_i]})

			#edge case, courses catalog doesn't contain the prereq
			elif curr_i not in ids:

				insert_into_course(i, {curr_i : curr_i})

	return {i: courses[i]}

def determine_path(course):

	course_path = dfs(course)

	print "Root:", course[0]

	print_path(course_path[course[0]], 4)

def print_path(dict_path, spaces):

	if type(dict_path) is str:
		return

	else:
		for key in dict_path.iterkeys():
			print " "*spaces + "Child: " + key
			print_path(dict_path[key], spaces+4)
