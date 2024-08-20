from flask import Blueprint, render_template, send_file, url_for, redirect, request, jsonify, session
from facade.vacations_facade import VacationsFacade
from utils.image_handler import ImageHandler
from models.client_error import *
from facade.likes_facade import LikesFacade
import logging
from models.vacations_model import VacationsModel

vacation_blueprint = Blueprint("vacation_view", __name__)

vacations_facade = VacationsFacade()
likes_facade = LikesFacade()

@vacation_blueprint.route("/")
@vacation_blueprint.route("/vacations")
def list():
    all_vacations = vacations_facade.get_all_vacations_sorted()  # List of dictionaries
    vacations_objects = VacationsModel.dictionaries_to_objects(all_vacations)

    user = session.get('current_user')
    if user is None:
        user_id = 0  
        role_id = 0
    else:
        if isinstance(user, dict):
            user_id = user.get('userID', 0)
            role_id = user.get('roleID', 0)
        try:
            user_id = int(user_id)
            role_id = int(role_id)
        except ValueError:
            user_id = 0
            role_id = 0

    # Collect like count and user like status for each vacation
    vacation_data = []
    for vac in vacations_objects:
        vacation_id = vac.vacationID
        like_count = likes_facade.get_like_count(vacation_id)
        user_has_liked = likes_facade.user_has_liked(user_id, vacation_id)
        vacation_data.append({
            "vacation": vac,
            "like_count": like_count,
            "user_has_liked": user_has_liked,
        })

    return render_template('vacations.html', 
                           vacation_data=vacation_data,
                           user_id=user_id, 
                           role_id=role_id)





@vacation_blueprint.route("/vacations/images/<string:image_name>")
def get_image(image_name):
    image_path = ImageHandler.get_image_path(image_name)
    return send_file(image_path)



@vacation_blueprint.route("/vacations/details/<int:id>")
def details(id):
    user = session.get('current_user')
    
    print("Debug details: user from session:", user)
    
    if user is None:
        user_id = 0  
        role_id = 0
    else:
        # Check type of user
        if isinstance(user, dict):
            # Extract the actual user ID and role ID from the dictionary
            user_id = user.get('userID', 0)  # Ensure to get userID
            role_id = user.get('roleID', 0)  # Ensure to get roleID
        try:
            user_id = int(user_id)  # Ensure user_id is an integer
            role_id = int(role_id)  # Ensure role_id is an integer
        except ValueError:
            user_id = 0  # Handle conversion failure appropriately
            role_id = 0  # Handle conversion failure appropriately
    
    # Fetch vacation details
    one_vacation = vacations_facade.get_one_vacation(id)
    previous_vacation_id = vacations_facade.get_previous_vacation_id(id)
    next_vacation_id = vacations_facade.get_next_vacation_id(id)
    
    # Calculate like count and whether the user has liked this vacation
    like_count = likes_facade.get_like_count(id)
    user_has_liked = likes_facade.user_has_liked(user_id, id)
    
    return render_template("details.html", 
                           vacation=one_vacation, previous_vacation_id=previous_vacation_id, next_vacation_id=next_vacation_id, 
                           like_count=like_count,user_has_liked=user_has_liked, 
                           user_id=user_id, role_id=role_id)


@vacation_blueprint.route("/vacation/<int:vacationID>/<action>", methods=["POST"])
def handle_like(vacationID, action):
    try:
        user = session.get('current_user')
        
        if isinstance(user, dict):
            user_id = user.get('userID')
        else:
            return jsonify({"success": False, "error": "User not authenticated."}), 401
        
        if not isinstance(user_id, int):
            return jsonify({"success": False, "error": "Invalid user ID."}), 400
        
        if action == "like":
            success = likes_facade.like(user_id, vacationID)
        elif action == "unlike":
            success = likes_facade.unlike(user_id, vacationID)
        else:
            return jsonify({"success": False, "error": "Invalid action."}), 400

        if success:
            like_count = likes_facade.get_like_count(vacationID)
            return jsonify({"success": True, "like_count": like_count})
        else:
            return jsonify({"success": False, "error": "Failed to update like status."}), 500
    except Exception as e:
        logging.error(f"Error handling like/unlike: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@vacation_blueprint.route("/vacations/new", methods=["GET", "POST"])
def insert():
    try:
        if(request.method=="GET"): return render_template("insert.html")
        #else "POST" when u click the button add
        vacations_facade.add_new_vacation()
        return redirect(url_for("vacation_view.list"))
    except AuthError as err:
        return redirect(url_for("auth_view.login", error= err.message, credentials={}))  #if anonymous not logged in return him to login page if he wants to insert stuff
    except ValidationError as err:
        return render_template('insert.html', error= err.message, model = err.model)    




@vacation_blueprint.route("/vacations/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    try:
        if(request.method=="GET"): 
            one_vacation = vacations_facade.get_one_vacation(id)
            return render_template("edit.html", vacation= one_vacation)
        
        vacations_facade.update_vacation(id)
        return redirect(url_for("vacation_view.list"))
    except AuthError as err:
        all_vacations = vacations_facade.get_all_vacations_sorted() 
        return render_template("vacations.html", error=err.message, vacations= all_vacations)
    except ValidationError as err:
        return render_template("edit.html",error=err.message)


@vacation_blueprint.route("/vacations/delete/<int:id>")
def delete(id):
    try:
        user = session.get('current_user')  # Fetch the user from the session
        if user is None:
            raise AuthError("User not logged in.")
        
        userID = user.get('userID')  # Extract the userID
        if not userID:
            raise AuthError("Invalid user session.")
        
        # Unlike the vacation first
        likes_facade.unlike_all(id)
        
        # Then delete the vacation
        vacations_facade.delete_vacation(id)
        
        return redirect(url_for("vacation_view.list"))
    except AuthError as err:
        all_vacations = vacations_facade.get_all_vacations_sorted()
        return render_template("vacations.html", error=err.message, vacations=all_vacations)
