from models import db, User
from server import app

with app.app_context():
    users = User.query.all()
    print("=== USERS IN DATABASE ===")
    for user in users:
        print(f"Email: {user.email}")
        print(f"Password: {user.password}")
        print(f"Name: {user.name}")
        print("---")
    
    if not users:
        print("No users found! Creating test user...")
        test_user = User(name='Test User', email='test', password='123')
        db.session.add(test_user)
        db.session.commit()
        print("Created user: test / 123")