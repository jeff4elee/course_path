from home import app
from dag_analyzer import course_catalog, determine_path
from catalog_scraper import read_catalog
from flask import render_template, flash, redirect, session, url_for, request, g
from .forms import CourseForm

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():

	form = CourseForm()

	if form.validate_on_submit():

		response = request.form.get('course')

		course_id = response.upper().replace(" ", "")

		path = determine_path(course_catalog[course_id])

		return render_template('index.html',
			form=form,
			course_path=path)

	return render_template('index.html',
		form=form)