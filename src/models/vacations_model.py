

class VacationsModel:
    def __init__(self, vacationID, countryName, countryID, description, startDate, endDate, price, vacationImage):
        self.vacationID = vacationID
        self.countryName = countryName
        self.countryID = countryID
        self.description = description
        self.startDate = startDate
        self.endDate = endDate
        self.price = price
        self.vacationImage = vacationImage
    
    def __str__(self) -> str:
        return f"vacationID: {self.vacationID}, countryID: {self.countryID}, countryName: {self.countryName}, description: {self.description}, startDate: {self.startDate}, endDate: {self.endDate}, price: {self.price}, vacationImage: {self.vacationImage}"
    
    @staticmethod
    def dictionary_to_object(dictionary) -> object:
        vacationID = dictionary["vacationID"]
        countryID = dictionary["countryID"]
        countryName = dictionary["countryName"]
        description = dictionary["description"]
        startDate = dictionary["startDate"]
        endDate = dictionary["endDate"]
        price = dictionary["price"]
        vacationImage = dictionary["vacationImage"]
        vacation = VacationsModel(vacationID,countryName, countryID, description,startDate,endDate,price,vacationImage)
        return vacation
    
    @staticmethod
    def dictionaries_to_objects(list_of_dictionaries) -> list:
        items = []
        for item in list_of_dictionaries:
            item = VacationsModel.dictionary_to_object(item)  #turn to object
            items.append(item)  #list of objects
        return items
    

    def validate_insert(self):
        if not self.countryName: return "missing country"
        if not self.description: return "missing description"
        if not self.startDate: return "missing start date"
        if not self.endDate: return "missing end date"
        if not self.price: return "missing price"
        
        if float(self.price) < 0 or float(self.price) > 10000: return "price must be 0-10000"
        return None #if no errors return nothing

    def validate_edit(self):
        if not self.countryName: return "missing country"
        if not self.description: return "missing description"
        if not self.startDate: return "missing start date"
        if not self.endDate: return "missing end date"
        if not self.price: return "missing price"
        
        if float(self.price) < 0 or float(self.price) > 10000: return "price must be 0-10000"
        return None #if no errors return nothing


