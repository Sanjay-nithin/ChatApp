# Simple Chat App

A simple real-time chat application built with Django and WebSockets for two people.

## Features

- Real-time messaging using WebSockets (Django Channels)
- Simple login system (no password required)
- Message history
- Clean and modern UI
- Docker support for easy deployment

## Local Development

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run migrations:

```bash
python manage.py migrate
```

3. Create a superuser (optional):

```bash
python manage.py createsuperuser
```

4. Run the development server:

```bash
python manage.py runserver
```

5. Access the app at `http://localhost:8000`

## Docker Deployment

Build and run with Docker:

```bash
docker build -t chatapp .
docker run -p 8000:8000 chatapp
```

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use the following settings:
   - **Environment**: Docker
   - **Build Command**: (automatically detected from Dockerfile)
   - **Start Command**: (automatically detected from Dockerfile)

4. Add environment variables if needed:
   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: False (for production)

5. Deploy!

## Usage

1. Open the app in your browser
2. Enter your name to join the chat
3. Start chatting with the other person!

## Technologies Used

- Django 5.2.6
- Django Channels 4.0.0
- Daphne (ASGI server)
- WebSockets
- Docker

## Notes

- This is a simple chat app designed for two people
- Messages are stored in SQLite database
- For production, consider using Redis for channel layers instead of InMemory
