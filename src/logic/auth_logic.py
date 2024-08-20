from utils.dal import DAL

class AuthLogic:
    def __init__(self):
       self.dal = DAL()

    #register
    def add_user(self, user):
        sql = "INSERT INTO vacations.users(firstname, lastname, password, email, roleID) VAlUES(%s,%s,%s,%s,%s)"
        self.dal.insert(sql, (user.firstname, user.lastname, user.password, user.email, user.roleID))
        
    #register email validation
    def is_email_taken(self, email):
        sql  = "SELECT EXISTS(SELECT * FROM  vacations.users WHERE email = %s) AS is_taken" #this returns true or false if taken/ is_taken is a variable name
        result = self.dal.get_scalar(sql, (email,))
        return result["is_taken"] == 1 #if 1 true if 0 false

    #login
    def get_user(self, credentials): #credentials contains email and password
        sql = "SELECT * FROM vacations.users WHERE email = %s AND password = %s "
        user = self.dal.get_scalar(sql, (credentials.email, credentials.password))
        return user


    def close(self):
        self.dal.close()