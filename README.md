# Social-Media-API
RESTful API for a social media platform. The API should allow users to create profiles, follow other users, create and retrieve posts, manage likes and comments, and perform basic social media actions.

## Setup
```
git clone https://github.com/WDemidenko/Social-Media-API.git
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser(optional)
python manage.py runserver
```
API Documentation

http://localhost/api/doc/swagger/
