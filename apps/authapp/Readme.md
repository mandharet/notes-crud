# User Authentication APIs

## 1. User Registration (Signup)

**Endpoint:** `POST /signup`

**Description:** Register a new user.

**Request:**
```json
{
  "username": "testuser",
  "password": "testpassword"
}
```

**Response (201 Created):**
```json
{
  "token": "generated_token",
  "user_id": 123
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Validation error details"
}
```

## 2. User Login

**Endpoint:** `POST /login`

**Description:** Log in a user and obtain an authentication token.

**Request:**
```json
{
  "username": "testuser",
  "password": "testpassword"
}
```

**Response (200 OK):**
```json
{
  "token": "generated_token",
  "user_id": 123
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Both username and password are required."
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

## 3. User Logout

**Endpoint:** `POST /logout`

**Description:** Log out a user by deleting the authentication token.

**Request:**
- Method: `POST`
- Requires authentication.

**Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Note:** Include the user's token in the Authorization header for logout request:

```http
Authorization: Token generated_token_here
```


