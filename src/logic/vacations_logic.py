from utils.dal import DAL
from utils.image_handler import ImageHandler
from models.vacations_model import VacationsModel
from models.client_error import *

class VacationsLogic:
    def __init__(self):
        self.dal = DAL()

    def get_all_vacations(self):
        sql = """SELECT vacations.*, 
                countries.countryName 
                FROM vacations
                JOIN countries ON vacations.countryID = countries.countryID 
                ORDER BY startDate DESC"""
        return self.dal.get_table(sql)

    def get_one_vacation(self, vacationID):
        sql = """SELECT vacations.*, 
                countries.countryName 
                FROM vacations
                JOIN countries ON vacations.countryID = countries.countryID 
                WHERE vacations.vacationID = %s"""
        return self.dal.get_scalar(sql, (vacationID,))

    def add_new_vacation(self, vacation):
        # Fetch country ID from country name
        countryID = self.add_country_if_not_exists(vacation.countryName)
        if not countryID:
            raise ValidationError("Invalid country name", model={})
        
        # Save the image and insert the new vacation
        image_name = ImageHandler.save_image(vacation.vacationImage)
        sql = """
        INSERT INTO vacations (countryID, description, startDate, endDate, price, vacationImage)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        params = (countryID, vacation.description, vacation.startDate, vacation.endDate, vacation.price, image_name)
        return self.dal.insert(sql, params)  # returns last_row_id
    
    def add_country_if_not_exists(self, countryName):
        # Check if the country already exists
        sql = "SELECT countryID FROM countries WHERE countryName = %s;"
        params = (countryName,)
        result = self.dal.get_scalar(sql, params)
        
        if result:
            # Country already exists, return its ID
            return result['countryID']
        
        # Country does not exist, insert it
        sql_insert = "INSERT INTO countries (countryName) VALUES (%s);"
        params_insert = (countryName,)
        self.dal.insert(sql_insert, params_insert)  # Perform the insert operation
        
        # Fetch the last inserted ID
        sql_last_id = "SELECT LAST_INSERT_ID() AS countryID;"
        new_country_id = self.dal.get_scalar(sql_last_id)
        
        return new_country_id['countryID'] if new_country_id else None

    def get_country_name_by_id(self, id):
        sql = "SELECT countryName FROM countries WHERE countryID = %s;"
        params = (id,)
        result = self.dal.get_scalar(sql, params)
        return result['countryName'] if result else None



    def update_vacation(self, vacation):
        old_image_name = self.get_old_image_name(vacation.vacationID)
        image_name = ImageHandler.update_image(old_image_name, vacation.vacationImage)
        sql = """
            UPDATE vacations.vacations
            SET countryID = %s, description = %s, startDate = %s, endDate = %s, price = %s, vacationImage = %s
            WHERE vacationID = %s;
            """
        params = (vacation.countryID, vacation.description, vacation.startDate, vacation.endDate, vacation.price, image_name, vacation.vacationID)
        return self.dal.update(sql, params)

    def get_old_image_name(self, vacationID):
        sql = "SELECT vacationImage FROM vacations.vacations WHERE vacationID= %s"
        result = self.dal.get_scalar(sql, (vacationID,))
        return result["vacationImage"]

    def delete_vacation(self, vacationID):
        # delete the product and the image from the database
        image_name = self.get_old_image_name(vacationID)
        ImageHandler.delete_image(image_name)
        sql = "DELETE FROM vacations.vacations WHERE vacationID = %s"
        return self.dal.delete(sql, (vacationID,))

    def get_previous_vacation_id(self, vacationID):
        sql = """
            SELECT vacationID
            FROM vacations.vacations
            WHERE vacationID < %s
            ORDER BY vacationID DESC
            LIMIT 1
        """
        result = self.dal.get_scalar(sql, (vacationID,))
        if result:
            return result['vacationID']
        return None

    def get_next_vacation_id(self, vacationID):
        sql = """
            SELECT vacationID
            FROM vacations.vacations
            WHERE vacationID > %s
            ORDER BY vacationID ASC
            LIMIT 1
        """
        result = self.dal.get_scalar(sql, (vacationID,))
        if result:
            return result['vacationID']
        return None


    def close(self):
        self.dal.close()
