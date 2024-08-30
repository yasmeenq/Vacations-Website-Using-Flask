from flask import request, session
from logic.auth_logic import AuthLogic
from models.users_model import UsersModel
from models.role_model import RoleModel
from models.client_error import *
from models.credentials_model import *
from utils.cyber import Cyber

class AuthFacade:
    def __init__(self):
        self.logic = AuthLogic()

    def register(self):
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        user = UsersModel(None, first_name, last_name, email, password, RoleModel.User.value)
        
        error = user.validate_register() 
        if error: raise ValidationError(error, user)
        if self.logic.is_email_taken(email): raise ValidationError("Email already exists", user)
        user.password = Cyber.hash(user.password)

        user_id = self.logic.add_user(user) #returns userID
        if user_id is None:
            raise ValueError("Failed to retrieve user ID after registration")
        user.userID = user_id  

        print(f'user added: {user}')
        print(f'{user_id}')

        # Store user details in the session
        session["current_user"] = {
            "userID": user.userID,  
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "roleID": user.roleID
        }
        return user



    def login(self):
        print("Login facade called")  
        email = request.form.get('email')
        password = request.form.get('password')
        
        credentials = CredentialModel(email, Cyber.hash(password)) 
        error = credentials.validate_login()
        if error: raise ValidationError(error, credentials)

        user = self.logic.get_user(credentials)
        print(f"User retrieved: {user}")
        
        if not user: raise AuthError("Incorrect email or password", credentials) #pass credentials so it saves email and password incase of error so it wont be deleted everytime
        #Assaf used  AuthError("Incorrect email or password", user) but i see that this is more accurate
        
        del user['password'] #delete from session dictionary password key
        
        session["current_user"] = user  #save user in the session


    def logout(self):
        print("Logging out user. Clearing session.")
        session.clear()  #delete everything you saved temporarily, any saved things are now saved to the database.


    #block guests - view only 
    def block_anonymous(self): 
        user = session.get("current_user")
        if not user: raise AuthError("you are not logged in")

    #block non admin 
    def block_user(self):
        user = session.get("current_user")
        if not user: raise AuthError("you are not logged in")
        if user["roleID"] != RoleModel.Admin.value: raise AuthError("you are not allowed")
        
    #block non user
    def block_admin(self):
        user = session.get("current_user")
        if not user: raise AuthError("you are not logged in")
        if user["roleID"] != RoleModel.User.value: raise AuthError("you are not allowed")        


    def close(self):
        self.logic.close()