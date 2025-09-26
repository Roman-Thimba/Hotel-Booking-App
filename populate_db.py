from models import db, User, Hotel, Booking
from server import app

with app.app_context():
    # Clear existing data
    Booking.query.delete()
    Hotel.query.delete()
    User.query.delete()
    
    # Add users
    user1 = User(name='John Doe', email='john@example.com', password='password123')
    user2 = User(name='Jane Smith', email='jane@example.com', password='password456')
    user3 = User(name='Mike Johnson', email='mike@example.com', password='password789')
    
    db.session.add_all([user1, user2, user3])
    db.session.flush()
    
    # Add hotels
    hotel1 = Hotel(id=1, name='Burj Al Arab', location='Dubai, UAE', description='Luxury sail-shaped hotel', rating=4.9, image='https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400')
    hotel2 = Hotel(id=2, name='The Ritz Paris', location='Paris, France', description='Legendary palace hotel', rating=4.8, image='https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=400')
    hotel3 = Hotel(id=3, name='Marina Bay Sands', location='Singapore', description='Architectural marvel', rating=4.7, image='https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400')
    
    db.session.add_all([hotel1, hotel2, hotel3])
    db.session.flush()
    
    # Add bookings
    booking1 = Booking(user_id=user1.id, hotel_id=1, room_type='Deluxe Suite', check_in='2024-12-01', check_out='2024-12-05', guests=2, total_price=2400.0)
    booking2 = Booking(user_id=user2.id, hotel_id=2, room_type='Imperial Suite', check_in='2024-12-10', check_out='2024-12-15', guests=4, total_price=14000.0)
    booking3 = Booking(user_id=user3.id, hotel_id=3, room_type='Skypark Suite', check_in='2024-12-20', check_out='2024-12-25', guests=2, total_price=7500.0)
    booking4 = Booking(user_id=user1.id, hotel_id=3, room_type='Deluxe Room', check_in='2025-01-01', check_out='2025-01-03', guests=1, total_price=1300.0)
    
    db.session.add_all([booking1, booking2, booking3, booking4])
    
    # Commit all changes
    db.session.commit()
    
    print("✅ Database populated successfully!")
    print(f"Users: {User.query.count()}")
    print(f"Hotels: {Hotel.query.count()}")
    print(f"Bookings: {Booking.query.count()}")