from hashlib import sha512
from utils.app_config import AppConfig

class Cyber:

    @staticmethod
    def hash(plain_text):
        #takes input
        encoded_text = plain_text.encode('utf-8') + AppConfig.password_salt.encode('utf-8') #check explanation below
        hashed_text = sha512(encoded_text).hexdigest()  #converts it to sha512 code
        return hashed_text

#the problem with hash code that there are websites that listed all words and names in the 
#dictionary and paired them with their hashcode so they can access any password they want 
#so what we'll do is add 'password salt' stored in .env, it can be anything random 
#so if the password of a user is abc it'll be coded abc + password salt 
# with that no one can know what's the password for each user 