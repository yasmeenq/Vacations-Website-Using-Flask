from pathlib import Path
from flask import current_app
from uuid import uuid4

class ImageHandler:  #this deals with the images on the disc only not with database
    
    @staticmethod
    def save_image(image): #image is a file
        if not image : return None
        suffix = Path(image.filename).suffix  #the ending(suffix) of image - egg.png suffix is png
        image_name = str(uuid4())+ suffix  #create unique name 12312-fwq13-f214af
        image_path = Path(current_app.root_path) / "static/images" / image_name #static/images/12312-fwq13-f214af.png
        image.save(image_path) #save image on the server side(to my project to disc) on static/images/12312-fwq13-f214af.png
        return image_name  #so we can save its name to mysql database 
 
    @staticmethod
    def get_image_path(image_name):
        image_path = Path(current_app.root_path) / "static/images" / image_name
        if not image_path.exists():
            image_path = Path(current_app.root_path) / "static/images/no-image.png" 
        return image_path
    
    @staticmethod
    def update_image(old_image_name, image):
        if not image.filename: return old_image_name
        image_name = ImageHandler.save_image(image)  #function from above
        ImageHandler.delete_image(old_image_name)  #delete old image
        return image_name
    
    @staticmethod
    def delete_image(image_name):  #delete old image
        if not image_name: return  #if theres no image return nothing
        if image_name == "no-image.png":
            return
        image_path = Path(current_app.root_path) / "static/images" / image_name
        image_path.unlink(missing_ok = True)  #deletes file