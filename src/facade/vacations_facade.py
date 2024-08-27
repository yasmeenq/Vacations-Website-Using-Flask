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


    def add_new_vacation(self, vacation_data):
        # Extract data from passed dictionary
        countryName = vacation_data.get("countryName")
        description = vacation_data.get("description")
        startDate = vacation_data.get("startDate")
        endDate = vacation_data.get("endDate")
        price = vacation_data.get("price")
        vacationImage = vacation_data.get("vacationImage")
        
        # Fetch or add the country and get the countryID
        countryID = self.logic.add_country_if_not_exists(countryName)
        
        # Validate dates
        if startDate > endDate:
            raise ValidationError("Start date cannot be greater than end date.")
        
        # Check if in the past
        start_date = datetime.strptime(startDate, '%Y-%m-%d')
        end_date = datetime.strptime(endDate, '%Y-%m-%d')
        current_date = datetime.now().date()
        if start_date.date() < current_date or end_date.date() < current_date:
            raise ValidationError("Dates cannot be in the past.")
        
        # Handle image
        if not vacationImage or vacationImage.filename == '':
            vacationImage = None
            
        # Create the new vacation object
        new_vacation = VacationsModel(None, countryName, countryID, description, startDate, endDate, price, vacationImage)
        
        # Validate the vacation data
        error = new_vacation.validate_insert()
        if error:
            raise ValidationError(error, model=vacation_data)
        
        return self.logic.add_new_vacation(new_vacation)


    def update_vacation(self, vacationID):
        vacationID = request.form.get("vacationID")
        countryName = request.form.get("countryName")
        description = request.form.get("description")
        startDate = request.form.get("startDate")
        endDate = request.form.get("endDate")
        price = request.form.get("price")
        vacationImage = request.files["vacationImage"]

        # Fetch or add the country and get the countryID if not exists
        countryID = self.logic.add_country_if_not_exists(countryName)
        if not countryID:
            raise ValidationError(f"Country '{countryName}' not found.")

        # Validate dates
        if startDate > endDate:
            raise ValidationError("Start date cannot be greater than end date.")
        
        updated_vacation = VacationsModel(vacationID, countryName, countryID, description, startDate, endDate, price, vacationImage)
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