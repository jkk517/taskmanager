# Task Manager – FastAPI + Vanilla JS

A full-stack task manager with JWT authentication, built with FastAPI (backend) and plain HTML/JS (frontend).

---

## Features

- User registration & login with JWT authentication
- Password hashing with bcrypt
- Full task CRUD (create, read, update, delete)
- Mark tasks as complete / incomplete
- Pagination & filtering (`?completed=true/false`)
- Users can only access their own tasks
- Interactive API docs at `/docs`
- Pytest test suite
- Dockerfile included

---

## Project Structure

```
taskmanager/
├── README.md
├── frontend/
│   └── index.html          ← single-file UI served by FastAPI
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    ├── .env.example
    └── app/
        ├── main.py
        ├── core/
        │   ├── config.py
        │   └── security.py
        ├── db/
        │   └── database.py
        ├── models/
        │   └── models.py
        ├── schemas/
        │   └── schemas.py
        └── routers/
            ├── deps.py
            ├── auth.py
            └── tasks.py
    └── tests/
        ├── conftest.py
        ├── test_auth.py
        └── test_tasks.py
```

---

## Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/taskmanager.git
cd taskmanager/backend

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and set a strong SECRET_KEY

# 5. Run the server
uvicorn app.main:app --reload

# App:  http://localhost:8000
# Docs: http://localhost:8000/docs
```

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | JWT signing secret (change this!) | `dev-secret-key-change-in-production` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime in minutes | `30` |
| `DATABASE_URL` | SQLAlchemy DB URL | `sqlite:///./taskmanager.db` |

> ⚠️ Never commit your `.env` file. Use `.env.example` as the template.

---

## API Endpoints

### Authentication
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login and receive a JWT |

### Tasks (all require `Authorization: Bearer <token>`)
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks` | List tasks (paginated, filterable) |
| `GET` | `/tasks/{id}` | Get a specific task |
| `PUT` | `/tasks/{id}` | Update a task |
| `DELETE` | `/tasks/{id}` | Delete a task |

**Query params for `GET /tasks`:**
- `?completed=true` — only completed tasks
- `?completed=false` — only active tasks
- `?page=1&page_size=10` — pagination

---

## Running Tests

```bash
cd backend
pytest tests/ -v
```

---

## Docker

```bash
cd backend
docker build -t taskmanager .
docker run -p 8000:8000 -e SECRET_KEY=your-secret taskmanager
```

---

## Deployment (Render)

1. Push this repo to a **public GitHub repository**
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your repo
4. Set **Root Directory** to `backend`
5. **Build command:** `pip install -r requirements.txt`
6. **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add environment variable: `SECRET_KEY` = any random 32+ character string
8. Click **Deploy**

**Live endpoints:**
- Frontend: `https://your-app.onrender.com/`
- API Docs: `https://your-app.onrender.com/docs`
