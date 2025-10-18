from ..models.place import Place 
from ..models.review import Review
from ..models.amenity import Amenity
from ..persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # === AMENITY METHODS ===
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity
    
    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)
        
    
    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()
    
    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        amenity.update(amenity_data)
        return amenity

    # === PLACE METHODS ===
    def create_place(self, place_data):
        """Create a new place with amenities"""
        place_data_clean = place_data.copy()
        if 'owner_id' in place_data_clean:
            place_data_clean['owner'] = place_data_clean['owner_id']
            del place_data_clean['owner_id']
    
        amenities_ids = place_data_clean.pop('amenities', [])
    
        place = Place(**place_data_clean)
        self.place_repo.add(place)

        for amenity_id in amenities_ids:
            amenity = self.get_amenity(amenity_id)
            if amenity:
                place.add_amenity(amenity)
    
        return place

    def get_place(self, place_id):
        """Get place by ID"""
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()
    
    def update_place(self, place_id, place_data):
        """Update a place"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        place.update(place_data)
        return place

    # === REVIEW METHODS ===
    def create_review(self, review_data):
        """Create a new review"""
        rating = review_data['rating']
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
            
        review = Review(**review_data)
        self.review_repo.add(review)
        return review
    
    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)
        
    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()
        
    def get_reviews_by_place(self, place_id):
        """Get reviews for a place"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        """Update a review"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        
        if 'rating' in review_data:
            rating = review_data['rating']
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5")
        
        review.update(review_data)
        return review
    
    def delete_review(self, review_id):
        """Delete a review"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)
        return True