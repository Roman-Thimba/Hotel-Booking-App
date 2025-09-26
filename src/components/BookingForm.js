import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const BookingSchema = Yup.object().shape({
  room_id: Yup.number().required('Please select a room'),
  check_in: Yup.date().min(new Date(), 'Check-in must be future date').required('Check-in required'),
  check_in_time: Yup.string(),
  check_out: Yup.date().min(Yup.ref('check_in'), 'Check-out must be after check-in').required('Check-out required'),
  check_out_time: Yup.string(),
  guests: Yup.number().min(1, 'Min 1 guest').max(10, 'Max 10 guests').required('Guests required')
});

const BookingForm = ({ selectedHotel, rooms, selectedRoom, setSelectedRoom, onSubmit, onCancel }) => {
  const handleSubmit = async (values, { setSubmitting }) => {
    const bookingData = {
      ...values,
      total_price: selectedRoom ? selectedRoom.price_per_night * values.guests : 0
    };
    await onSubmit(bookingData);
    setSubmitting(false);
  };

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
      <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '8px', width: '400px' }}>
        <h2 style={{ margin: '0 0 20px 0' }}>Book {selectedHotel?.name}</h2>
        
        <Formik
          initialValues={{ room_id: selectedRoom?.id || '', check_in: '', check_in_time: '', check_out: '', check_out_time: '', guests: 1 }}
          validationSchema={BookingSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting, setFieldValue }) => (
            <Form>
              <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#333' }}>Select Room *</label>
              <Field as="select" name="room_id" style={{ width: '100%', padding: '12px', marginBottom: '5px', border: '1px solid #ddd', borderRadius: '4px', boxSizing: 'border-box' }}
                onChange={(e) => {
                  const room = rooms.find(r => r.id === parseInt(e.target.value));
                  setSelectedRoom(room);
                  setFieldValue('room_id', e.target.value);
                }}>
                <option value="">Select room...</option>
                {rooms.map(room => (
                  <option key={room.id} value={room.id}>
                    {room.type} - ${room.price_per_night}/night
                  </option>
                ))}
              </Field>
              <ErrorMessage name="room_id" component="div" style={{ color: 'red', fontSize: '0.8rem', marginBottom: '15px' }} />
              
              <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#333' }}>Check-in Date *</label>
              <Field type="date" name="check_in" style={{ width: '100%', padding: '12px', marginBottom: '5px', border: '1px solid #ddd', borderRadius: '4px', boxSizing: 'border-box' }} />
              <ErrorMessage name="check_in" component="div" style={{ color: 'red', fontSize: '0.8rem', marginBottom: '5px' }} />
              
              <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#333' }}>Check-in Time (optional)</label>
              <Field type="time" name="check_in_time" style={{ width: '100%', padding: '12px', marginBottom: '15px', border: '1px solid #ddd', borderRadius: '4px', boxSizing: 'border-box' }} />
              
              <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#333' }}>Check-out Date *</label>
              <Field type="date" name="check_out" style={{ width: '100%', padding: '12px', marginBottom: '5px', border: '1px solid #ddd', borderRadius: '4px', boxSizing: 'border-box' }} />
              <ErrorMessage name="check_out" component="div" style={{ color: 'red', fontSize: '0.8rem', marginBottom: '5px' }} />
              
              <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#333' }}>Check-out Time (optional)</label>
              <Field type="time" name="check_out_time" style={{ width: '100%', padding: '12px', marginBottom: '15px', border: '1px solid #ddd', borderRadius: '4px', boxSizing: 'border-box' }} />
              
              <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', color: '#333' }}>Number of Guests *</label>
              <Field type="number" name="guests" min="1" max="10" style={{ width: '100%', padding: '12px', marginBottom: '5px', border: '1px solid #ddd', borderRadius: '4px', boxSizing: 'border-box' }} />
              <ErrorMessage name="guests" component="div" style={{ color: 'red', fontSize: '0.8rem', marginBottom: '20px' }} />
              
              <div style={{ display: 'flex', gap: '10px' }}>
                <button type="submit" disabled={isSubmitting} style={{ flex: 1, padding: '12px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                  {isSubmitting ? 'Booking...' : 'Book Now'}
                </button>
                <button type="button" onClick={onCancel} style={{ flex: 1, padding: '12px', backgroundColor: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                  Cancel
                </button>
              </div>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
};

export default BookingForm;