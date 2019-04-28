# RESTful API

An example RESTful API for simple blog build with Django REST framework

## Installation

1. Install dependencies `pip install -r requirements.txt`
2. Set `SECRET_KEY` environment variable
3. Run migrations `python manage.py migrate`
4. Run server `python manage.py runserver`
5. Create superuser `python manage.py createsuperuser`
6. Open url http://127.0.0.1:8000

## API Examples

1. Create blog post as superuser

    `curl -d '{"title":"First post", "text":"Post content"}' -H "Content-Type: application/json" -u admin:password123 -X POST http://127.0.0.1:8000/api/posts/`
    
2. Get blog post with id 1

    `curl -X GET http://127.0.0.1:8000/api/posts/1/`

3. Get posts list

    `curl -X GET http://127.0.0.1:8000/api/posts/`