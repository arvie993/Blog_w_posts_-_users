# Architecture Documentation

## Overview

This blog application follows a **Model-View-Controller (MVC)** architectural pattern implemented using Flask. The application is designed for scalability, maintainability, and security.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT BROWSER                          │
│                    (HTML/CSS/JavaScript)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         FLASK SERVER                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Routes    │  │  Templates  │  │      Static Files       │ │
│  │  (main.py)  │  │  (Jinja2)   │  │   (CSS/JS/Images)       │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│         │                │                                      │
│         ▼                │                                      │
│  ┌─────────────┐        │                                      │
│  │   Forms     │◄───────┘                                      │
│  │ (forms.py)  │                                               │
│  └─────────────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              SQLAlchemy ORM Layer                        │   │
│  │  ┌─────────┐  ┌───────────┐  ┌─────────────┐           │   │
│  │  │  User   │  │  BlogPost │  │   Comment   │           │   │
│  │  │  Model  │  │   Model   │  │    Model    │           │   │
│  │  └─────────┘  └───────────┘  └─────────────┘           │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SQLite DATABASE                            │
│                      (posts.db)                                 │
│  ┌─────────┐  ┌───────────┐  ┌─────────────┐                  │
│  │  users  │  │blog_posts │  │  comments   │                  │
│  └─────────┘  └───────────┘  └─────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
```

## Database Schema

### Entity Relationship Diagram

```
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│      USERS       │       │    BLOG_POSTS    │       │     COMMENTS     │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │       │ id (PK)          │
│ email            │       │ author_id (FK)───┼───────│ author_id (FK)───┤
│ password         │       │ title            │       │ post_id (FK)─────┤
│ name             │       │ subtitle         │       │ text             │
└────────┬─────────┘       │ date             │       └──────────────────┘
         │                 │ body             │                │
         │                 │ img_url          │                │
         │                 └────────┬─────────┘                │
         │                          │                          │
         └──────────────────────────┴──────────────────────────┘
                     One-to-Many Relationships
```

### Table Definitions

#### Users Table
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| email | String(100) | UNIQUE, NOT NULL | User's email |
| password | String(100) | NOT NULL | Hashed password |
| name | String(100) | NOT NULL | Display name |

#### Blog Posts Table
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| author_id | Integer | FOREIGN KEY → users.id | Post author |
| title | String(250) | UNIQUE, NOT NULL | Post title |
| subtitle | String(250) | NOT NULL | Post subtitle |
| date | String(250) | NOT NULL | Publication date |
| body | Text | NOT NULL | Post content (HTML) |
| img_url | String(250) | NOT NULL | Header image URL |

#### Comments Table
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| text | Text | NOT NULL | Comment content (HTML) |
| author_id | Integer | FOREIGN KEY → users.id | Comment author |
| post_id | Integer | FOREIGN KEY → blog_posts.id | Parent post |

## Component Architecture

### 1. Main Application (main.py)

The main Flask application contains:

```python
# Core Components
├── Flask App Configuration
│   ├── SECRET_KEY (from environment)
│   ├── Database URI
│   └── CKEditor setup
│
├── Database Models
│   ├── User (with UserMixin)
│   ├── BlogPost
│   └── Comment
│
├── Authentication
│   ├── Flask-Login setup
│   ├── User loader
│   └── Admin decorator
│
├── Routes
│   ├── Public Routes
│   │   ├── / (home)
│   │   ├── /post/<id>
│   │   ├── /about
│   │   └── /contact
│   │
│   ├── Auth Routes
│   │   ├── /register
│   │   ├── /login
│   │   └── /logout
│   │
│   └── Admin Routes
│       ├── /new-post
│       ├── /edit-post/<id>
│       └── /delete/<id>
│
└── Utility Functions
    ├── gravatar_url()
    └── admin_only decorator
```

### 2. Forms (forms.py)

WTForms definitions with validation:

```python
Forms
├── CreatePostForm
│   ├── title (DataRequired)
│   ├── subtitle (DataRequired)
│   ├── img_url (DataRequired, URL)
│   └── body (CKEditorField, DataRequired)
│
├── RegisterForm
│   ├── email (DataRequired, Email, Length)
│   ├── password (DataRequired, Length, password_strength)
│   ├── confirm_password (DataRequired, EqualTo)
│   └── name (DataRequired, Length, Regexp)
│
├── LoginForm
│   ├── email (DataRequired, Email)
│   └── password (DataRequired)
│
├── CommentForm
│   └── comment_text (CKEditorField, DataRequired)
│
└── ContactForm
    ├── name (DataRequired, Length)
    ├── email (DataRequired, Email)
    ├── phone (Length)
    └── message (DataRequired, Length)
```

### 3. Templates (Jinja2)

Template inheritance structure:

```
templates/
├── header.html (base navigation + flash messages)
│   └── Includes: navbar, flash message container
│
├── footer.html (base footer)
│   └── Includes: social links, copyright, scripts
│
├── index.html
│   └── Extends: header.html, footer.html
│   └── Content: Post list with thumbnails
│
├── post.html
│   └── Extends: header.html, footer.html
│   └── Content: Full post, comments, AJAX handlers
│
├── make-post.html
│   └── Extends: header.html, footer.html
│   └── Content: CKEditor form, AJAX submission
│
├── register.html
│   └── Extends: header.html, footer.html
│   └── Content: Registration form with validation hints
│
├── login.html
│   └── Extends: header.html, footer.html
│   └── Content: Login form
│
├── about.html
│   └── Extends: header.html, footer.html
│   └── Content: About information, social links
│
└── contact.html
    └── Extends: header.html, footer.html
    └── Content: Contact form with validation
