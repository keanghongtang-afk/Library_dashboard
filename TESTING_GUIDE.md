# Testing Guide & API Reference

## 🧪 Quick Testing Steps

### Prerequisites
1. Backend running on `http://localhost:8000`
2. Frontend running on `http://localhost:5173`
3. Database created with users table

---

## 📍 Setup: Create Test Accounts

### Option 1: Using SQLite CLI
```bash
# Open database
sqlite3 database/database.db

# Create admin user
INSERT INTO users (name, email, password, status, role) 
VALUES ('Admin User', 'admin@example.com', 'password123', 1, 'admin');

INSERT INTO devices (user_id, device_id) 
VALUES (1, 'admin-device-123');

# Create regular user
INSERT INTO users (name, email, password, status, role) 
VALUES ('Test User', 'user@example.com', 'password123', 1, 'user');

INSERT INTO devices (user_id, device_id) 
VALUES (2, 'user-device-123');

# Verify
SELECT * FROM users;
```

### Option 2: Using Python Script
```python
from app.db import session, User, Device

# Create admin
admin = User(
    name='Admin User',
    email='admin@example.com',
    password='password123',
    status=True,
    role='admin'
)
session.add(admin)
session.flush()

device1 = Device(user_id=admin.id, device_id='admin-device-123')
session.add(device1)

# Create regular user
user = User(
    name='Test User',
    email='user@example.com',
    password='password123',
    status=True,
    role='user'
)
session.add(user)
session.flush()

device2 = Device(user_id=user.id, device_id='user-device-123')
session.add(device2)

session.commit()
```

---

## 🧪 Test Scenario 1: Admin User Flow

### Step 1: Login as Admin
```bash
# Frontend: Navigate to http://localhost:5173/login

# Enter credentials:
Email:    admin@example.com
Password: password123

# Expected:
- OTP required (will be in terminal logs for testing)
- Redirect to OTP page
```

### Step 2: Verify Device with OTP
```
# Check backend terminal for OTP code
# (In verify_device logs or email if configured)

# Enter OTP in frontend
# Expected:
- Success message
- Redirect to /admin (automatic)
```

### Step 3: Admin Page Access
```
# URL: http://localhost:5173/admin

# Expected to see:
- Admin dashboard
- User info: "Admin User" (admin@example.com)
- Admin badge: "🔑 Admin"
- Logout button
```

### Step 4: Test Logout
```
# Click Logout button
# Expected:
- Session cleared
- Redirected to /login
- User cannot access /admin without relogin
```

---

## 🧪 Test Scenario 2: Regular User Flow

### Step 1: Signup as New User
```
# Navigate to: http://localhost:5173/signup

# Fill form:
Name:     John Doe
Email:    john@example.com
Password: test123

# Note: NO role selection (removed)
# Role automatically set to 'user'

# Expected:
- Success message
- Redirect to login
```

### Step 2: Login as New User
```
# Login with:
Email:    john@example.com
Password: test123

# Expected:
- OTP required
- Device verification
- Success
- Redirect to /books (not /admin)
```

### Step 3: Try to Access Admin Page
```
# Try to navigate to: http://localhost:5173/admin

# Expected:
- Immediately redirect to /books
- ProtectedAdminRoute blocks access
- No admin page visible
```

---

## 🧪 Test Scenario 3: Book Operations Protection

### Test Add Book (Non-Admin)
```javascript
// Frontend: Try to call add book with regular user logged in

const addBook = async () => {
  const response = await fetch('http://localhost:8000/books', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: 'Test Book',
      author: 'Test Author',
      genre: 'Fiction',
      stock: 5,
      user_email: 'user@example.com'  // Regular user
    })
  });
  
  const result = await response.json();
  console.log(result);
  // Expected: { error: "Admin access required" }
};
```

### Test Add Book (Admin)
```javascript
// Same request but with admin user

const addBook = async () => {
  const response = await fetch('http://localhost:8000/books', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: 'Test Book',
      author: 'Test Author',
      genre: 'Fiction',
      stock: 5,
      user_email: 'admin@example.com'  // Admin user
    })
  });
  
  const result = await response.json();
  console.log(result);
  // Expected: { message: "Successfully added..." } or similar
};
```

### Using cURL to Test
```bash
# Non-admin trying to add book
curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Book",
    "author": "Test Author",
    "genre": "Fiction",
    "stock": 5,
    "user_email": "user@example.com"
  }'
# Expected: {"error":"Admin access required"}

# Admin adding book
curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Book",
    "author": "Test Author",
    "genre": "Fiction",
    "stock": 5,
    "user_email": "admin@example.com"
  }'
# Expected: Success response
```

---

## 📡 API Endpoints Reference

### Authentication Endpoints

#### POST /login
```
Request:
{
  "email": "user@example.com",
  "password": "password123",
  "device_id": "device-fingerprint"
}

Response (Success - Same Device):
{
  "status": "success",
  "message": "Login Success!",
  "user": {
    "id": 1,
    "name": "User Name",
    "email": "user@example.com",
    "role": "user"
  }
}

Response (OTP Required - New Device):
{
  "status": "otp_required",
  "message": "A verification code has been sent to your email..."
}
```

#### POST /verify-device
```
Request:
{
  "email": "user@example.com",
  "otp": "123456"
}

Response:
{
  "status": "success",
  "message": "Device verified. Login Success.",
  "user": {
    "id": 1,
    "name": "User Name",
    "email": "user@example.com",
    "role": "user"
  }
}
```

