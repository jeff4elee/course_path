import requests
import sqlite3
import csv
from course import Course, CourseArchive
from bs4 import BeautifulSoup

def clean_list(list_to_clean):
	
	data_to_remove = []

	for i in range(len(list_to_clean)):
		
		list_to_clean[i] = clean(list_to_clean[i].text.encode('utf-8'))

		#if u"\xa0".encode('utf-8') in c.text.encode('utf-8'):
		#	print c.text.encode('utf-8').strip().split()
		
		if not list_to_clean[i].split():
			data_to_remove.insert(0, i)

		
	for i in data_to_remove:
		list_to_clean.pop(i)

	return list_to_clean
		
def clean(string):

	replace_values = [(u"\xa0".encode('utf-8'), " "), (u"\u2014".encode('utf-8'), "-"), \
					(u"\u0027".encode('utf-8'), "'"), (u"\u2013".encode('utf-8'), "-"), \
					(u"\u2019".encode('utf-8'), "'")]

	for utf, new in replace_values:
		string = string.replace(utf, new)

	return " ".join(string.split())
	#return " ".join(string.replace(u"\u2013".encode('utf-8'), '-').split())

def writeCourses(courses):

	with open('courses.csv', 'wb') as csvfile:
		for course in courses:
			spamwriter = csv.writer(csvfile)

			row_to_write = [course.name()] + [pre for pre in course.prereq()]

			spamwriter.writerow(row_to_write)


page = requests.get("http://ucsd.edu/catalog/courses/CSE.html")

soup = BeautifulSoup(page.content, 'html.parser')

course_names = clean_list(soup.find_all('p', class_='course-name'))
course_dscrpts = clean_list(soup.find_all('p', class_='course-descriptions'))

course_info = zip(course_names, course_dscrpts)

courses = []

course_archive = {}

for course in course_info:
	
	course_name = course[0]
	
	course_full_dscrpt = course[1].split("Prerequisites:", 1)

	course_dscrpt = course_full_dscrpt.pop(0)
	course_prereq = "none."

	if course_full_dscrpt:
		course_prereq = course_full_dscrpt.pop(0)

	courses.append(Course(course_name, course_dscrpt, course_prereq))

for course in courses:

	course_archive[course.name()] = course
#	print str(course)
#	print course.prereq()
#	print ""

#writeCourses(courses)

ca = CourseArchive(courses)

while(True):

	course_id = raw_input("Course ID: ")

	print "" 

	ca.get_prereqs(course_id)