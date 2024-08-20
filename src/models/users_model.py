from email_validator import validate_email, EmailNotValidError
from models.role_model import RoleModel

class UsersModel:
    def __init__(self, userID, firstname, lastname, email, password, roleID):
        self.userID = userID
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.roleID = roleID
    
    def __str__(self) -> str:
        return (f"userID: {self.userID}, firstname: {self.firstname}, lastname: {self.lastname}, "
                f"email: {self.email}, password: {self.password}, roleID: {self.roleID}")
    
    def validate_register(self):
        # Check for missing fields
        if not self.firstname:
            return "Missing firstname"
        if not self.lastname:
            return "Missing lastname"
        if not self.email:
            return "Missing email"
        if not self.password:
            return "Missing password"
        if not self.roleID:
            return "Missing roleID"
        
        # Validate field lengths
        if len(self.firstname) < 2 or len(self.firstname) > 100:
            return "Firstname must be between 2 and 100 characters"
        if len(self.lastname) < 2 or len(self.lastname) > 100:
            return "Lastname must be between 2 and 100 characters"
        if len(self.password) < 5 or len(self.password) > 20:
            return "Password must be between 5 and 20 characters"

        # Validate email format
        try:
            validate_email(self.email)
        except EmailNotValidError:
            return "Invalid email address"

        # Validate roleID
        if self.roleID != RoleModel.Admin.value and self.roleID != RoleModel.User.value:
            return "Invalid role"

        return None  # No validation errors