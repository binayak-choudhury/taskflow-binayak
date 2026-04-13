# TaskFlow

A task management system built with Flask and React. Create projects, manage tasks, and collaborate with your team.

## Tech Stack

**Backend:** Flask, PostgreSQL, SQLAlchemy, JWT authentication  
**Frontend:** React + TypeScript, Tailwind CSS, Vite  
**Infrastructure:** Docker, Docker Compose, Nginx

---

## Key Features

- User authentication with JWT (bcrypt password hashing)
- Create and manage projects
- Add tasks with status, priority, and due dates
- Assign tasks to team members
- Filter tasks by status and assignee
- **Pagination** for projects and tasks
- **Project statistics** endpoint (task counts by status, priority, assignee)
- **Repository pattern** for clean data access
- **Integration tests** with pytest
- Responsive design for mobile and desktop
- Docker-based deployment with multi-stage builds

---

## Getting Started

```bash
git clone https://github.com/binayak-choudhury/taskflow-binayak.git
cd taskflow-binayak
cp .env.example .env
docker compose up --build
```

Visit http://localhost:3000 and login with:
- Email: `test@example.com`
- Password: `password123`

---


## Architecture

### Design Patterns

**Repository Pattern**: Separates data access logic from business logic. All database operations go through repository classes (`UserRepository`, `ProjectRepository`, `TaskRepository`).

**Factory Pattern**: Application factory pattern for Flask app creation, enabling easy testing and configuration.

**Dependency Injection**: Repositories are injected into routes, making the code testable and maintainable.

### Key Improvements

- **Pagination**: All list endpoints support `page` and `limit` parameters
- **Statistics**: `/projects/:id/stats` endpoint provides task analytics
- **Tests**: Integration tests for auth, projects, and tasks (run with `pytest`)
- **Clean Architecture**: Repository pattern separates concerns
- **Type Safety**: TypeScript on frontend, type hints on backend

---

## API Reference

Base URL: `http://localhost:5000`

### Authentication

#### Register
```http
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}

Response 201:
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2026-04-13T10:00:00"
  }
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}

Response 200:
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

### Projects

All project endpoints require `Authorization: Bearer <token>` header.

#### List Projects
```http
GET /projects?page=1&limit=20

Response 200:
{
  "projects": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  }
}
```

#### Create Project
```http
POST /projects
Content-Type: application/json

{
  "name": "New Project",
  "description": "Optional description"
}

Response 201: (project object)
```

#### Get Project Details
```http
GET /projects/:id

Response 200:
{
  "id": "uuid",
  "name": "Website Redesign",
  "description": "Q2 project",
  "owner_id": "uuid",
  "created_at": "2026-04-13T10:00:00",
  "tasks": [ ... ]
}
```

#### Update Project
```http
PATCH /projects/:id
Content-Type: application/json

{
  "name": "Updated Name",
  "description": "Updated description"
}

Response 200: (updated project object)
```

#### Delete Project
```http
DELETE /projects/:id

Response 204: (no content)
```

#### Get Project Statistics
```http
GET /projects/:id/stats

Response 200:
{
  "total_tasks": 12,
  "by_status": {
    "todo": 4,
    "in_progress": 3,
    "done": 5
  },
  "by_priority": {
    "low": 2,
    "medium": 6,
    "high": 4
  },
  "by_assignee": {
    "user-id-1": 7,
    "user-id-2": 5
  }
}
```

### Tasks

#### List Tasks
```http
GET /projects/:id/tasks?status=todo&assignee=uuid&page=1&limit=50

Response 200:
{
  "tasks": [...],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 120,
    "pages": 3
  }
}
```

#### Create Task
```http
POST /projects/:id/tasks
Content-Type: application/json

{
  "title": "New task",
  "description": "Task description",
  "status": "todo",
  "priority": "medium",
  "assignee_id": "uuid",
  "due_date": "2026-04-20"
}

Response 201: (task object)
```

#### Update Task
```http
PATCH /tasks/:id
Content-Type: application/json

{
  "title": "Updated title",
  "status": "done",
  "priority": "low"
}

Response 200: (updated task object)
```

#### Delete Task
```http
DELETE /tasks/:id

Response 204: (no content)
```

### Error Responses

```http
400 Bad Request:
{
  "error": "validation failed",
  "fields": {
    "email": "is required",
    "password": "must be at least 6 characters"
  }
}

401 Unauthorized:
{
  "error": "invalid credentials"
}

403 Forbidden:
{
  "error": "forbidden"
}

404 Not Found:
{
  "error": "not found"
}
```

---

## Testing

Run the test suite:

```bash
# Inside backend container
docker compose exec backend pytest

# Or locally
cd backend
pytest -v
```

Tests cover:
- Authentication (register, login, validation)
- Projects CRUD operations
- Tasks CRUD operations
- Authorization checks
- Pagination

---

## What's Next

With more time, I'd add:
- Real-time updates via WebSocket
- User search for task assignment
- Task comments and file attachments
- Drag-and-drop task management
- Dark mode
- Email notifications
