from app.models import BaseModel

class Amenity(BaseModel):
        def __init__(self,name):
            super().__init__() 
            self.name = name

            self._validate()
        def _validate(self):
            """Validate amenity attributes"""
            if len(self.name) > 50:  
                raise ValueError("Amenity name too long")
            if not self.name or len(self.name.strip()) == 0:
                raise ValueError("Amenity name cannot be empty")