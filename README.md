# Book bounty Backend

Book bounty is a book management system built with Django REST Framework, allowing users to manage books and reading lists efficiently.

## Features
- User authentication with JWT (JSON Web Token)
- Profile management with avatar and favorite genre selection
- Book management (CRUD operations with cover image and PDF upload)
- Reading list management with book ordering

## Prerequisites
- **Python 3.10+**
- **Git** (for cloning the repository)
- **Virtual Environment** (recommended for package management)

## Setup Instructions

### 1. Clone the Repository
```bash
  git clone https://github.com/Rabah-Muhammed/bookbounty_backend.git
  cd bookbounty
```

### 2. Create a Virtual Environment
```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
  pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file and add:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Apply Migrations
```bash
  python manage.py makemigrations
  python manage.py migrate
```

### 6. Create a Superuser (Optional)
```bash
  python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
  python manage.py runserver
```

## API Endpoints

| Endpoint                                      | Method         | Description                   | Permissions       |
|-----------------------------------------------|---------------|-------------------------------|-------------------|
| `/api/register/`                              | `POST`        | Register a new user           | `AllowAny`        |
| `/api/login/`                                 | `POST`        | Login and obtain JWT token    | `AllowAny`        |
| `/api/token/refresh/`                         | `POST`        | Refresh access token          | `AllowAny`        |
| `/api/profile/`                               | `GET/PUT`     | Get or update profile         | `IsAuthenticated` |
| `/api/books/`                                 | `GET/POST`    | List or create books          | `IsAuthenticated` |
| `/api/books/<int:book_id>/`                   | `GET/PUT`     | Retrieve or update a book     | `IsAuthenticated` |
| `/api/books/<int:book_id>/delete/`            | `DELETE`      | Delete a book                 | `IsAuthenticated` |
| `/api/all-books/`                             | `GET`         | Get all books                 | `AllowAny`        |
| `/api/reading-lists/`                         | `GET/POST`    | List or create reading lists  | `IsAuthenticated` |
| `/api/reading-lists/<int:pk>/`                | `GET/PUT/DELETE` | Manage a reading list      | `IsAuthenticated` |
| `/api/reading-lists/<int:list_id>/add-book/`  | `POST`        | Add a book to reading list    | `IsAuthenticated` |
| `/api/reading-lists/<int:list_id>/remove/<int:book_id>/` | `DELETE` | Remove a book from list | `IsAuthenticated` |
| `/api/reading-lists/<int:list_id>/reorder/`   | `PUT`         | Reorder books in a list       | `IsAuthenticated` |

For API documentation:
- Swagger: `http://127.0.0.1:8000/api/schema/swagger-ui/`
- Redoc: `http://127.0.0.1:8000/api/schema/redoc/`

## Deployment
### To Deploy on Render
1. Set up a new Django project on **Render**.
2. Add the following environment variables:
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `DEBUG=False`
3. Update `ALLOWED_HOSTS` in settings for your Render domain.
4. Deploy via GitHub.

## Contributing
- Fork the repository.
- Create a feature branch (`git checkout -b feature-name`).
- Commit changes (`git commit -m "Add feature"`).
- Push to the branch (`git push origin feature-name`).
- Open a pull request.

## License
This project is licensed under the MIT License.
