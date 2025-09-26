import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import LoginForm from './components/LoginForm';
import BookingForm from './components/BookingForm';

function Hotels({ user, setUser }) {
  const [hotels, setHotels] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [showBookingForm, setShowBookingForm] = useState(false);
  const [selectedHotel, setSelectedHotel] = useState(null);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchHotels();
  }, []);

  const fetchHotels = async () => {
    try {
      const response = await fetch('https://hotel-booking-app-1-99r9.onrender.com/api/hotels');
      const data = await response.json();
      setHotels(data.hotels);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const fetchRooms = async (hotelId) => {
    try {
      const response = await fetch(`https://hotel-booking-app-1-99r9.onrender.com/api/rooms?hotel_id=${hotelId}`);
      const data = await response.json();
      setRooms(data.rooms);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const openBookingForm = async (hotel) => {
    setSelectedHotel(hotel);
    await fetchRooms(hotel.id);
    setShowBookingForm(true);
  };

  const handleBooking = async (bookingData) => {
    const token = localStorage.getItem('token');
    
    try {
      const response = await fetch('https://hotel-booking-app-1-99r9.onrender.com/api/bookings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          hotel_id: selectedHotel.id,
          room_id: selectedRoom.id,
          ...bookingData
        })
      });
      
      if (response.ok) {
        alert('Booking successful!');
        setShowBookingForm(false);
      } else {
        alert('Booking failed');
      }
    } catch (error) {
      alert('Booking failed');
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    setUser(null);
    navigate('/login');
  };

  return (
    <div style={{ 
      minHeight: '100vh',
      backgroundImage: 'url("https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80")',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundAttachment: 'fixed',
      padding: '20px'
    }}>
      <nav style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px', padding: '15px', backgroundColor: 'rgba(255,255,255,0.9)', backdropFilter: 'blur(10px)', borderRadius: '8px' }}>
        <h1 style={{ color: '#333' }}>🏖️ Hotels</h1>
        <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
          <button onClick={() => navigate('/hotels')} style={{ padding: '8px 16px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Hotels</button>
          <button onClick={() => navigate('/bookings')} style={{ padding: '8px 16px', backgroundColor: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>My Bookings</button>
          <span style={{ color: '#333' }}>Welcome, {user?.name}!</span>
          <button onClick={handleLogout} style={{ padding: '8px 16px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Logout</button>
        </div>
      </nav>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
        {hotels.map(hotel => (
          <div key={hotel.id} style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '20px', backgroundColor: 'rgba(255,255,255,0.95)', backdropFilter: 'blur(5px)', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
            <img src={hotel.image} alt={hotel.name} style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: '4px', marginBottom: '15px' }} />
            <h3>{hotel.name}</h3>
            <p>📍 {hotel.location}</p>
            <p>{hotel.description}</p>
            <p>⭐ {hotel.rating}</p>
            <button onClick={() => openBookingForm(hotel)} style={{ width: '100%', padding: '12px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
              Book Now
            </button>
          </div>
        ))}
      </div>

      {showBookingForm && (
        <BookingForm
          selectedHotel={selectedHotel}
          rooms={rooms}
          selectedRoom={selectedRoom}
          setSelectedRoom={setSelectedRoom}
          onSubmit={handleBooking}
          onCancel={() => setShowBookingForm(false)}
        />
      )}
    </div>
  );
}

function Bookings({ user, setUser }) {
  const [bookings, setBookings] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    const token = localStorage.getItem('token');
    try {
      const response = await fetch('https://hotel-booking-app-1-99r9.onrender.com/api/bookings', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setBookings(data.bookings);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const cancelBooking = async (bookingId) => {
    if (!window.confirm('Cancel this booking?')) return;
    
    const token = localStorage.getItem('token');
    try {
      const response = await fetch(`https://hotel-booking-app-1-99r9.onrender.com/api/bookings/${bookingId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        alert('Booking cancelled!');
        fetchBookings();
      }
    } catch (error) {
      alert('Cancel failed');
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    setUser(null);
    navigate('/login');
  };

  return (
    <div style={{ 
      minHeight: '100vh',
      backgroundImage: 'url("https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80")',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundAttachment: 'fixed',
      padding: '20px'
    }}>
      <nav style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px', padding: '15px', backgroundColor: 'rgba(255,255,255,0.9)', backdropFilter: 'blur(10px)', borderRadius: '8px' }}>
        <h1 style={{ color: '#333' }}>🏖️ My Bookings</h1>
        <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
          <button onClick={() => navigate('/hotels')} style={{ padding: '8px 16px', backgroundColor: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Hotels</button>
          <button onClick={() => navigate('/bookings')} style={{ padding: '8px 16px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>My Bookings</button>
          <span style={{ color: '#333' }}>Welcome, {user?.name}!</span>
          <button onClick={handleLogout} style={{ padding: '8px 16px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Logout</button>
        </div>
      </nav>

      {bookings.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px', backgroundColor: 'rgba(255,255,255,0.9)', backdropFilter: 'blur(10px)', borderRadius: '8px' }}>
          <p>No bookings yet. Book your first hotel!</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          {bookings.map(booking => (
            <div key={booking.id} style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '20px', backgroundColor: 'rgba(255,255,255,0.95)', backdropFilter: 'blur(5px)' }}>
              <h3>{booking.hotel_name}</h3>
              <p><strong>Room:</strong> {booking.room_type}</p>
              <p><strong>Check-in:</strong> {booking.check_in}</p>
              <p><strong>Check-out:</strong> {booking.check_out}</p>
              <p><strong>Guests:</strong> {booking.guests}</p>
              <p><strong>Total:</strong> ${booking.total_price}</p>
              <p><strong>Status:</strong> {booking.status}</p>
              <button onClick={() => cancelBooking(booking.id)} style={{ padding: '8px 16px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                Cancel Booking
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function App() {
  const [user, setUser] = useState(null);
  const [logoutKey, setLogoutKey] = useState(0);

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleSetUser = (userData) => {
    setUser(userData);
    setLogoutKey(prev => prev + 1);
  };

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginForm key={logoutKey} setUser={handleSetUser} />} />
        <Route path="/hotels" element={user ? <Hotels user={user} setUser={setUser} /> : <Navigate to="/login" />} />
        <Route path="/bookings" element={user ? <Bookings user={user} setUser={setUser} /> : <Navigate to="/login" />} />
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;