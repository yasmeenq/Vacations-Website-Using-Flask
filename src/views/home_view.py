from flask import Blueprint, render_template, session


home_blueprint = Blueprint('home_view', __name__)

@home_blueprint.route("/")
@home_blueprint.route("/home")
def home():
    user = session.get('current_user', {})
    return render_template("home.html", current_user = user)