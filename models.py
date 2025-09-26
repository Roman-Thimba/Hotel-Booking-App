from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    bookings = db.relationship('Booking', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

class Hotel(db.Model):
    __tablename__ = 'hotels'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)
    image = db.Column(db.String(500))
    
    bookings = db.relationship('Booking', backref='hotel', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'rating': self.rating,
            'image': self.image
        }

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False)
    room_type = db.Column(db.String(100), nullable=False)
    check_in = db.Column(db.String(50), nullable=False)
    check_out = db.Column(db.String(50), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='confirmed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'hotel_id': self.hotel_id,
            'room_type': self.room_type,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'guests': self.guests,
            'total_price': self.total_price,
            'status': self.status,
            'hotel_name': self.hotel.name if self.hotel else 'Unknown'
        }