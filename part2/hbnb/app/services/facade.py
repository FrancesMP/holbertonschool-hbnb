from ..models.place import Place
from ..persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        pass

    def create_place(self, place_data):
        """Checking if owner exists """
        owner_id = place_data['owner_id']
        print(f"🔍 Recherche user avec ID: {owner_id}")  # DEBUG
    
        all_users = self.user_repo.get_all()
        print(f"📋 Users dans le repo: {[user.id for user in all_users]}")  # DEBUG
    
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner user does not exist")
    
    
        """Checking Amenities"""
        for amenity_id in place_data.get('amenities', []):
            if not self.amenity_repo.get(amenity_id):
                raise ValueError(f"Amenity {amenity_id} does not exist")
    
        """creating instance"""
        # CORRECTION : Préparer les données pour Place
        place_data_clean = place_data.copy()
        place_data_clean['owner'] = owner  # ← Ajouter l'objet owner
        del place_data_clean['owner_id']   # ← Supprimer l'ID
    
        place = Place(**place_data_clean)  # ← Utiliser place_data_clean, pas place_data
        """saving instance"""
        self.place_repo.add(place)
        return place
    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        """Get place From Repo """
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place
        

    def create_review(self, review_data):
         # Vérifier que l'user existe
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError("User does not exist")
    
        # Vérifier que le place existe  
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError("Place does not exist")
    
        # Vérifier le rating (1-5)
        rating = review_data['rating']
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
    
        # Créer la review
        from ..models.review import Review
        review = Review(**review_data)
    
        # Sauvegarder
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        return review
        

    def get_all_reviews(self):
        return self.review_repo.get_all()
        

    def get_reviews_by_place(self, place_id):
    # Placeholder for logic to retrieve all reviews for a specific place
        pass

    def update_review(self, review_id, review_data):
    # Placeholder for logic to update a review
        pass

    def delete_review(self, review_id):
    # Placeholder for logic to delete a review
        pass