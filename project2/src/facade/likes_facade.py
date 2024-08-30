from utils.dal import DAL
from logic.likes_logic import LikesLogic

class LikesFacade:
    def __init__(self):
        self.logic = LikesLogic()
    
    def like(self, userID, vacationID):
        return self.logic.add_like(userID, vacationID)

    def unlike(self, userID, vacationID):
        return self.logic.delete_like(userID, vacationID)

    def unlike_all(self, vacationID):
        return self.logic.delete_all_likes(vacationID)

    def get_like_count(self, vacationID):
        return self.logic.get_like_count(vacationID)

    def user_has_liked(self, userID, vacationID):
        return self.logic.user_has_liked(userID, vacationID)
    
    def close(self):
        self.logic.close()
