#!flask/bin/python
from home import app
app.run(debug=True)

"""
from dag_analyzer import course_catalog, determine_path
from catalog_scraper import read_catalog

prompt = "Type a number I guess: "

while(True):

	response = str(raw_input(prompt)).upper().replace(" ", "")

	determine_path(course_catalog[response])
"""