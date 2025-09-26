import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { useNavigate } from 'react-router-dom';

const LoginSchema = Yup.object().shape({
  email: Yup.string().email('Invalid email').required('Email required'),
  password: Yup.string().min(3, 'Min 3 characters').required('Password required')
});

const LoginForm = ({ setUser }) => {
  const navigate = useNavigate();

  const handleSubmit = async (values, { setSubmitting, setFieldError }) => {
    try {
      const response = await fetch('https://hotel-booking-app-1-99r9.onrender.com/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      });
      const data = await response.json();
      
      if (response.ok) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        setUser(data.user);
        navigate('/hotels');
      } else {
        setFieldError('password', data.error);
      }
    } catch (error) {
      setFieldError('password', 'Login failed');
    }
    setSubmitting(false);
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f0f2f5' }}>
      <div style={{ backgroundColor: 'white', padding: '40px', borderRadius: '8px', width: '400px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
        <h1 style={{ textAlign: 'center', marginBottom: '30px' }}>🏖️ Hotel Booking</h1>
        
        <Formik initialValues={{ email: '', password: '' }} validationSchema={LoginSchema} onSubmit={handleSubmit}>
          {({ isSubmitting }) => (
            <Form>
              <Field name="email" placeholder="Email" style={{ width: '100%', padding: '12px', marginBottom: '5px', border: '1px solid #ddd', borderRadius: '4px', boxSizing: 'border-box' }} />
              <ErrorMessage name="email" component="div" style={{ color: 'red', fontSize: '0.8rem', marginBottom: '15px' }} />
              
              <Field type="password" name="password" placeholder="Password" style={{ width: '100%', padding: '12px', marginBottom: '5px', border: '1px solid #ddd', borderRadius: '4px', boxSizing: 'border-box' }} />
              <ErrorMessage name="password" component="div" style={{ color: 'red', fontSize: '0.8rem', marginBottom: '20px' }} />
              
              <button type="submit" disabled={isSubmitting} style={{ width: '100%', padding: '12px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                {isSubmitting ? 'Logging in...' : 'Login'}
              </button>
            </Form>
          )}
        </Formik>
        
        <p style={{ textAlign: 'center', marginTop: '20px', color: '#666' }}>
          Use any email format (e.g., test@example.com) with any password
        </p>
      </div>
    </div>
  );
};

export default LoginForm;