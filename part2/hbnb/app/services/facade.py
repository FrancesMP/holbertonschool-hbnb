from ..models.place import Place 
from ..models.review import Review
from ..persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # === PLACE METHODS ===
    def create_place(self, place_data):
        
        # # """Create a new place"""
        # # owner_id = place_data['owner_id']
        # # owner = self.user_repo.get(owner_id)
        # # if not owner:
        # #     raise ValueError("Owner user does not exist")
    
        # # for amenity_id in place_data.get('amenities', []):
        # #     if not self.amenity_repo.get(amenity_id):
        # #         raise ValueError(f"Amenity {amenity_id} does not exist")
    
        # place_data_clean = place_data.copy()
        # # place_data_clean['owner'] = owner
        # # del place_data_clean['owner_id']
        # # del place_data_clean['amenities']
        
        # place = Place(**place_data_clean)
        # self.place_repo.add(place)
        # return place

        print("🔍 DEBUG 1: create_place appelé")
    
        try:
            place_data_clean = place_data.copy()
            if 'owner_id' in place_data_clean:
                place_data_clean['owner'] = place_data_clean['owner_id']
                del place_data_clean['owner_id']
        
        # ⬇️ ENLÈVE amenities car pas dans le constructeur
            place_data_clean.pop('amenities', None)
        
            print("🔍 DEBUG 3: place_data_clean =", place_data_clean)
        
            place = Place(**place_data_clean)
        # ⬇️ AJOUTE LES AMENITIES APRÈS si besoin
        # for amenity_id in place_data.get('amenities', []):
        #     place.add_amenity(amenity_id)
            
            self.place_repo.add(place)
            return place
        
        except Exception as e:
            print("❌ ERREUR:", e)
            import traceback
            print("❌ TRACEBACK:", traceback.format_exc())
            raise
        
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
        try:
           
            review_data_clean = review_data.copy()
           
            rating = review_data_clean['rating']
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5")
            
            review = Review(**review_data_clean)
            self.review_repo.add(review)
            return review
        except Exception as e:
            print("❌ Erreur create_review:", e)
            raise
    
    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)
        
    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()
        
    def get_reviews_by_place(self, place_id):
        """Get reviews for a place"""
        place = self.place_repo.get(place_id)  # ✅ CORRIGÉ
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