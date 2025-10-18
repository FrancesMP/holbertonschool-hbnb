from flask import Flask
from flask_restx import Api, Resource

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Import and register API namespaces
    from .api.v1.amenities import api as amenities_ns
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, and amenities will be added later
    @app.route('/')
    def index():
        return "Welcome to HBNB API "
    
    @api.route('/hello')
    class HelloResource(Resource):
        def get(self):
            return {"message": "Hello from HBNB API "}

    """Test Route"""
    @app.route('/api/v1/test-models')
    def test_models_route():
        from .models import User, Place, Review, Amenity
        
        """create data for testing with postman """
        user = User("Postman", "Test", "postman@test.com")
        place = Place("Test Villa", "Luxury villa", 300.0, 40.0, -70.0, user)
        review = Review(5, "Perfect for testing!")
        amenity = Amenity("Swimming Pool")
        
        place.add_review(review)
        place.add_amenity(amenity)
        
        return {
            "message": " All models work with Postman!",
            "user": user.to_dict(),
            "place": place.to_dict(),
            "review": review.to_dict(),
            "amenity": amenity.to_dict()
        }
    
    return app
    
    
    
