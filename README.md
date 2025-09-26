# Hotel Booking Application

A full-stack hotel booking application with React frontend and Flask backend, optimized for Vercel deployment.

## Features

- 🏖️ Beautiful beach hotel theme with background image
- 👤 User registration and login with JWT authentication
- 🏨 Browse available hotels
- 🛏️ View room details
- 📅 Create bookings (protected routes)
- 📱 Responsive design

## API Endpoints

- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/hotels` - Get all hotels
- `GET /api/rooms` - Get all rooms
- `GET /api/bookings` - Get user bookings (protected)
- `POST /api/bookings` - Create new booking (protected)

## Demo Credentials

- Email: demo@hotel.com
- Password: demo123

## Local Development

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run development server:
   ```bash
   npm run dev
   ```

3. Open http://localhost:3000

## Deployment to Vercel

1. Push to GitHub
2. Connect repository to Vercel
3. Deploy automatically

The app is configured to work perfectly with Vercel's serverless functions.

## Tech Stack

- **Frontend**: React, Next.js
- **Backend**: Flask (Vercel Functions)
- **Authentication**: JWT
- **Deployment**: Vercel