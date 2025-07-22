# Django E-Shop 🛒

A modern, full-featured e-commerce web application built with Django, featuring user authentication, product catalog, shopping cart, and order management.

## ✨ Features

### 🔐 User Management

- User registration and authentication
- User profile management with shipping details
- Login/logout functionality
- Profile dashboard with order history and statistics

### 🛍️ Product Management

- Product catalog with detailed product pages
- Product categories and descriptions
- Image uploads for products
- Product caching for improved performance

### 🛒 Shopping Cart

- Session-based cart management
- Add/remove products from cart
- Quantity adjustment (increase/decrease)
- Real-time cart counter in navigation
- Cart persistence across sessions

### 💳 Checkout System

- Professional checkout interface with order summary
- Shipping information collection
- Order creation and management
- Order status tracking (Pending, Accepted, Shipped, Delivered)
- Order history and total spending analytics

### 🎨 User Interface

- Responsive design with Bootstrap 5.3.3
- Font Awesome icons for professional UI
- Auto-dismissing success/error messages
- Modern CSS hover effects
- Mobile-friendly navigation

## 🛠️ Technology Stack

- **Backend**: Django 5.1
- **Frontend**: HTML5, CSS3, Bootstrap 5.3.3
- **Database**: SQLite (default), PostgreSQL compatible
- **Caching**: Redis with django-redis
- **Icons**: Font Awesome 6.4.0
- **Image Handling**: Pillow
- **Session Management**: Django Sessions

## 📋 Prerequisites

- Python 3.12+
- pip (Python package installer)
- pipenv (recommended) or virtualenv
- Redis server (for caching)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AdhamIsHere/Django-EShop.git
cd Django-EShop
```

### 2. Set Up Virtual Environment

```bash
# Using pipenv (recommended)
pipenv install
pipenv shell

# Or using venv
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

### 3. Install and Start Redis

```bash
# On Windows (using Chocolatey)
choco install redis-64

# On Windows (using WSL2)
sudo apt update
sudo apt install redis-server
sudo service redis-server start

# On macOS (using Homebrew)
brew install redis
brew services start redis

# On Ubuntu/Debian
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server

# Verify Redis is running
redis-cli ping
# Should return: PONG
```

### 4. Navigate to Project Directory

```bash
cd E_Shop
```

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📁 Project Structure

```
Django-EShop/
├── README.md
├── Pipfile
├── Pipfile.lock
└── E_Shop/
    ├── manage.py
    ├── db.sqlite3
    ├── E_Shop/                 # Main project settings
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    ├── E_ShopApp/              # Main application
    │   ├── models.py           # Database models
    │   ├── views.py            # Business logic
    │   ├── urls.py             # URL routing
    │   ├── forms.py            # Django forms
    │   ├── admin.py            # Admin interface
    │   ├── templates/          # HTML templates
    │   │   ├── layout.html     # Base template
    │   │   ├── home.html       # Product catalog
    │   │   ├── product_details.html
    │   │   ├── cart.html       # Shopping cart
    │   │   ├── checkout.html   # Checkout page
    │   │   ├── profile.html    # User dashboard
    │   │   ├── login.html
    │   │   ├── signup.html
    │   │   └── style.css       # Custom styles
    │   └── migrations/         # Database migrations
    └── media/                  # User uploaded files
        └── products/           # Product images
```

## 🗄️ Database Models

### Product

- Name, price, stock, category
- Image upload capability
- Detailed descriptions

### Profile

- User profile extension
- Phone, country, city, address
- One-to-one relationship with User

### Order

- Order management with status tracking
- Many-to-many relationship with OrderItems
- Created/updated timestamps

### OrderItem

- Individual items within an order
- Product and quantity tracking
- Price calculation methods

## 🔧 Configuration

### Static Files

Configure static files in `settings.py`:

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'E_ShopApp' / 'templates',
]
```

### Media Files

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Cache Configuration

The application uses Redis for high-performance caching. Configure in `settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

**Redis Benefits:**

- **Product Caching**: Fast retrieval of frequently accessed products
- **Session Storage**: Optional Redis-based session backend
- **Performance**: Significant speed improvements for repeated queries

## 🌟 Key Features Explained

### Shopping Cart System

- **Session-based**: Cart data persists across browser sessions
- **Real-time updates**: Dynamic cart counter in navigation
- **Quantity management**: Easy increase/decrease functionality

### Order Management

- **Status tracking**: Orders progress through Pending → Accepted → Shipped → Delivered
- **Order history**: Users can view all past orders
- **Analytics**: Total spending and order count calculations

### User Experience

- **Responsive design**: Works on desktop, tablet, and mobile
- **Auto-dismissing messages**: User feedback with automatic cleanup
- **Professional UI**: Modern design with Bootstrap and Font Awesome


## 📝 API Endpoints

| Endpoint                  | Method   | Description                    |
| ------------------------- | -------- | ------------------------------ |
| `/`                       | GET      | Home page with product catalog |
| `/signup/`                | GET/POST | User registration              |
| `/login/`                 | GET/POST | User login                     |
| `/logout/`                | POST     | User logout                    |
| `/profile/`               | GET      | User profile dashboard         |
| `/cart/`                  | GET      | Shopping cart view             |
| `/checkout/`              | GET/POST | Checkout process               |
| `/details/<id>/`          | GET      | Product details                |
| `/add-to-cart/<id>/`      | POST     | Add product to cart            |
| `/remove-from-cart/<id>/` | POST     | Remove from cart               |

**Happy Shopping! 🛍️**
