from models import db, User, Hotel, Booking
from server import app

with app.app_context():
    # Get a user
    user = User.query.first()
    print(f"Testing with user: {user.name} (ID: {user.id})")
    
    # Create a test hotel
    hotel = Hotel(
        id=1,
        name='Test Hotel',
        location='Test City',
        description='Test Description',
        rating=4.5,
        image='test.jpg'
    )
    db.session.add(hotel)
    
    # Create a test booking
    booking = Booking(
        user_id=user.id,
        hotel_id=1,
        room_type='Deluxe Suite',
        check_in='2024-01-01',
        check_out='2024-01-02',
        guests=2,
        total_price=200.0
    )
    db.session.add(booking)
    
    try:
        db.session.commit()
        print("✅ Test booking created successfully!")
        print(f"Hotel: {hotel.name}")
        print(f"Booking: {booking.room_type} for {booking.guests} guests")
    except Exception as e:
        print(f"❌ Error creating booking: {e}")
        db.session.rollback()