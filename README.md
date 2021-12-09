# One Minute
This is the server code of our service "Sinabro".
# stack
- Django 3.2.9
- Django REST framework 
- pymysql
- simple jwt
- pyjwt
- asyncio
# how to run
## install dependency
```
pip install -r requirements.txt
```
## start server
test mode
```
python manage.py runserver
```

# directory
```
├── README.md
├── app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   ├── models.py
│   ├── serializer.py
│   ├── tests.py
│   └── views.py
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── my_settings.py
└── requirements.txt
```
