from flask import Flask, render_template, session, request
from views.vacation_view import vacation_blueprint
from views.auth_view import auth_blueprint
from views.home_view import home_blueprint
from logging import getLogger, ERROR
from utils.app_config import AppConfig
from models.role_model import RoleModel
from logging import getLogger, ERROR

app = Flask(__name__)
app.secret_key = AppConfig.session_secret_key  #a secret key for the sessions#how many sessions do we have? maybe a thousand #how many uses are logged in
app.register_blueprint(vacation_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(home_blueprint)

#for role models
@app.context_processor
def inject_user():
    return dict(current_user=session.get('current_user'))
     
@app.context_processor
def inject_role_model():
    return dict(RoleModel=RoleModel)


#error handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html") 

#always use this for safety 
@app.errorhandler(Exception) #for all other errors that im not aware of 
def catch_all(error):
    print(error)
    return render_template('500.html', error=error)
# werkzeug - ארגז כלים 
getLogger("werkzeug").setLevel(ERROR)


if __name__ == '__main__':
    app.run(debug=True)