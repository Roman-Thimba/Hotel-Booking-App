import requests
import json

# Test login with new user
login_data = {
    "email": "newuser@test.com",
    "password": "password123"
}

try:
    response = requests.post('http://localhost:8000/api/login', 
                           json=login_data,
                           headers={'Content-Type': 'application/json'})
    
    if response.status_code == 200:
        print("✅ Login successful!")
        data = response.json()
        print(f"User: {data['user']['name']} ({data['user']['email']})")
        print(f"Token received: {data['token'][:20]}...")
    else:
        print(f"❌ Login failed: {response.json()}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("Make sure Flask server is running on port 8000")