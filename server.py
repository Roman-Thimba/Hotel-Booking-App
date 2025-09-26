from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from models import db, User, Hotel, Booking

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = "secret"

db.init_app(app)

# Static hotel data
hotels = [
    {'id': 1, 'name': 'Burj Al Arab', 'location': 'Dubai, UAE', 'description': 'Luxury sail-shaped hotel', 'rating': 4.9, 'image': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400&h=300&fit=crop'},
    {'id': 2, 'name': 'The Ritz Paris', 'location': 'Paris, France', 'description': 'Legendary palace hotel', 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=400&h=300&fit=crop'},
    {'id': 3, 'name': 'Marina Bay Sands', 'location': 'Singapore', 'description': 'Architectural marvel', 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400&h=300&fit=crop'},
    {'id': 4, 'name': 'The Plaza', 'location': 'New York, USA', 'description': 'Iconic luxury hotel', 'rating': 4.6, 'image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400&h=300&fit=crop'},
    {'id': 5, 'name': 'Atlantis The Palm', 'location': 'Dubai, UAE', 'description': 'Ocean-themed resort', 'rating': 4.5, 'image': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop'},
    {'id': 6, 'name': 'The Savoy', 'location': 'London, UK', 'description': 'Historic luxury hotel', 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&h=300&fit=crop'},
    {'id': 7, 'name': 'Four Seasons George V', 'location': 'Paris, France', 'description': 'Art Deco masterpiece', 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400&h=300&fit=crop'},
    {'id': 8, 'name': 'The St. Regis Bora Bora', 'location': 'Bora Bora, French Polynesia', 'description': 'Overwater villa paradise', 'rating': 4.9, 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=300&fit=crop'},
    {'id': 9, 'name': 'Aman Tokyo', 'location': 'Tokyo, Japan', 'description': 'Urban sanctuary', 'rating': 4.6, 'image': 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&h=300&fit=crop'},
    {'id': 10, 'name': 'The Gritti Palace', 'location': 'Venice, Italy', 'description': 'Venetian palace hotel', 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?w=400&h=300&fit=crop'},
    {'id': 11, 'name': 'Mandarin Oriental Bangkok', 'location': 'Bangkok, Thailand', 'description': 'Riverside luxury', 'rating': 4.5, 'image': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400&h=300&fit=crop'},
    {'id': 12, 'name': 'The Peninsula Hong Kong', 'location': 'Hong Kong', 'description': 'Grande dame of the Far East', 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=400&h=300&fit=crop'},
    {'id': 13, 'name': 'Hotel del Coronado', 'location': 'San Diego, USA', 'description': 'Victorian beach resort', 'rating': 4.4, 'image': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400&h=300&fit=crop'},
    {'id': 14, 'name': 'Raffles Singapore', 'location': 'Singapore', 'description': 'Colonial grandeur', 'rating': 4.6, 'image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&h=300&fit=crop'},
    {'id': 15, 'name': 'The Oberoi Udaivilas', 'location': 'Udaipur, India', 'description': 'Palace on Lake Pichola', 'rating': 4.9, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop'},
    {'id': 16, 'name': 'Belmond Hotel Caruso', 'location': 'Amalfi Coast, Italy', 'description': 'Clifftop paradise', 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop'},
    {'id': 17, 'name': 'The Langham London', 'location': 'London, UK', 'description': 'Europe\'s first grand hotel', 'rating': 4.5, 'image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&h=300&fit=crop'},
    {'id': 18, 'name': 'Park Hyatt Sydney', 'location': 'Sydney, Australia', 'description': 'Harbour views', 'rating': 4.6, 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop'},
    {'id': 19, 'name': 'The Brando', 'location': 'Tetiaroa, French Polynesia', 'description': 'Eco-luxury resort', 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=300&fit=crop'},
    {'id': 20, 'name': 'Singita Sasakwa Lodge', 'location': 'Serengeti, Tanzania', 'description': 'Safari luxury', 'rating': 4.9, 'image': 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=400&h=300&fit=crop'}
]

rooms = [
    # Hotel 1 - Burj Al Arab
    {'id': 1, 'hotel_id': 1, 'type': 'Deluxe Suite', 'capacity': 2, 'price_per_night': 1200, 'amenities': ['Ocean View', 'King Bed']},
    {'id': 2, 'hotel_id': 1, 'type': 'Royal Suite', 'capacity': 4, 'price_per_night': 2500, 'amenities': ['Private Elevator', 'Butler']},
    # Hotel 2 - The Ritz Paris
    {'id': 3, 'hotel_id': 2, 'type': 'Classic Suite', 'capacity': 2, 'price_per_night': 950, 'amenities': ['City View', 'Mini Bar']},
    {'id': 4, 'hotel_id': 2, 'type': 'Imperial Suite', 'capacity': 4, 'price_per_night': 2800, 'amenities': ['Terrace', 'Piano']},
    # Hotel 3 - Marina Bay Sands
    {'id': 5, 'hotel_id': 3, 'type': 'Deluxe Suite', 'capacity': 2, 'price_per_night': 650, 'amenities': ['Pool Access', 'WiFi']},
    {'id': 6, 'hotel_id': 3, 'type': 'Skypark Suite', 'capacity': 4, 'price_per_night': 1500, 'amenities': ['Skypark Access', 'Butler']},
    # Hotel 4 - The Plaza
    {'id': 7, 'hotel_id': 4, 'type': 'Plaza Suite', 'capacity': 2, 'price_per_night': 800, 'amenities': ['Central Park View', 'Marble Bath']},
    {'id': 8, 'hotel_id': 4, 'type': 'Presidential Suite', 'capacity': 6, 'price_per_night': 3500, 'amenities': ['Private Terrace', 'Butler Service']},
    # Hotel 5 - Atlantis The Palm
    {'id': 9, 'hotel_id': 5, 'type': 'Neptune Suite', 'capacity': 2, 'price_per_night': 900, 'amenities': ['Aquarium View', 'Ocean Access']},
    {'id': 10, 'hotel_id': 5, 'type': 'Poseidon Suite', 'capacity': 4, 'price_per_night': 2200, 'amenities': ['Underwater Suite', 'Private Pool']},
    # Hotel 6 - The Savoy
    {'id': 11, 'hotel_id': 6, 'type': 'Thames Suite', 'capacity': 2, 'price_per_night': 750, 'amenities': ['River View', 'Art Deco']},
    {'id': 12, 'hotel_id': 6, 'type': 'Royal Suite', 'capacity': 4, 'price_per_night': 2000, 'amenities': ['Private Dining', 'Butler']},
    # Hotel 7 - Four Seasons George V
    {'id': 13, 'hotel_id': 7, 'type': 'Parisian Suite', 'capacity': 2, 'price_per_night': 1100, 'amenities': ['Courtyard View', 'Marble Bath']},
    {'id': 14, 'hotel_id': 7, 'type': 'Presidential Suite', 'capacity': 6, 'price_per_night': 4000, 'amenities': ['Private Terrace', 'Grand Piano']},
    # Hotel 8 - The St. Regis Bora Bora
    {'id': 15, 'hotel_id': 8, 'type': 'Overwater Suite', 'capacity': 2, 'price_per_night': 1800, 'amenities': ['Glass Floor', 'Private Deck']},
    {'id': 16, 'hotel_id': 8, 'type': 'Royal Overwater Suite', 'capacity': 4, 'price_per_night': 3200, 'amenities': ['Private Beach', 'Butler']},
    # Hotel 9 - Aman Tokyo
    {'id': 17, 'hotel_id': 9, 'type': 'Deluxe Suite', 'capacity': 2, 'price_per_night': 900, 'amenities': ['City View', 'Japanese Bath']},
    {'id': 18, 'hotel_id': 9, 'type': 'Aman Suite', 'capacity': 4, 'price_per_night': 2500, 'amenities': ['Garden View', 'Private Onsen']},
    # Hotel 10 - The Gritti Palace
    {'id': 19, 'hotel_id': 10, 'type': 'Canal Suite', 'capacity': 2, 'price_per_night': 850, 'amenities': ['Grand Canal View', 'Venetian Decor']},
    {'id': 20, 'hotel_id': 10, 'type': 'Doge Suite', 'capacity': 4, 'price_per_night': 2300, 'amenities': ['Terrace', 'Antique Furnishings']},
    # Hotel 11 - Mandarin Oriental Bangkok
    {'id': 21, 'hotel_id': 11, 'type': 'River Suite', 'capacity': 2, 'price_per_night': 600, 'amenities': ['River View', 'Thai Decor']},
    {'id': 22, 'hotel_id': 11, 'type': 'Oriental Suite', 'capacity': 4, 'price_per_night': 1400, 'amenities': ['Private Balcony', 'Butler']},
    # Hotel 12 - The Peninsula Hong Kong
    {'id': 23, 'hotel_id': 12, 'type': 'Harbour Suite', 'capacity': 2, 'price_per_night': 700, 'amenities': ['Harbour View', 'Marble Bath']},
    {'id': 24, 'hotel_id': 12, 'type': 'Peninsula Suite', 'capacity': 4, 'price_per_night': 1800, 'amenities': ['Private Terrace', 'Butler Service']},
    # Hotel 13 - Hotel del Coronado
    {'id': 25, 'hotel_id': 13, 'type': 'Ocean Suite', 'capacity': 2, 'price_per_night': 500, 'amenities': ['Beach View', 'Victorian Charm']},
    {'id': 26, 'hotel_id': 13, 'type': 'Presidential Suite', 'capacity': 6, 'price_per_night': 1200, 'amenities': ['Private Beach Access', 'Historic Decor']},
    # Hotel 14 - Raffles Singapore
    {'id': 27, 'hotel_id': 14, 'type': 'Colonial Suite', 'capacity': 2, 'price_per_night': 650, 'amenities': ['Garden View', 'Colonial Decor']},
    {'id': 28, 'hotel_id': 14, 'type': 'Presidential Suite', 'capacity': 4, 'price_per_night': 1600, 'amenities': ['Private Verandah', 'Butler']},
    # Hotel 15 - The Oberoi Udaivilas
    {'id': 29, 'hotel_id': 15, 'type': 'Lake Suite', 'capacity': 2, 'price_per_night': 800, 'amenities': ['Lake View', 'Private Courtyard']},
    {'id': 30, 'hotel_id': 15, 'type': 'Maharaja Suite', 'capacity': 4, 'price_per_night': 2000, 'amenities': ['Palace View', 'Private Pool']},
    # Hotel 16 - Belmond Hotel Caruso
    {'id': 31, 'hotel_id': 16, 'type': 'Sea View Suite', 'capacity': 2, 'price_per_night': 900, 'amenities': ['Mediterranean View', 'Private Terrace']},
    {'id': 32, 'hotel_id': 16, 'type': 'Belmond Suite', 'capacity': 4, 'price_per_night': 2200, 'amenities': ['Infinity Pool', 'Butler Service']},
    # Hotel 17 - The Langham London
    {'id': 33, 'hotel_id': 17, 'type': 'Regent Suite', 'capacity': 2, 'price_per_night': 700, 'amenities': ['Park View', 'Victorian Elegance']},
    {'id': 34, 'hotel_id': 17, 'type': 'Sterling Suite', 'capacity': 4, 'price_per_night': 1700, 'amenities': ['Private Dining', 'Butler']},
    # Hotel 18 - Park Hyatt Sydney
    {'id': 35, 'hotel_id': 18, 'type': 'Harbour Suite', 'capacity': 2, 'price_per_night': 750, 'amenities': ['Opera House View', 'Private Balcony']},
    {'id': 36, 'hotel_id': 18, 'type': 'Sydney Suite', 'capacity': 4, 'price_per_night': 1900, 'amenities': ['Harbour Bridge View', 'Butler']},
    # Hotel 19 - The Brando
    {'id': 37, 'hotel_id': 19, 'type': 'Beach Villa Suite', 'capacity': 2, 'price_per_night': 2000, 'amenities': ['Private Beach', 'Eco Luxury']},
    {'id': 38, 'hotel_id': 19, 'type': 'Presidential Villa Suite', 'capacity': 6, 'price_per_night': 4500, 'amenities': ['Private Island', 'Butler Service']},
    # Hotel 20 - Singita Sasakwa Lodge
    {'id': 39, 'hotel_id': 20, 'type': 'Safari Suite', 'capacity': 2, 'price_per_night': 1500, 'amenities': ['Serengeti View', 'Private Deck']},
    {'id': 40, 'hotel_id': 20, 'type': 'Presidential Safari Suite', 'capacity': 4, 'price_per_night': 3000, 'amenities': ['Infinity Pool', 'Game Viewing Deck']}
]

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except:
        return None

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Accept any valid email format with any password
    if '@' in email and '.' in email:
        # Create or get user
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(name=email.split('@')[0].title(), email=email, password=password)
            db.session.add(user)
            db.session.commit()
        
        token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=24)}, SECRET_KEY)
        return jsonify({'token': token, 'user': user.to_dict()}), 200
    
    return jsonify({'error': 'Invalid email format'}), 401

@app.route('/api/hotels', methods=['GET'])
def get_hotels():
    return jsonify({'hotels': hotels}), 200

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    hotel_id = request.args.get('hotel_id')
    if hotel_id:
        filtered_rooms = [room for room in rooms if room['hotel_id'] == int(hotel_id)]
        return jsonify({'rooms': filtered_rooms}), 200
    return jsonify({'rooms': rooms}), 200

@app.route('/api/bookings', methods=['GET', 'POST'])
def handle_bookings():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Token required'}), 401
    
    token = auth_header.split(' ')[1]
    user_id = verify_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    
    if request.method == 'GET':
        bookings = Booking.query.filter_by(user_id=user_id).all()
        return jsonify({'bookings': [booking.to_dict() for booking in bookings]}), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        
        try:
            # Save hotel to database if not exists
            hotel_data = next((h for h in hotels if h['id'] == data.get('hotel_id')), None)
            if hotel_data and not Hotel.query.filter_by(id=data.get('hotel_id')).first():
                hotel = Hotel(**hotel_data)
                db.session.add(hotel)
                db.session.flush()
            
            # Get room type
            room_id = int(data.get('room_id')) if data.get('room_id') else None
            room_data = next((r for r in rooms if r['id'] == room_id), None)
            room_type = room_data['type'] if room_data else 'Standard Room'
            
            # Create booking
            booking = Booking(
                user_id=user_id,
                hotel_id=data.get('hotel_id'),
                room_type=room_type,
                check_in=data.get('check_in'),
                check_out=data.get('check_out'),
                guests=data.get('guests'),
                total_price=data.get('total_price')
            )
            
            db.session.add(booking)
            db.session.commit()
            
            return jsonify({'booking': booking.to_dict(), 'message': 'Booking successful'}), 201
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@app.route('/api/bookings/<int:booking_id>', methods=['PATCH', 'DELETE'])
def modify_booking(booking_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Token required'}), 401
    
    token = auth_header.split(' ')[1]
    user_id = verify_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    
    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if request.method == 'PATCH':
        data = request.get_json()
        if 'status' in data:
            booking.status = data['status']
        db.session.commit()
        return jsonify({'booking': booking.to_dict()}), 200
    
    elif request.method == 'DELETE':
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'Booking cancelled'}), 200

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Create test user
        user = User(name='User', email='user@test.com', password='123')
        db.session.add(user)
        db.session.commit()

@app.route('/api/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Token required'}), 401
    
    token = auth_header.split(' ')[1]
    token_user_id = verify_token(token)
    if not token_user_id or token_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    
    db.session.commit()
    return jsonify({'user': user.to_dict()}), 200

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Token required'}), 401
    
    token = auth_header.split(' ')[1]
    token_user_id = verify_token(token)
    if not token_user_id or token_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

@app.route('/api/db-status', methods=['GET'])
def db_status():
    users = User.query.all()
    hotels = Hotel.query.all()
    bookings = Booking.query.all()
    
    return jsonify({
        'users': [{'id': u.id, 'name': u.name, 'email': u.email} for u in users],
        'hotels': [h.to_dict() for h in hotels],
        'bookings': [b.to_dict() for b in bookings]
    }), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8000)