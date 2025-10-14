from app.models import BaseModel

class Amenity(BaseModel):
        def __init__(self,name):
            super().__init__() 
            self.name = name

            self._validate()
        def _validate(self): 
              
            if len(self.first_name) > 50:
                raise ValueError("Amenity too long")

