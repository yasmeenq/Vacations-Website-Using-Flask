


class ClientError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message 


class ResourceNotFoundError(ClientError):
    def __init__(self, id):
        super().__init__(f"{id} not found")
        self.id = id

#validation error: if user input incorrect data or whatnot
class ValidationError(ClientError):
    def __init__(self, message, model=None):
        super().__init__(message)
        self.model = model

#auth error: if user and password are incorrect  
class AuthError(ClientError):
    def __init__(self, message, model=None):
        super().__init__(message)
        self.model = model