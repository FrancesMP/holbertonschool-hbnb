from flask_restx import Namespace, Resource, fields
from ...services.facade import HBnBFacade
from ...models.place import Place
from ...models.user import User

# Create namespace for places
api = Namespace('places', description='Place operations')

# Connect to business logic
facade = HBnBFacade()

# Define the data structure for places
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(required=True, description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='Owner user ID')
})

# Handle /api/v1/places/ (create and list)
@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    def post(self):
        """Create a new place"""
        data = api.payload
        
        try:
            # Find the owner user
            owner = facade.user_repo.get(data['owner_id'])
            if not owner:
                return {'error': 'Owner not found'}, 400
            
            # Create place
            place = Place(
                title=data['title'],
                description=data['description'],
                price=data['price'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                owner=owner
            )
            
            # Save to storage
            facade.place_repo.add(place)
            return place.to_dict(), 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
    
    def get(self):
        """Get all places"""
        places = facade.place_repo.get_all()
        return [place.to_dict() for place in places], 200

# Handle /api/v1/places/<place_id> (get one and update)
@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Get a specific place by ID"""
        place = facade.place_repo.get(place_id)
        if place:
            return place.to_dict(), 200
        return {'error': 'Place not found'}, 404
    
    @api.expect(place_model)
    def put(self, place_id):
        """Update a place"""
        data = api.payload
        place = facade.place_repo.get(place_id)
        
        if not place:
            return {'error': 'Place not found'}, 404
            
        try:
            # If owner_id is provided, find the new owner
            if 'owner_id' in data:
                owner = facade.user_repo.get(data['owner_id'])
                if not owner:
                    return {'error': 'Owner not found'}, 400
                data['owner'] = owner
                del data['owner_id']  # Remove owner_id since Place uses owner object
            
            place.update(data)
            return place.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
