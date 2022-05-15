from flask import Blueprint, request, render_template, flash, redirect
from flask_login import current_user
from validators import url as is_url
from . import db
from .models import Course

courses = Blueprint('courses', __name__)


@courses.route("/add-course", methods=["GET", "POST"])
def add_course():
    if request.method == "GET":
        return render_template("add_course.html")

    name = request.form.get("name")
    link = request.form.get("link")
    status = request.form.get("status")

    if (name == "") or (link == "") or (status == ""):
        flash("All fields are required")
        return redirect("/add-course")

    if not is_url(link):
        flash(f"This is not a valid url: {link}")
        return redirect("/add-course")

    new_course = Course(name=name, link=link, status=status)
    current_user.courses.append(new_course)
    db.session.add(new_course)
    db.session.add(current_user)
    db.session.commit()

    return redirect("/")

@courses.route("/mark-as-learning/<int:id>")
def mark_as_learning(id):

    course_to_edit = Course.query.get(id)
    course_to_edit.status = "GOING_ON"

    db.session.add(course_to_edit)
    db.session.commit()

    return redirect("/")

@courses.route("/mark-as-finished/<int:id>")
def mark_as_finished(id):

    course_to_edit = Course.query.get(id)
    course_to_edit.status = "COMPLETED"

    db.session.add(course_to_edit)
    db.session.commit()

    return redirect("/")

@courses.route("/mark-as-to-start/<int:id>")
def mark_as_to_start(id):

    course_to_edit = Course.query.get(id)
    course_to_edit.status = "TO_START"

    db.session.add(course_to_edit)
    db.session.commit()

    return redirect("/")

@courses.route("/delete/<int:id>")
def delete_course(id):

    Course.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect("/")

@courses.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_course_details(id):

    course_to_edit = Course.query.get(id)

    if request.method == "GET":
        return render_template("edit_course.html", course=course_to_edit)

    name = request.form.get("name")
    link = request.form.get("link")

    if (name=="") and (link==""):
        flash("Nothing to edit!")
        return redirect(f"/edit/{id}")

    if (name==course_to_edit.name) and (link==course_to_edit.link):
        flash("Nothing to edit!")
        return redirect(f"/edit/{id}")

    if not name == course_to_edit.name:
        course_to_edit.name = name

    if not link == course_to_edit.link:

        if not is_url(link):
            flash(f"This is not a valid url: {link}")
            return redirect(f"/edit/{id}")
        course_to_edit.link = link

    db.session.add(course_to_edit)
    db.session.commit()

    return redirect("/")

