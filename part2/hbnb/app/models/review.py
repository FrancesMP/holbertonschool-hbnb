from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, rating, comment):
        super().__init__()
        self.rating = rating
        self.comment = comment
        self._validate()  
        
    def _validate(self):
        """Validate review attributes"""
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if not self.comment or len(self.comment.strip()) == 0:
            raise ValueError("Comment cannot be empty")