#### POST /signin (Signup)
```
Request:
{
  "name": "New User",
  "email": "newuser@example.com",
  "password": "password123",
  "device_id": "device-fingerprint",
  "role": "user"  // Only "user" allowed
}

Response:
{
  "message": "Successfully signed up!"
}
```

#### POST /logout
```
Request (Form Data):
email: user@example.com
device_id: device-fingerprint

Response:
"Logout Success"
```

---

### Book Endpoints

#### GET /books
```
Request:
GET /books?limit=10

Response:
[
  {
    "id": 1,
    "title": "Book Title",
    "author": "Author Name",
    "genre": "Fiction",
    "stock": 5
  },
  ...
]
```

#### POST /books (Admin Only)
```
Request:
POST /books?user_email=admin@example.com
{
  "title": "New Book",
  "author": "Author Name",
  "genre": "Fiction",
  "stock": 10
}

Response (Admin):
Success response

Response (Non-Admin):
{
  "error": "Admin access required"
}
```

#### PUT /books/{book_id} (Admin Only)
```
Request:
PUT /books/1?user_email=admin@example.com
{
  "title": "Updated Title",
  "author": "Updated Author",
  "genre": "Updated Genre",
  "stock": 20
}

Response (Admin):
"successfully updated!"

Response (Non-Admin):
{
  "error": "Admin access required"
}
```

#### DELETE /books/{book_id} (Admin Only)
```
Request:
DELETE /books/1?user_email=admin@example.com

Response (Admin):
{
  "Noti": "Delete successfully!"
}

Response (Non-Admin):
{
  "error": "Admin access required"
}
```

---

### Borrow/Return Endpoints

#### POST /borrow
```
Request:
{
  "user_id": 1,
  "title": "Book Title"
}

Response:
"User No: 1 has borrow Book Title"
```

#### GET /borrow
```
Request:
GET /borrow?limit=10

Response:
[
  {
    "username": "John Doe",
    "Borrow": ["Book 1", "Book 2"]
  },
  ...
]
```

#### POST /return
```
Request:
{
  "user_id": 1,
  "title": "Book Title"
}

Response:
"User No: 1 has return Book Title"
```

---

## 🔍 Debugging Tips

### Check Frontend State
```javascript
// In browser console
import { AuthContext } from './context/AuthContext';

// Check stored user
const user = localStorage.getItem('user');
console.log('Stored user:', JSON.parse(user));

// Check device_id
const device = localStorage.getItem('device_id');
console.log('Device ID:', device);
```

### Check Backend Logs
```
# Terminal where backend is running should show:
- Login attempt
- OTP generation
- Device verification
- Role check results
```

### Test Network Requests
```javascript
// In browser DevTools > Network tab
// Watch requests to:
// - POST /login
// - POST /verify-device
// - GET /books
// - POST /books (if admin)

// Check response body for role information
```

### Database Check
```sql
-- Check users table
SELECT id, name, email, role, status FROM users;

-- Check devices table
SELECT id, user_id, device_id FROM devices;

-- Check borrow table
SELECT id, user_id, title FROM borrow;
```

---

## ⚠️ Common Issues & Solutions

### Issue: "Admin access required" error on login
**Solution**: Make sure user role is set to 'admin' in database
```sql
UPDATE users SET role='admin' WHERE email='admin@example.com';
```

### Issue: Redirects to /books instead of /admin after admin login
**Solution**: Check that backend returns correct role in login response
```bash
# Test API directly
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password123","device_id":"test"}'
```

### Issue: Frontend can't find ProtectedAdminRoute
**Solution**: Ensure file exists at `Frontend/src/component/ProtectedAdminRoute.jsx`

### Issue: OTP not working
**Solution**: 
1. Check email configuration in backend
2. For testing, OTP will be in console logs if email is not configured
3. Use same device_id for testing to avoid OTP requirement

### Issue: Database locked error
**Solution**: 
1. Close all database connections
2. Restart backend server
3. Check that database.db is not open in another application

---

## 📊 Test Results Checklist

- [ ] Admin can login and access /admin
- [ ] Admin can add books (role='admin')
- [ ] Admin can update books (role='admin')
- [ ] Admin can delete books (role='admin')
- [ ] Regular user can signup (role forced to 'user')
- [ ] Regular user can login
- [ ] Regular user redirected from /admin to /books
- [ ] Regular user gets error on add book attempt
- [ ] Unauthenticated user redirected to /login
- [ ] Logout clears session
- [ ] Role persists across page refresh (localStorage)
- [ ] Device verification works correctly
- [ ] New device gets OTP requirement

---

## 🚀 Running the Full Application

### Terminal 1: Backend
```bash
cd Backend
python main.py

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2: Frontend
```bash
cd Frontend
npm run dev

# Expected output:
#   VITE v... dev server running at:
#   http://localhost:5173/
```

### Terminal 3: Test
```bash
# Run tests, view logs, check API responses
# Monitor both backend and frontend output
```

---

## 📝 Notes

- Device fingerprinting uses browser userAgent + language + screen resolution
- OTP valid for 5 minutes (configurable via `OTP_EXPIRY_MINUTES`)
- Passwords stored as plain text in DB (should hash in production!)
- CORS configured for localhost and production URLs
- SQLite database file at `Backend/database/database.db`

---

**All tests should pass with the implemented changes!** ✅
