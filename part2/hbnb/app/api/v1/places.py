from flask_restx import Namespace, Resource, fields


from ...services.facade import HBnBFacade
facade = HBnBFacade()

api = Namespace('places', description='Place operations')

# Define models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

"""TEST for users """
from ...models.user import User
if not facade.user_repo.get_all():  # Si pas de users
    test_user = User("Test", "User", "test@example.com")
    facade.user_repo.add(test_user)
    print(f"✅ User de test créé: {test_user.id}")


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201  
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": "Internal server error"}, 500
        

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places ], 200 

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place :
            return {"error": "Place not found "}, 404
        
        return place.to_dict(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        try:
            place_data = api.payload
            updated_place = facade.update_place(place_id, place_data)  # ⬅️ Retourne direct l'updated
            return updated_place.to_dict(), 200
        except ValueError as e:
            if "not found" in str(e).lower():
                return {"error": "Place not found"}, 404
            return {"error": str(e)}, 400