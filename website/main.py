from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route("/")
def index():

    if not current_user.is_authenticated:
        return render_template("index.html")

    courses = []
    for c in current_user.courses:
        courses.append({
            "id": c.id,
            "name": c.name,
            "link": c.link,
            "status": str(c.status) # looping to convert enum type to string
        })

    return render_template("index.html", courses=courses[::-1])

@main.route("/profile")
@login_required
def profile():

    to_start_courses = 0
    going_on_courses = 0
    finished_courses = 0

    for c in current_user.courses:

        if str(c.status) == "CourseStatusEnum.TO_START":
            to_start_courses += 1
        elif str(c.status) == "CourseStatusEnum.GOING_ON":
            going_on_courses += 1
        else:
            finished_courses += 1

    return render_template("profile.html",
                           name=current_user.name,
                           to_start_courses=to_start_courses,
                           going_on_courses=going_on_courses,
                           finished_courses=finished_courses)

