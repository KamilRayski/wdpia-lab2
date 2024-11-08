# User Management API with PostgreSQL in Docker

## Project Description

This project is a web application with an API for managing users. It consists of:

- **Back-end server** written in Python, handling CRUD operations for user data.
- **PostgreSQL database** to store user information.
- **pgAdmin** - a tool for managing the PostgreSQL database.
- **Front-end interface** for displaying, adding, and deleting users.

The project is containerized using Docker Compose, which simplifies the process of running all application components.

## Project Structure

- **docker-compose.yml** - The configuration file for Docker Compose to launch the application.
- **python_server/server.py** - Python server handling HTTP requests and database interactions.
- **postgres_init/init.sql** - SQL file for initializing the database and creating the users table.
- **public/** - Directory containing front-end files, including JavaScript for interacting with the API.

## Requirements

- **Docker** and **Docker Compose** installed on your machine.
- **Postman** (optional) for testing the API.

## Installation and Setup

1. **Clone the repository**:
  ```bash
  git clone https://github.com/yourusername/yourproject.git
  cd yourproject
  ```
2. **Build and launch containers:** In the root directory of the project, run:
  ```bash docker-compose up --build```
3. **Verify the setup:** After launching, you should see container logs. The application runs on the following ports:
- **API (Python server)** at http://localhost:8000
- **pgAdmin** at http://localhost:5050 (login: admin@admin.com, password: admin)
- **Front-end** at http://localhost (if a static file server is configured)
  
### PostgreSQL Database Configuration

- **pgAdmin** is accessible at http://localhost:5050.
- Default database configuration:
  ```bash
  Database name: mydatabase
  User: myuser
  Password: mypassword
  Database Structure
  ```

The users table is automatically created on first launch, thanks to the init.sql file. The table has the following columns:

- **id:** Primary key (SERIAL)
- **first_name:** User's first name (VARCHAR)
- **last_name:** User's last name (VARCHAR)
- **role:** User's role (VARCHAR)
- **user_id:** Unique identifier for the user (VARCHAR)

## API Testing with Postman

Postman can be used to test the API endpoints.

1. **Retrieve List of Users (GET)**
- **Method:** GET
- **URL:** http://localhost:8000
- Description: Fetches a list of all users in JSON format.
  
2. **Add a New User (POST)**
- **Method:** POST
- **URL:** http://localhost:8000
- **Body:** JSON format:
```bash
{
    "first_name": "John",
    "last_name": "Doe",
    "role": "student",
    "user_id": "unique-id-123"
}
```
- Description: Adds a new user with the provided data in the request.
  
3. **Delete a User (DELETE)**
- **Method:** DELETE
- **URL:** http://localhost:8000/{user_id}
- Description: Deletes the user with the specified user_id from the database.

## Accessing pgAdmin

1. Open a browser and go to http://localhost:5050.
2. Log in using the credentials:
- **Email:** admin@admin.com
- **Password:** admin
3. Add a new server in pgAdmin:
- **Name:** Any name, e.g., PostgresDB
- Connection tab settings:
  - **Host name/address:** postgres
  - **Port:** 5432
  - **Maintenance database:** mydatabase
  - **Username:** myuser
  - **Password:** mypassword
- Save the server and connect to explore the database and tables.

## License

This project is licensed under the **MIT License**.
