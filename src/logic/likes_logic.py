from flask import session
from utils.dal import DAL
import logging
from models.role_model import RoleModel

class LikesLogic:
    def __init__(self):
        self.dal = DAL()

    def add_like(self, userID, vacationID):
        user = session.get("current_user")
        userID = user["userID"]
        roleID = user["roleID"]

        if roleID is None or roleID == RoleModel.Admin.value:
            logging.info(f"User with userID {userID} is an admin or guest. Cannot like vacationID {vacationID}.")
            return False

        if roleID != RoleModel.User.value:
            logging.error(f"User with userID {userID} does not have the correct roleID to like vacationID {vacationID}.")
            return False

        try:
            sql = "INSERT INTO likes (userID, vacationID) VALUES (%s, %s)"
            params = (userID, vacationID)
            self.dal.insert(sql, params)
            logging.info(f"Like added for userID {userID} and vacationID {vacationID}.")
            return True
        except Exception as e:
            logging.error(f"Error adding like: {e}")
            return False


    def delete_like(self, userID, vacationID):
        try:
            sql = "DELETE FROM likes WHERE userID = %s AND vacationID = %s"
            params = (userID, vacationID)
            self.dal.delete(sql, params)
            logging.info(f"Like deleted for userID {userID} and vacationID {vacationID}.")
            return True
        except Exception as e:
            logging.error(f"Error deleting like: {e}")
            return False


    #incase of deletion
    def delete_all_likes(self, vacationID):
        try:
            sql = "DELETE FROM likes WHERE vacationID = %s"
            params = (vacationID,)
            self.dal.delete(sql, params)
            logging.info(f"All likes deleted for vacationID {vacationID}.")
            return True
        except Exception as e:
            logging.error(f"Error deleting likes: {e}")
            return False



    def get_like_count(self, vacationID):
        try:
            sql = "SELECT count(*) as like_count FROM likes WHERE vacationID = %s"
            params = (vacationID,)
            result = self.dal.get_scalar(sql, params)
            like_count = result['like_count'] if result else 0
            logging.debug(f"Like count for vacationID {vacationID}: {like_count}")
            return like_count
        except Exception as e:
            logging.error(f"Error getting like count: {e}")
            return 0

    def user_has_liked(self, userID, vacationID):
        try:
            sql = "SELECT COUNT(*) FROM likes WHERE userID = %s AND vacationID = %s"
            params = (userID, vacationID)
            result = self.dal.get_scalar(sql, params)
            has_liked = result['COUNT(*)'] > 0 if result else False
            logging.debug(f"User with userID {userID} has liked vacationID {vacationID}: {has_liked}")
            return has_liked
        except Exception as e:
            logging.error(f"Error checking if user has liked: {e}")
            return False

    def close(self):
        self.dal.close()
