import re

class Course:

	def __init__(self, course_name, course_description, course_prereq):

		# 1+ letters, space, 1+ digits, 1 letter
		pattern = "[a-zA-Z]+\s?[0-9]+[a-zA-Z]?"
		
		or_pattern = "(?:[a-zA-Z]+\s?[0-9]+[a-zA-Z]?)+(?: or [a-zA-Z]+\s?[0-9]+[a-zA-Z]?)+"

		#retrieves the course title and id
		self.course_name = re.match(pattern, course_name).group(0)
		
		#sets the course id
		self.string_name = course_name

		#sets the full description of the course
		self.course_description = course_description

		#sets the prerequisites of the course
		self.course_prereq = re.findall(pattern, course_prereq)
		self.prereq_ors = re.findall(or_pattern, course_prereq)
		
		#check prereq classes which clear the same class
		for prereq in self.prereq_ors:
			
			prereq = prereq.split(" or ")

			for p in prereq:
				self.course_prereq.remove(p)

		if self.prereq_ors:
			self.course_prereq += self.prereq_ors

		#sets the string representation of the prerequisite
		self.string_prereq = "Prerequisites:" + course_prereq

	def name(self):
		return self.course_name

	def description(self):
		return self.course_description

	def prereq(self):
		return self.course_prereq

	def __str__(self):
		return self.string_name + "\n" + self.course_description + "\n" + \
				self.string_prereq

class CourseArchive:

	def __init__(self, course_list):

		self.course_archive = {}

		self.marked_courses = {}

		for c in course_list:
			self.course_archive[c.name()] = c
			self.marked_courses[c.name()] = False

	def get(self):
		return self.course_archive

	#wrapper function to recursively print prereqs and to cleanse the hashmap
	def get_prereqs(self, course_id):

		#self.prereq_chain(course_id)
		#self.bfs_prereqs(course_id)
		self.dfs_prereqs(course_id)
		self.cleanse()

	#recursive call to print the prerequisite classes
	def prereq_chain(self, course_id):

		print course_id,

		if course_id not in self.course_archive:
			return

		#gets the course and prereqs
		course = self.course_archive[course_id]
		prereqs = course.prereq()
		self.marked_courses[course_id] = True
		
		#base case, no prereqs, leaf course
		if not prereqs:
			print "\n"
			return

		#for every prerequisite, print in-order traversal
		for prereq in prereqs:
 
			print "Prereq: " + prereq + "\n"
			
			p_ors = prereq.split(" or ")

			for p in p_ors:

				#if the current course hasn't been marked, or doesn't exist, mark it
				if p in self.marked_courses and self.marked_courses[p]:
					continue

				self.marked_courses[p] = True

				if p not in self.course_archive:
					continue

				self.prereq_chain(p)

	def bfs_prereqs(self, course_id):

		"""Finds the chain of prereqs of a certain course using BFS"""

		if course_id not in self.course_archive:
			print course_id + "\n"
			return

		queue = [self.course_archive[course_id]]
		self.marked_courses[course_id] = True

		print "Root: " + course_id + "\n"

		while queue:

			course = queue.pop(0)

			if course.name() != course_id:
				print "Course: " + course.name()

			for prereq in course.prereq():

				if "or" in prereq:

					print prereq
					pre_ors = prereq.split(" or ")

					for c in pre_ors:

						if c not in self.course_archive or self.marked_courses[c]:
							continue

						self.marked_courses[c] = True
						queue.append(self.course_archive[c])
				else:

						if prereq not in self.course_archive or self.marked_courses[prereq]:
							continue

						self.marked_courses[prereq] = True
						queue.append(self.course_archive[prereq])

		print ""

	def dfs_prereqs(self, course_id):

		"""Finds the chain of prereqs of a certain course using BFS"""

		if course_id not in self.course_archive:
			print course_id + "\n"
			return

		stack = [self.course_archive[course_id]]
		self.marked_courses[course_id] = True

		print "Root: " + course_id + "\n"

		while stack:

			course = stack.pop()

			if course.name() != course_id:
				print "Course: " + course.name()

			for prereq in course.prereq():

				if "or" in prereq:

					print prereq
					pre_ors = prereq.split(" or ")

					for c in pre_ors:

						if c not in self.course_archive or self.marked_courses[c]:
							continue

						self.marked_courses[c] = True
						stack.append(self.course_archive[c])
				else:

						if prereq not in self.course_archive or self.marked_courses[prereq]:
							continue

						self.marked_courses[prereq] = True
						stack.append(self.course_archive[prereq])

		print ""

	#unmarks all courses from the hashmap
	def cleanse(self):

		for key in self.marked_courses.iterkeys():

			self.marked_courses[key] = False

	def __str__(self):
		return self.string_name + "\n" + self.course_description + "\n" + \
				self.string_prereq