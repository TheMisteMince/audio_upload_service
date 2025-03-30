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
-POST /auth/jwt/login: Login with JWT (not implemented for direct use, used internally).
-GET /auth/yandex/login: Redirects to Yandex OAuth for authentication.
-GET /auth/yandex/callback: Callback endpoint for Yandex OAuth, returns a JWT token.
2)Audio Management
-POST /audio/upload-audio: Upload an audio file (requires authentication).
-GET /audio/my-audio: Get a list of your uploaded audio files (requires authentication).
3)User Management (Admin Only)
-GET /users/: List all users (requires superuser).
-PUT /users/{user_id}: Update a user (requires superuser).
-DELETE /users/{user_id}: Delete a user (requires superuser).
