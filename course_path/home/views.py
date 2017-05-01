from home import app
from catalog_scraper import read_catalog
from flask import render_template, flash, redirect, session, url_for, request, g
from .forms import CourseForm
from dag_analyzer import generate_graph, course_catalog

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():

	form = CourseForm()

	if form.validate_on_submit():

		response = request.form.get('course')

		course_id = response.upper().replace(" ", "")

		path = generate_graph(course_catalog[course_id])
		
		return render_template('index.html',
			form=form,
			read=True)

	return render_template('index.html',
		form=form)