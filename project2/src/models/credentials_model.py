from email_validator import validate_email, EmailNotValidError

class CredentialModel:
    def __init__(self, email, password) :
        self.email = email
        self.password = password

    def validate_login(self):
        #protection from hackers
        if not self.email: return "INCORRECT EMAIL"
        if not self.password: return "INCORRECT PASSWORD"
        try:
            validate_email(self.email)
        except EmailNotValidError:
            return "one of the parameters are not correct"
        return None #if there's no error return nth