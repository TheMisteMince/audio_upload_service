1. Git clone
cd audio_upload_service

2. Configure Environment Variables
Create a .env file in the root directory and add the following:

DATABASE_URL=postgresql+asyncpg://user:password@db/dbname
YANDEX_CLIENT_ID=your_yandex_client_id
YANDEX_CLIENT_SECRET=your_yandex_client_secret
SECRET_KEY=your_secret_key

3. Build and Run with Docker Compose
docker-compose up --build

5. Access the API
Open http://localhost:8000/docs in your browser to access the Swagger UI.

API Endpoints:

1)Authentication

-POST /auth/jwt/login: Login with JWT (used internally by fastapi-users, not intended for direct use with Yandex OAuth).

-POST /auth/jwt/logout: Logout (invalidates the JWT token, requires authentication).

-GET /auth/yandex/login: Redirects to Yandex OAuth for authentication.

-GET /auth/yandex/callback: Callback endpoint for Yandex OAuth, returns a JWT token.

2)Audio Management

-POST /audio/upload-audio: Upload an audio file (requires authentication).
Body: file (UploadFile), name (str)
Response: {"message": "File uploaded successfully"}

-GET /audio/my-audio: Get a list of your uploaded audio files (requires authentication).
Response: List of audio files with id, file_name, file_path, uploaded_at.

3)User Management (Admin Only)

-GET /users/: List all users (requires superuser).
Response: List of users with id, email, username, is_active, is_superuser, is_verified.

-PUT /users/{user_id}: Update a user (requires superuser).
Path Parameter: user_id (int)
Body: JSON with fields to update (e.g., {"is_active": false})
Response: {"message": "User updated"}

-DELETE /users/{user_id}: Delete a user (requires superuser).
Path Parameter: user_id (int)
Response: {"message": "User deleted"}
