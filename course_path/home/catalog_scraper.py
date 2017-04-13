import requests
import csv
import time
import re
from bs4 import BeautifulSoup

CSE_CATALOG_URL = 'https://cse.ucsd.edu/undergraduate/courses/prerequisites-cse-undergraduate-classes'

def clean(string, utf8=None):

	string = string.encode('utf-8')

	replace_values = [(u"\xa0".encode('utf-8'), " "), (u"\u2014".encode('utf-8'), "-"), \
					(u"\u0027".encode('utf-8'), "'"), (u"\u2013".encode('utf-8'), "-"), \
					(u"\u2019".encode('utf-8'), "'")]

	for utf, new in replace_values:
		string = string.replace(utf, new)

	if utf8 and utf8 is True:
		return " ".join(string.split()).encode('utf-8')

	return " ".join(string.split())

def extract_catalog_dict(record):

	course_ids = []
	course_titles = []
	course_prereqs = []

	if record:
		start = time.time()
		print "Requesting access to the UCSD catalog page at %s..." % CSE_CATALOG_URL
	page = requests.get(CSE_CATALOG_URL)

	if record:
		print "Webscraping the catalog..."
	soup = BeautifulSoup(page.content, 'html.parser')

	table = soup.find('table')

	# Find all the <tr> tag pairs, skip the first one, then for each.
	for row in table.find_all('tr')[1:]:

		col = row.find_all('td')

		cse_course = clean(col[0].text.strip(), True)
		course_ids.append(cse_course)

		title = clean(col[1].text.strip(), True)
		course_titles.append(title)

		#creates a list of preqreqs, with a few rules
		#NO CO-REQUISITES
		#NO SELF-DEPENDENCIES
		prereqs = col[2].text.strip().split('***', 1)[0].split('Co-requisite', 1)[0].split('co-requisite', 1)[0]
		prereqs = clean(prereqs.replace(cse_course, ""), True)

		# 1 capital letter, 0+ letters, space, 1+ digits, 0 or 1 letter
		# i.e. 'CSE 30' or 'CSE 8A'
		pattern = "[A-Z][a-zA-Z]*\s?[0-9]+[a-zA-Z]?"
		or_pattern = "(?:[a-zA-Z]+\s?[0-9]+[a-zA-Z]?)+(?: or [a-zA-Z]+\s?[0-9]+[a-zA-Z]?)+"

		# creates a list of prereqs based on the regex
		or_filter = re.findall(or_pattern, prereqs)
		reg_filter = re.findall(pattern, prereqs)

		filtered_prereqs = [course for course in reg_filter if not any(course in c for c in or_filter)]
		filtered_prereqs += [courses.split(" or ") for courses in or_filter]

		course_prereqs.append(filtered_prereqs)

	if record:
		end = time.time()
		print "Completed scraping... %.3f seconds" % (end-start)

	write_catalog(course_ids, course_titles, course_prereqs, record)

	return course_ids, course_titles, course_prereqs

def write_catalog(ids, titles, prereqs, record):

	if record:
		start = time.time()
		print "Writing to the csv file 'courses.csv'..."

	with open('courses.csv', 'wb') as csvfile:

		writer = csv.writer(csvfile)

		rows = zip(ids, titles, prereqs)

		writer.writerows(rows)

	if record:
		end = time.time()
		print "Completed writing to file... %.3f seconds" % (end-start)

def read_catalog(csv_file):

	catalog = []

	with open(csv_file, 'rb') as csvfile:
		
		reader = csv.reader(csvfile)

		for row in reader:

			c_id = row[0]
			c_title = row[1]
			
			c_prereqs = ''.join([x for x in row[2] if x not in ["'", "[", "]"]]).split(', ')
			
			#makes a copy to loop through and remove 'or prerequisites'
			c_p_copy = [c for c in c_prereqs]

			or_pattern = "\[[a-zA-Z0-9, ]+]"
			
			#finds and parses the string for 'or prerequisites'
			or_c_prereqs = re.findall(or_pattern, row[2][1:-1].replace("'", ""))
			
			#parses the list of 'or prerequisites'
			for i in range(len(or_c_prereqs)):
				or_c_prereqs[i] = or_c_prereqs[i][1:-1].split(', ')

			#removes any courses in the 'or prerequisites'
			for c in c_p_copy:
				if any(c in course for course in or_c_prereqs):
					c_prereqs.remove(c)

			#combine the lists and remove any empty strings
			c_prereqs += or_c_prereqs
			c_prereqs = filter(None, c_prereqs)

			catalog.append((c_id, c_title, c_prereqs))

	course_catalog = {}

	#create a dictionary of the courses and the prereqs
	#use course_id as key, a tuple of id/title/prereq as value
	for x, y, z in catalog:
		course_catalog[x.upper().replace(" ", "")] = (x, y, z)

	return course_catalog