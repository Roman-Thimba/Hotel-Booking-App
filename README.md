# Hotel Booking Application

A full-stack hotel booking application with React frontend and Flask backend, deployed on modern cloud platforms.

## 🌟 Features

- 🏖️ Beautiful beach hotel theme with background images
- 👤 User authentication with JWT tokens
- 🏨 Browse 20 luxury hotels worldwide
- 🛏️ Multiple suite options for each hotel
- 📅 Create and manage bookings (protected routes)
- 📱 Fully responsive design
- 🔄 Real-time data persistence

##  Live Demo

- **Frontend**: [Hotel Booking App](https://your-vercel-url.vercel.app)
- **Backend API**: [https://hotel-booking-app-1-99r9.onrender.com](https://hotel-booking-app-1-99r9.onrender.com)

## 📋 API Endpoints

### Authentication
- `POST /api/login` - User login

### Hotels & Rooms
- `GET /api/hotels` - Get all hotels
- `GET /api/rooms` - Get rooms by hotel

### Bookings (Protected)
- `GET /api/bookings` - Get user bookings
- `POST /api/bookings` - Create new booking
- `PATCH /api/bookings/<id>` - Update booking
- `DELETE /api/bookings/<id>` - Cancel booking

### User Management (Protected)
- `PATCH /api/users/<id>` - Update user profile
- `DELETE /api/users/<id>` - Delete user account

##  Featured Hotels

20 world-class luxury hotels including:
- Burj Al Arab (Dubai)
- The Ritz Paris (France)
- Marina Bay Sands (Singapore)
- The Plaza (New York)
- Atlantis The Palm (Dubai)
- And 15 more premium destinations

##  Tech Stack

### Frontend
- **React 18** - UI framework
- **React Router** - Client-side routing
- **Formik + Yup** - Form handling and validation
- **CSS-in-JS** - Styling

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - ORM and database management
- **JWT** - Authentication tokens
- **Flask-CORS** - Cross-origin requests
- **SQLite** - Database

### Deployment
- **Frontend**: Vercel
- **Backend**: Render
- **Database**: SQLite (persistent)

##  Local Development

### Prerequisites
- Node.js 16+
- Python 3.9+
- Git

### Setup

1. **Clone repository**
   ```bash
   git clone https://github.com/barakasamuel/HOTEL-BOOKING-APP.git
   cd HOTEL-BOOKING-APP
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Install backend dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run backend server**
   ```bash
   python server.py
   ```

5. **Run frontend (new terminal)**
   ```bash
   npm start
   ```

6. **Open application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

##  Demo Credentials

Use any valid email format with any password:
- Email: `test@example.com`
- Password: `password123`

##  Usage

1. **Login** with any email/password combination
2. **Browse Hotels** - View 20 luxury hotels with ratings and descriptions
3. **Select Suites** - Choose from multiple room types per hotel
4. **Make Bookings** - Fill out booking form with dates and guest count
5. **Manage Bookings** - View and cancel your reservations

##  Architecture

```
Frontend (Vercel)     Backend (Render)      Database
     React      ←→      Flask API      ←→    SQLite
   Components           Routes               Models
   Formik Forms         JWT Auth             Users
   React Router         CORS                 Hotels
                                            Bookings
```

##  Database Schema

### Users
- id, name, email, password, created_at

### Hotels
- id, name, location, description, rating, image

### Bookings
- id, user_id, hotel_id, room_type, check_in, check_out, guests, total_price, status, created_at

## Security Features

- JWT token authentication
- Protected API routes
- Input validation with Yup
- CORS configuration
- SQL injection prevention with SQLAlchemy

## Performance

- **Frontend**: Static site deployment on Vercel CDN
- **Backend**: Serverless deployment on Render
- **Database**: Optimized SQLite with proper indexing
- **Images**: Optimized Unsplash CDN images

##  Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

##  License

This project is licensed under the MIT License.

##  Authors

**.Baraka Samuel**

**.Roman Thimba**
- GitHub: [@barakasamuel](https://github.com/barakasamuel)
- Github: [@Roman-Thimba](https://github.com/Roman-Thimba)
- Project: [Hotel Booking App](https://github.com/barakasamuel/HOTEL-BOOKING-APP)

##  Acknowledgments

- Unsplash for beautiful hotel images
- Render for backend hosting
- Vercel for frontend deployment
- React community for excellent documentation
