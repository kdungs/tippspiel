# tippspiel
An online game of betting on football matches.

**This code is heavily under development.** Don't expect anything to be running yet.

## What has been done?
 * Basic Structure for a django app
 * Install script that fetches the schedule from bundesliga.de and installs it into the database.

## How to test the code?
 * Install [django](https://www.djangoproject.com/).
 * For the install script you will also have to install [requests](http://docs.python-requests.org/en/latest/index.html).
 * Setup a basic django project `django-admin.py startproject bundesliga`.
 * Add `AUTH_PROFILE_MODULE = 'tippspiel.Player` to your settings.py.
 * Add `'tippspiel',` to the installed apps.
 * Copy the tippspiel folder into your project's folder.
 * Run `./manage.py syncdb` and make sure to setup your admin account.
 * Run `./manage.py shell` and in the shell `from tippspiel import install` and finally `install.install()`.
 * You should be ready to go.

## Where's the EURO 2012 version?
It has been moved to an own [branch](https://github.com/SirCoemgen/tippspiel/tree/euro2012).
