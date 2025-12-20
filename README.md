# Django News Application

A comprehensive news platform built with Django featuring role-based access control, article management, subscriptions, automated notifications, and a RESTful API.

## Features

### User Roles & Permissions
- **Readers**: View articles, subscribe to publishers and journalists
- **Journalists**: Create, edit, and submit articles for approval
- **Editors**: Review and approve articles for publication

### Core Functionality
- Custom user authentication with role-based access control
- Article creation and approval workflow
- Publisher and journalist profiles
- Subscription system (subscribe to publishers or individual journalists)
- Automated email notifications when articles are approved
- Automatic posting to X (Twitter) when articles are published
- RESTful API with subscription-based filtering
- Comprehensive unit tests for API endpoints

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: MariaDB
- **API**: Django REST Framework
- **Email**: Django Email System
- **External APIs**: X (Twitter) API v2

## Installation & Setup

### Prerequisites
- Python 3.8+ (for venv setup)
- MariaDB 10.5+ (for local database)
- pip (Python package manager)
- Docker and Docker Compose (for Docker setup - optional)

---

## Method 1: Using Virtual Environment (venv)

### 1. Clone or Extract the Project

\`\`\`bash
cd news-application-development
\`\`\`

### 2. Create Virtual Environment

\`\`\`bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
\`\`\`

### 3. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configure Database

Create a MariaDB database:

\`\`\`sql
CREATE DATABASE news_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
\`\`\`

### 5. Environment Configuration

Create a `.env` file in the project root with the following variables:

\`\`\`bash
# Database Configuration
DB_NAME=news_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@newsapp.com

# Twitter API Configuration (Optional)
TWITTER_API_KEY=your-api-key
TWITTER_API_SECRET=your-api-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-access-token-secret
TWITTER_BEARER_TOKEN=your-bearer-token
\`\`\`

**Important**: Never commit the `.env` file to version control. It contains sensitive information.

### 6. Run Migrations

\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### 7. Create Superuser

\`\`\`bash
python manage.py createsuperuser
\`\`\`

### 8. Run Development Server

\`\`\`bash
python manage.py runserver
\`\`\`

Visit `http://127.0.0.1:8000/` in your browser.

---

## Method 2: Using Docker

### 1. Clone or Extract the Project

\`\`\`bash
cd news-application-development
\`\`\`

### 2. Create Environment File

Create a `.env` file in the project root (see Method 1, Step 5 for required variables).

**Note**: For Docker, you may need to adjust `DB_HOST` to your database container name or host machine IP if using an external database.

### 3. Build Docker Image

\`\`\`bash
docker build -t news-app .
\`\`\`

### 4. Run Docker Container

\`\`\`bash
docker run -d -p 8000:8000 --env-file .env --name news-app news-app
\`\`\`

Or if you need to mount volumes for media files:

\`\`\`bash
docker run -d -p 8000:8000 --env-file .env -v $(pwd)/media:/app/media --name news-app news-app
\`\`\`

### 5. Access the Application

Visit `http://localhost:8000/` in your browser.

### 6. Create Superuser (Inside Container)

\`\`\`bash
docker exec -it news-app python manage.py createsuperuser
\`\`\`

### 7. Stop and Remove Container

\`\`\`bash
docker stop news-app
docker rm news-app
\`\`\`

**Note**: The Dockerfile runs migrations automatically on container start. For production use, you may want to modify the CMD to use a proper WSGI server like gunicorn.

## Usage Guide

### For Readers
1. Register with the "Reader" role
2. Browse publishers and journalists
3. Subscribe to publishers or journalists you're interested in
4. View your personalized feed in "My Feed"
5. Receive email notifications when new articles are published

### For Journalists
1. Register with the "Journalist" role
2. Create articles from the Journalist Dashboard
3. Optionally affiliate with publishers
4. Submit articles for editor approval
5. Track article status (Pending/Approved)

### For Editors
1. Register with the "Editor" role
2. Review pending articles in the Editor Dashboard
3. Approve or reject articles
4. When approved, subscribers are automatically notified via email
5. Approved articles are automatically posted to X (Twitter) if configured

### API Access

The REST API is available at `/api/` endpoints:

**Endpoints:**
- `GET /api/articles/` - Get articles from subscriptions
- `GET /api/articles/by_publisher/?publisher_id=X` - Filter by publisher
- `GET /api/articles/by_journalist/?journalist_id=X` - Filter by journalist
- `GET /api/articles/subscriptions/` - View subscription info
- `GET /api/publishers/` - List all publishers
- `GET /api/journalists/` - List all journalists

**Authentication**: Basic Authentication or Session Authentication

**Example Request:**
\`\`\`bash
curl -u username:password http://127.0.0.1:8000/api/articles/
\`\`\`

## Running Tests

Run the automated unit tests:

\`\`\`bash
python manage.py test news
\`\`\`

This will test:
- API authentication
- Subscription-based article filtering
- Publisher and journalist filtering
- Permission checks
- Data integrity

## Project Structure

\`\`\`
news_project/
├── news/                      # Main application
│   ├── models.py             # Database models
│   ├── views.py              # View logic
│   ├── forms.py              # Forms
│   ├── serializers.py        # API serializers
│   ├── api_views.py          # API views
│   ├── signals.py            # Django signals for automation
│   ├── tests.py              # Unit tests
│   ├── urls.py               # URL routing
│   └── api_urls.py           # API URL routing
├── news_project/             # Project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py              # WSGI configuration
├── templates/                # HTML templates
│   ├── base.html            # Base template
│   └── news/                # App-specific templates
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md               # This file
\`\`\`

## Key Models

- **CustomUser**: Extended user model with role-based fields
- **Publisher**: News organizations
- **Article**: News articles with approval workflow
- **Newsletter**: Newsletter content (extendable feature)

## Automated Features

### Email Notifications
When an editor approves an article, the system automatically:
1. Identifies all readers subscribed to the publisher or journalist
2. Sends mass emails with article details
3. Includes a link to read the full article

### X (Twitter) Integration
Upon article approval, the system:
1. Generates a tweet with article title and summary
2. Posts to the configured X account using the API
3. Includes a link back to the article

## Security Features

- Role-based access control (RBAC)
- Group-based permissions
- Password validation
- CSRF protection
- SQL injection prevention (Django ORM)
- Secure session management

## Development Notes

- The application uses Django Signals (`post_save`) to trigger automated actions
- All API endpoints require authentication
- API results are filtered based on user subscriptions
- Unit tests cover all critical API functionality
- Code follows PEP 8 style guidelines

## Troubleshooting

### Email not sending
- Check your email provider allows SMTP access
- For Gmail, create an App Password instead of using your regular password
- Ensure `EMAIL_USE_TLS` is set to `True`

### Twitter posts not working
- Verify all Twitter API credentials are correct
- Ensure you have "Elevated" access for Twitter API v2
- Check that your app has Read and Write permissions

### Database connection errors
- Verify MariaDB is running
- Check database credentials in `.env`
- Ensure the database exists and is accessible

## Future Enhancements

- Add newsletter scheduling functionality
- Implement article categories and tags
- Add search functionality
- Implement article comments
- Add analytics dashboard
- Support for multiple languages

## License

This project is created for educational purposes as part of a Django capstone project.

## Support

For issues or questions, please refer to the Django documentation at https://docs.djangoproject.com/
