# Affpilot Content Generation Service

A FastAPI microservice for content generation.

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/affpilot-ai/affpilot-content-generation-service.git
cd affpilot-content-generation-service
```

### 2. Create & Activate Virtual Environment

**Linux/Mac:**
```sh
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```sh
python -m venv venv
venv\Scripts\activate
```

### 3. Install Requirements

```sh
pip install -r requirements.txt
```

### 4. Run the Service

```sh
uvicorn app.main:app --reload
# for celery worker
celery --app=app.tasks.celery.celery_app worker --pool=solo --loglevel=DEBUG
```

### 5. Database Migrations (Alembic)

Initialize Alembic:
```sh
alembic init alembic
```
This creates the `alembic/` directory and `alembic.ini` file.

Update the database connection string in `alembic.ini`:
```
sqlalchemy.url = postgresql://postgres:postgres@localhost/affpilot-content-generation
```

In `alembic/env.py`, import your models and database settings:

```python
from app.models.base_model import Base
from app.database.session import DATABASE_URL
```

To generate migration files and apply them:
```sh
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 6. Environment Variables

Create a `.env` file with:

```
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=affpilot_content_generator

JWT_SECRET_KEY=your_jwt_secret
```

### 7. Docker Container Setup

**Build and start the Docker containers:**
```sh
docker compose up --build
```

**Initialize Alembic locally (only once):**
```sh
alembic init alembic
```

** Open a new terminal and run alembic migrations inside the Docker container:**
Whenever you change your models, run it:
```sh
docker exec -it fastapi_app alembic revision --autogenerate -m "Your migration message"
docker exec -it fastapi_app alembic upgrade head
```


### 8. API Testing with Postman

A Postman collection (`postman_collection.json`) is included in the codebase for testing API endpoints.  
You can import this file into Postman to quickly test and explore the available APIs.

**How to use:**
1. Open Postman.
2. Click "Import" and select `postman_collection.json` from the project directory.
3. Use the pre-configured requests to interact with the API.