```

## Request Flow

### Standard Page Request

```
Browser → GET /post/1
    │
    ▼
Flask Router → show_post(post_id=1)
    │
    ▼
Database Query → SELECT * FROM blog_posts WHERE id=1
    │
    ▼
Jinja2 Render → post.html with post data
    │
    ▼
Browser ← HTML Response
```

### AJAX Comment Submission

```
Browser → POST /post/1 (AJAX with X-Requested-With header)
    │
    ▼
Flask Router → show_post(post_id=1)
    │
    ├── Validate form
    ├── Check authentication
    ├── Create Comment object
    └── Commit to database
    │
    ▼
JSON Response → {success: true, comment: {...}}
    │
    ▼
JavaScript → Animate new comment into DOM
    │
    ▼
Toast Notification → "Comment added successfully!"
```

## Security Architecture

### Authentication Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Browser   │────▶│    Flask    │────▶│  Database   │
│             │     │             │     │             │
│  Login Form │     │ check_hash  │     │ users table │
│  (email,    │     │ login_user  │     │ (hashed pw) │
│   password) │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │
       ▼                   ▼
┌─────────────────────────────────────┐
│         Session Cookie              │
│  (encrypted with SECRET_KEY)        │
└─────────────────────────────────────┘
```

### Password Security

```
User Input: "MyPassword123!"
           │
           ▼
┌─────────────────────────────────────┐
│     Validation Layer (forms.py)     │
│  ├── Length: 8-128 chars           │
│  ├── Uppercase: at least 1         │
│  ├── Lowercase: at least 1         │
│  ├── Number: at least 1            │
│  └── Special char: at least 1      │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│     Hashing (Werkzeug)              │
│  Method: pbkdf2:sha256              │
│  Salt length: 8                     │
└─────────────────────────────────────┘
           │
           ▼
Database: "pbkdf2:sha256:260000$..."
```

### Authorization Decorator

```python
@admin_only
def protected_route():
    # Only user with id=1 can access
    pass

# Flow:
Request → @admin_only decorator
    │
    ├── current_user.id == 1? → Continue to route
    │
    └── current_user.id != 1? → abort(403)
```

## AJAX Architecture

### Comment System

```javascript
// Frontend (post.html)
┌─────────────────────────────────────────────────────────────┐
│  1. Form Submit Event                                       │
│  2. Prevent default                                         │
│  3. Update CKEditor                                         │
│  4. Show loading spinner                                    │
│  5. Fetch POST with X-Requested-With header                 │
│  6. Parse JSON response                                     │
│  7. Animate new comment OR show error                       │
│  8. Show toast notification                                 │
│  9. Clear form                                              │
└─────────────────────────────────────────────────────────────┘

// Backend (main.py)
┌─────────────────────────────────────────────────────────────┐
│  1. Check X-Requested-With header                           │
│  2. Validate form                                           │
│  3. Check authentication                                    │
│  4. Create comment                                          │
│  5. Return JSON with comment data + gravatar URL            │
└─────────────────────────────────────────────────────────────┘
```

## Environment Configuration

```
.env
├── SECRET_KEY          # Flask session encryption
├── MAIL_SERVER         # SMTP server (e.g., smtp.gmail.com)
├── MAIL_PORT           # SMTP port (e.g., 587)
├── MAIL_USERNAME       # Email address
└── MAIL_PASSWORD       # App password (not regular password)
```

## Scalability Considerations

### Current Limitations
- SQLite database (single-file, not suitable for high concurrency)
- Single server instance
- No caching layer
- No CDN for static files

### Recommended Improvements for Production
1. **Database:** Migrate to PostgreSQL or MySQL
2. **Caching:** Add Redis for session storage and caching
3. **Static Files:** Use CDN (CloudFront, CloudFlare)
4. **Server:** Deploy with Gunicorn + Nginx
5. **Containerization:** Docker for deployment consistency
6. **Monitoring:** Add logging and error tracking (Sentry)

## Deployment Architecture (Recommended)

```
┌─────────────────────────────────────────────────────────────────┐
│                         INTERNET                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     LOAD BALANCER                               │
│                   (AWS ALB / Nginx)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Gunicorn │   │ Gunicorn │   │ Gunicorn │
        │ Worker 1 │   │ Worker 2 │   │ Worker 3 │
        └──────────┘   └──────────┘   └──────────┘
              │               │               │
              └───────────────┼───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PostgreSQL / MySQL                          │
│                    (RDS or managed DB)                          │
└─────────────────────────────────────────────────────────────────┘
```

## Testing Strategy

### Recommended Test Structure
```
tests/
├── conftest.py          # Pytest fixtures
├── test_auth.py         # Authentication tests
├── test_posts.py        # Blog post CRUD tests
├── test_comments.py     # Comment system tests
├── test_forms.py        # Form validation tests
└── test_models.py       # Database model tests
```

### Key Test Cases
1. User registration with valid/invalid data
2. Login/logout functionality
3. Admin-only route protection
4. CRUD operations on posts
5. Comment creation and deletion
6. AJAX endpoint responses
7. Form validation rules

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-06 | Initial release with full feature set |
