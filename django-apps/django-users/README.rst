=====
Users
=====

Users is a Django app to conduct Web-based users. It contains
Login, Logout, Register views and logics and much more.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "users" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'users.apps.UsersConfig',
    ]

2. Include the users URLconf in your project urls.py like this::

    path('', include('users.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/
    to login or create a new user.