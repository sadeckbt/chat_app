# Real-Time Chat Backend

### Django • DRF • Channels • JWT • WebSockets

---

## Preview

---

## Overview

This project is a **real-time chat backend system** built with:

* **Django** for core backend logic
* **Django REST Framework** for APIs
* **Django Channels** for WebSocket communication
* **JWT Authentication** for secure connections

It supports:

* **Group chat (rooms)**
* **Private messaging (1-to-1)**

---

## Features

* JWT authentication for WebSocket
* Real-time group chat
* Private chat system
* Asynchronous WebSocket handling (Channels)
* User-based messaging
* Message persistence (database)
* Redis channel layer
* Custom WebSocket middleware

---

## WebSocket Authentication (JWT)

WebSocket connections use a JWT token passed as query parameter:

```
bash
ws://localhost:8000/ws/chat/room_name/?token=YOUR_JWT_TOKEN
```

The token is:

* extracted from query parameters
* decoded
* attached to `scope["user"]`

---

## Project Structure

```
chat_app/
│── accounts/
│── chat/
│   ├── consumers/
│   │   ├── group.py
│   │   ├── private.py
│   ├── middleware.py
│   ├── models.py
│   ├── routing.py
│   ├── serializers.py
│   ├── views.py
│
│── chat_backend/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
```

---

## Installation

### 1. Clone

```
bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Create virtual environment

```
bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
bash
pip install -r requirements.txt
```

### 4. Run Redis

```bash
redis-server
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run server

```bash
python manage.py runserver
```

---

## WebSocket Endpoints

### Group chat

```
ws://localhost:8000/ws/chat/group/<chat_id>/?token=<JWT_TOKEN>
```

### Private chat

```
ws://localhost:8000/ws/chat/private/<chat_id>/?token=<JWT_TOKEN>
```

---

## Example (JavaScript)

```javascript
const socket = new WebSocket(
  "ws://localhost:8000/ws/chat/privat/test/?token=YOUR_TOKEN"
);

socket.onmessage = (e) => {
  const data = JSON.parse(e.data);
  console.log(data);
};

socket.onopen = () => {
  socket.send(JSON.stringify({
    message: "Hello github"
  }));
};
```

---

## Key Components

| Component          | Description                   |
| ------------------ | ----------------------------- |
| JWTAuthMiddleware  | Authenticates WebSocket users |
| GroupConsumer      | Handles room messages         |
| PrivateConsumer    | Handles private chat          |
| Redis Layer        | Message broadcasting          |
| ASGI Configuration | Protocol routing              |

---

## Notes

* Redis is required for production
* JWT must be valid for WebSocket access
* ASGI must be used (not WSGI)

---

## Contributing

Pull requests are welcome.

---

## License

MIT License

---

## Author

**Sadeck --Backend Developer**
**https://github.com/sadeckbt/**

---
