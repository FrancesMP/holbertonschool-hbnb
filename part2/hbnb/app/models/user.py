from app.models import BaseModel

class User(BaseModel):
    def __init__(self,first_name,last_name,email,is_admin=False):
        super().__init__() 
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        self._validate()
        
        def _validate(self):
            """Validate user attributes"""
        if len(self.first_name) > 50:
            raise ValueError("First name too long")
        if len(self.last_name) > 50:
            raise ValueError("Last name too long")