# Heroku Django Starter Template

An utterly fantastic project starter template for Django 1.9.

## Features

- Production-ready configuration for Static Files, Database Settings, Gunicorn, etc.
- Enhancements to Django's static file serving functionality via WhiteNoise

## How to Use

To use this project, follow these steps:

1. Create your working environment.
2. Install dependencies (`$ pip install -r requirements.txt`)
3. Set up database and server
``` 
$ sudo su postgres
$ createdb pixlee_project
$ createuser pixlee -P 
$ (Enter password: pixlee)
$ exit
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
$ Go to http://127.0.0.1:8000/
```
