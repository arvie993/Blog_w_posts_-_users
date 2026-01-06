# Aravind's Blog

A full-featured blog application built with Flask, featuring user authentication, comments, and an admin dashboard.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

### User Management
- **User Registration** with comprehensive validation:
  - Email validation
  - Strong password requirements (8+ characters, uppercase, lowercase, numbers, special characters)
  - Password confirmation
  - Name validation
- **User Login/Logout** with Flask-Login session management
- **Gravatar Integration** for user avatars

### Blog Posts
- **Create, Read, Update, Delete (CRUD)** blog posts
- **Rich Text Editor** (CKEditor 4.25.1-lts) for post content
- **Image URLs** for post headers
- **Admin-only** post management (first registered user is admin)

### Comments
- **Authenticated users** can comment on posts
- **AJAX-powered** comment submission (no page reload)
- **Smooth animations** for adding/deleting comments
- **Delete own comments** or admin can delete any comment
- **Toast notifications** for feedback

### Contact Form
- **Form validation** with WTForms
- **Email notifications** sent to admin
- **SMTP integration** (configurable via environment variables)

### UI/UX
- **Bootstrap 5** responsive design
- **Clean, modern interface** based on Start Bootstrap theme
- **Toast notifications** for all actions
- **Loading spinners** during form submissions
- **No page reloads** for comments (AJAX)

## Screenshots

The blog features a clean, modern design with:
- Hero headers with background images
- Card-based post listings with thumbnails
- Rich text editing for posts and comments
- Responsive navigation

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/arvie993/Blog_w_posts_-_users.git
   cd Blog_w_posts_-_users
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your_secret_key_here
   
   # Email Configuration (optional, for contact form)
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password
   ```

   > **Note:** For Gmail, you need to create an [App Password](https://support.google.com/accounts/answer/185833)

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Open in browser**
   ```
   http://127.0.0.1:5002
   ```

## Usage

### First User = Admin
The first user to register becomes the **admin** with special privileges:
- Create new blog posts
- Edit existing posts
- Delete any post
- Delete any comment

### Regular Users
- View all blog posts
- Comment on posts
- Delete their own comments
- Use the contact form

## Project Structure

```
Blog_w_posts_-_users/
├── main.py              # Main Flask application
├── forms.py             # WTForms form definitions
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in repo)
├── instance/
│   └── posts.db         # SQLite database
├── static/
│   ├── css/
│   │   └── styles.css   # Custom styles
│   ├── js/
│   │   └── scripts.js   # JavaScript
│   └── assets/
│       └── img/         # Images
└── templates/
    ├── header.html      # Navigation header
    ├── footer.html      # Footer with social links
    ├── index.html       # Home page with post list
    ├── post.html        # Individual post view
    ├── make-post.html   # Create/edit post form
    ├── register.html    # User registration
    ├── login.html       # User login
    ├── about.html       # About page
    └── contact.html     # Contact form
```

## Technologies Used

- **Backend:** Flask 2.3.2, Python 3.10+
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** Flask-Login, Werkzeug password hashing
- **Forms:** Flask-WTF, WTForms
- **Rich Text:** CKEditor 4.25.1-lts
- **Frontend:** Bootstrap 5, Font Awesome
- **Email:** smtplib (Python standard library)

## Security Features

- CSRF protection on all forms
- Password hashing with PBKDF2-SHA256
- Strong password validation
- Environment variables for sensitive data
- Secure CKEditor version (4.25.1-lts)
- Admin-only routes with decorators

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Home page with all posts | No |
| GET/POST | `/register` | User registration | No |
| GET/POST | `/login` | User login | No |
| GET | `/logout` | User logout | Yes |
| GET/POST | `/post/<id>` | View post & add comment | No/Yes |
| GET/POST | `/new-post` | Create new post | Admin |
| GET/POST | `/edit-post/<id>` | Edit post | Admin |
| GET | `/delete/<id>` | Delete post | Admin |
| DELETE | `/delete-comment/<id>` | Delete comment | Owner/Admin |
| GET | `/about` | About page | No |
| GET/POST | `/contact` | Contact form | No |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Author

**Aravind Sridharan**
- LinkedIn: [aravinds93](https://www.linkedin.com/in/aravinds93/)
- GitHub: [arvie993](https://github.com/arvie993)
- Email: arv993@gmail.com

## Acknowledgments

- [100 Days of Code - Python](https://www.udemy.com/course/100-days-of-code/) by Dr. Angela Yu
- [Start Bootstrap](https://startbootstrap.com/) for the theme
- [Flask Documentation](https://flask.palletsprojects.com/)
