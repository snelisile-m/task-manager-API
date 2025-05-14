# Task Manager API Documentation

## Overview
The Task Manager API allows users to manage tasks with features such as creating, updating, deleting, and retrieving tasks. The API also supports user authentication using JWT tokens and role-based access control.

### User Roles and Permissions
- **Admin Users**: Can assign tasks to other users and view all tasks.
- **Non-Admin Users**: When they create tasks, these are automatically assigned to them. They can only view tasks assigned to them.


## User Registration
- **Endpoint**: `/api/register/`
- **Method**: POST
- **Description**: Register a new user.
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "role": "ADMIN"
  }
  ```
- **Response**:
  ```json
  {
    "username": "string",
    "email": "string",
    "role": "ADMIN"
  }
  ```


## Authentication
- **Endpoint**: `/api/login/`
- **Method**: POST
- **Description**: Obtain a JWT token by providing valid user credentials.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "refresh": "string",
    "access": "string"
  }
  ```


### Create a Task
- **Endpoint**: `/api/tasks/`
- **Method**: POST
- **Description**: Create a new task.
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "due_date": "YYYY-MM-DD",
    "status": "PENDING",
    "assigned_to": "1"
  }
  ```
- **Headers**:
  - `Authorization: Bearer <access_token>`


## Task Management
### Get All Tasks
- **Endpoint**: `/api/tasks/`
- **Method**: GET
- **Description**: Retrieve all tasks. Requires admin role.
- **Headers**:
  - `Authorization: Bearer <access_token>`


### Get My Tasks
- **Endpoint**: `/api/my-tasks/`
- **Method**: GET
- **Description**: Retrieve tasks assigned to the authenticated user.
- **Headers**:
  - `Authorization: Bearer <access_token>`


### Update a Task
- **Endpoint**: `/api/tasks/{id}/`
- **Method**: PUT
- **Description**: Update an existing task.
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "due_date": "YYYY-MM-DD",
    "status": "IN_PROGRESS"
  }
  ```
- **Headers**:
  - `Authorization: Bearer <access_token>`


### Delete a Task
- **Endpoint**: `/api/tasks/{id}/`
- **Method**: DELETE
- **Description**: Delete a task by ID.
- **Headers**:
  - `Authorization: Bearer <access_token>`


## Error Handling
- All error responses will be returned in the following format:
  ```json
  {
    "detail": "Error message"
  }
  ```


## Contact
For any questions or issues, please contact [support@taskmanager.com](mailto:support@taskmanager.com).
