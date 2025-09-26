import os
from models import db, User, Hotel, Booking
from server import app

print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
print(f"Database file exists: {os.path.exists('instance/hotel.db')}")

with app.app_context():
    print("=== DATABASE CONTENTS ===")
    print(f"Users: {User.query.count()}")
    print(f"Hotels: {Hotel.query.count()}")
    print(f"Bookings: {Booking.query.count()}")
    
    print("\n=== USERS ===")
    for user in User.query.all():
        print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
    
    print("\n=== HOTELS ===")
    for hotel in Hotel.query.all():
        print(f"ID: {hotel.id}, Name: {hotel.name}")
    
    print("\n=== BOOKINGS ===")
    for booking in Booking.query.all():
        print(f"ID: {booking.id}, User: {booking.user_id}, Hotel: {booking.hotel_id}, Room: {booking.room_type}")