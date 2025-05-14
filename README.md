# Task Manager Project

## Description
The Task Manager is a Django-based API project designed to manage tasks efficiently. It provides features for user authentication, role-based access control, and task management including creating, updating, deleting, and retrieving tasks.

## Features
- User Authentication with JWT
- Role-based Access Control (Admin, User)
- Task Management (CRUD operations)
- PostgreSQL Database
- Comprehensive Test Suite

## Prerequisites
- Python 3.8+
- PostgreSQL
- Virtualenv

## Installation

### Clone the Repository
```bash
git clone https://github.com/snelisile-m/task-manager-API.git
cd task_manager_project
```

### Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Database Setup

### Create PostgreSQL Database
1. Open PostgreSQL shell:
   ```bash
   psql -U postgres
   ```
2. Create a new database:
   ```sql
   CREATE DATABASE taskmanager;
   ```
3. Exit the shell:
   ```sql
   \q
   ```

### Configure Database Settings
Ensure the `DATABASES` setting in `settings.py` is configured as follows:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taskmanager',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Migrations

### Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Running the Server
```bash
python manage.py runserver
```

## Testing
Run the test suite to ensure everything is working correctly:
```bash
python manage.py test
```

## API Documentation
API documentation is available in `API_DOCUMENTATION.md`.

## Contact
For any queries or support, please contact [snelisile@hotmail.com](mailto:snelisile@hotmail.com).
