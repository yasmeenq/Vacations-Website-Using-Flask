from models.vacations_model import *
from models.client_error import *
from logic.vacations_logic import *
from datetime import datetime
from flask import request

class VacationsFacade:
    def __init__(self):
        self.logic = VacationsLogic()
    
    def get_all_vacations_sorted(self):
        return self.logic.get_all_vacations()

    def get_one_vacation(self, vacationID):
        return self.logic.get_one_vacation(vacationID)


    def add_new_vacation(self):
        countryName = request.form.get("countryName")
        description = request.form.get("description")
        startDate = request.form.get("startDate")
        endDate = request.form.get("endDate")
        price = request.form.get("price")
        vacationImage = request.files["vacationImage"]
        
        # Fetch or add the country and get the countryID
        countryID = self.logic.add_country_if_not_exists(countryName)
        
        new_vacation = VacationsModel(None, countryName, countryID, description, startDate, endDate, price, vacationImage)
        error = new_vacation.validate_insert()
        if error: 
            raise ValidationError(error, model={})
        return self.logic.add_new_vacation(new_vacation)


    def update_vacation(self, vacationID):
        vacationID = request.form.get("vacationID") #<input type=hidden...name = "vacationID">
        countryID = request.form.get("countryID") #<input type=text...name = "countryID">
        description = request.form.get("description")
        startDate = request.form.get("startDate")
        endDate = request.form.get("endDate")
        price = request.form.get("price")   #<input type=number...name = "price">
        vacationImage = request.files["vacationImage"]
        updated_vacation = VacationsModel(vacationID, countryID, description, startDate, endDate,price, vacationImage)
        error = updated_vacation.validate_edit()
        if error: raise ValidationError(error)
        return self.logic.update_vacation(updated_vacation)
    
    
    def delete_vacation(self, vacationID): 
        return self.logic.delete_vacation(vacationID)
    

    def get_previous_vacation_id(self, vacationID):
        return self.logic.get_previous_vacation_id(vacationID)

    def get_next_vacation_id(self, vacationID):
        return self.logic.get_next_vacation_id(vacationID)

    def close(self):
        self.logic.close()