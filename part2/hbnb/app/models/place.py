from app.models import BaseModel

class Place(BaseModel):
    def __init__(self,title,description,price,latitude,longitude,owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id    
        self.amenities = []  
        self.reviews = []   




    def add_amenity(self, amenity):
            
            self.amenities.append(amenity)


    def add_review(self, review):
            
            self.reviews.append(review)