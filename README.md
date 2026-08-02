# 🎓 EduXchange - Backend API

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20.svg)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.17-red.svg)](https://www.django-rest-framework.org/)
[![JWT Auth](https://img.shields.io/badge/Auth-SimpleJWT-orange.svg)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![Cloudinary](https://img.shields.io/badge/Storage-Cloudinary-blueviolet.svg)](https://cloudinary.com/)

**EduXchange** is a robust, RESTful backend API designed for an academic resource-sharing ecosystem. It empowers students and educational communities to buy, sell, lend, or share study materials, notes, textbooks, lab equipment, and electronic items effortlessly across semesters and departments.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Database Setup & Fixtures](#database-setup--fixtures)
  - [Running the Application](#running-the-application)
- [API Reference](#-api-reference)
  - [Authentication & Accounts](#1-authentication--account-management)
  - [Resources & Listings](#2-resources--listings)
  - [Categories & Filters](#3-categories--filters)
  - [User Favorites](#4-user-favorites)
- [Media & Storage Integration](#-media--storage-integration)
- [Project Structure](#-project-structure)
- [License](#-license)

---

## ✨ Features

- 🔐 **Custom Authentication & User Profiles**:
  - Email-based user identification (`CustomUser`) with no username requirement.
  - JWT Authentication using `djangorestframework-simplejwt` with refresh token rotation and blacklisting.
  - Profile management including department, semester (1–8), profile picture, and bio.
  - Email verification workflow and password reset system via Brevo SMTP relay with custom HTML templates.

- 📚 **Resource & Listing Management**:
  - Support for multiple resource types: **Free**, **Lend**, **Sell** (with pricing).
  - Real-time status tracking: **Available**, **Lent**, **Sold**.
  - Multi-file & multi-image support (primary images + additional item gallery).
  - Cloud storage integration via Cloudinary for persistent media assets and document storage.

- 🔍 **Filtering & Search**:
  - Filter listings by category, semester, status, or transaction type.
  - Full-text search across titles, descriptions, and category names.
  - Custom pagination and field ordering.

- ⭐ **User Engagement & Favorites**:
  - Bookmark/favorite listings for quick reference.
  - Dedicated user dashboard endpoints to retrieve personal uploads and saved favorites.

---

## 🛠️ Tech Stack

- **Framework**: Django 6.0+ & Django REST Framework (DRF)
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Authentication**: SimpleJWT (`rest_framework_simplejwt`)
- **Cloud Media Storage**: Cloudinary & `django-cloudinary-storage`
- **Static File Serving**: WhiteNoise
- **Email Service**: Brevo (SMTP Relay)
- **Production Server**: Gunicorn

---

## 🏗️ Project Architecture

```
EduXchange/
├── accounts/          # User authentication, profiles, verification, password resets
├── backend/           # Core Django settings, URL routing, WSGI/ASGI configs
├── listings/          # Educational resources, categories, favorites, media items
├── templates/         # HTML email templates (Password reset UI & confirmations)
├── staticfiles/       # Collected static files (WhiteNoise)
├── media/             # Local media uploads backup/cache
├── data.json          # Combined database fixture
├── listings.json      # Resource & category fixtures
├── accounts.json      # User account fixtures
└── manage.py          # Django management script
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **pip** (Python package manager)
- **PostgreSQL** (Optional for local development; SQLite works out-of-the-box)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/EduXchange.git
   cd EduXchange
   ```

2. **Create and Activate a Virtual Environment**:
   - **Windows**:
     ```powershell
     python -m venv env
     .\env\Scripts\activate
     ```
   - **Linux / macOS**:
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

### Environment Variables

Create a `.env` file in the root directory by duplicating `.env.example`:

```bash
cp .env.example .env
```

Configure your parameters in `.env`:

```ini
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,*

# Database Configuration (PostgreSQL)
DB_NAME=eduxchange_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# Cloudinary Storage Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Brevo SMTP Configuration for Emails
BREVO_SMTP_LOGIN=your_brevo_smtp_login
BREVO_SMTP_KEY=your_brevo_api_key

# Backend URL (used in email links)
BACKEND_URL=http://127.0.0.1:8000
```

---

### Database Setup & Fixtures

1. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Load Initial Fixtures** *(Optional)*:
   Populate initial categories, sample users, and listings:
   ```bash
   python manage.py loaddata listings.json
   ```
   *or load the full dataset:*
   ```bash
   python manage.py loaddata data.json
   ```

3. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

---

### Running the Application

Start the local Django development server:

```bash
python manage.py runserver
```

The API server will be available at `http://127.0.0.1:8000/`.

---

## 📡 API Reference

Base URL: `http://127.0.0.1:8000/`

### 1. Authentication & Account Management

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :---: | :--- |
| `POST` | `/api/auth/register/` | ❌ | Register a new user account |
| `POST` | `/api/auth/login/` | ❌ | Authenticate user & obtain JWT tokens |
| `POST` | `/api/auth/refresh/` | ❌ | Refresh JWT access token |
| `GET` | `/api/auth/profile/` | `Bearer Token` | Retrieve current user profile details |
| `PUT / PATCH` | `/api/auth/profile/` | `Bearer Token` | Update user profile (bio, dept, semester, avatar) |
| `GET` | `/api/auth/user/<id>/` | ❌ | View public profile of a user |
| `GET` | `/api/auth/verify-email/<token>/` | ❌ | Verify email address via link token |
| `POST` | `/api/auth/forget-password/` | ❌ | Request password reset email |
| `POST` | `/reset-password/<token>/` | ❌ | Complete password reset process |

---

### 2. Resources & Listings

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :---: | :--- |
| `GET` | `/api/resources/` | `Bearer Token` | List resources (Supports filtering, search, pagination) |
| `POST` | `/api/resources/` | `Bearer Token` | Create a new resource listing |
| `GET` | `/api/resources/<id>/` | `Bearer Token` | Retrieve detailed view of a specific resource |
| `PUT / PATCH` | `/api/resources/<id>/` | `Owner Only` | Edit a resource listing |
| `DELETE` | `/api/resources/<id>/` | `Owner Only` | Delete a resource listing |
| `GET` | `/api/resources/user/` | `Bearer Token` | List all resources uploaded by the logged-in user |
| `DELETE` | `/api/delete-image/<id>/` | `Owner Only` | Delete a specific extra image from a resource |

---

### 3. Categories & Filters

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :---: | :--- |
| `GET` | `/api/categories/` | ❌ | List all resource categories |
| `GET` | `/api/semesters/` | ❌ | List available semester options (Semesters 1 - 8) |
| `GET` | `/api/statuses/` | ❌ | List available status options (`available`, `lent`, `sold`) |
| `GET` | `/api/types/` | ❌ | List available resource types (`free`, `lend`, `sell`) |

#### Query Parameters for Resource Filtering:
- `search`: Search title, description, or category name (e.g., `/api/resources/?search=physics`)
- `category`: Filter by category ID
- `semester`: Filter by semester integer (1-8)
- `type`: Filter by transaction type (`free`, `lend`, `sell`)
- `status`: Filter by availability status (`available`, `lent`, `sold`)
- `ordering`: Sort by fields like `created_at`, `updated_at`, `title` (e.g., `/api/resources/?ordering=-created_at`)

---

### 4. User Favorites

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :---: | :--- |
| `POST` | `/api/resources/<id>/favorite/` | `Bearer Token` | Add resource to favorites |
| `DELETE` | `/api/resources/<id>/remove-favorite/` | `Bearer Token` | Remove resource from favorites |
| `GET` | `/api/favorites/` | `Bearer Token` | List all favorited resources of the current user |

---

## ☁️ Media & Storage Integration

- **Cloudinary Storage**: User profile pictures, resource cover images, extra gallery photos, and document attachments (PDFs, raw files) are securely stored and served via Cloudinary.
- **WhiteNoise**: Collects and serves static assets efficiently in production without requiring separate web server configurations.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/YourFeatureName`
3. Commit your changes: `git commit -m 'Add concise feature description'`
4. Push to the branch: `git push origin feature/YourFeatureName`
5. Open a Pull Request.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
