"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    # github = "jhacks"

    first, last, github = hackbright.get_student_by_github(github)

    title, grade = hackbright.get_grades_by_github(github)

    # return "{} is the GitHub account for {} {}".format(github, first, last)

    html = render_template("student_info.html",
                            first=first, 
                            last=last, 
                            github=github,
                            title=title,
                            grade=grade)

    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add-form")
def student_add_form():
    """show form to add student"""

    return render_template("student_add_form.html")

@app.route("/student-add", methods=['POST'])
def student_add():
    """ add student"""

    first = request.form.get('first')
    last = request.form.get('last')
    github = request.form.get('github')

    hackbright.make_new_student(first, last, github)

    return render_template("student_added.html",first=first, last=last, github=github)

@app.route("/project")
def project_info():
    """Show form for searching for a student."""

    title = request.args.get('title')

    # title = "Markov"

    title, description, max_grade = hackbright.get_project_by_title(title)

    student_grade = hackbright.get_grades_by_title(title)

    return render_template("project_info.html",
                            title=title,
                            description=description,
                            max_grade=max_grade,
                            student_grade=student_grade)

@app.route("/")
def homepage():
    """this the homepage for students and projects."""

    all_students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()

    return render_template("homepage.html",
                            all_students=all_students,
                            projects=projects)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    # app.run(debug=True)
    app.run(debug=True, host="0.0.0.0")
