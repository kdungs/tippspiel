# tippspiel
An online game of betting on football matches.

## Warning
**This code is heavily under development.** Don't expect anything to work yet.

## Where's the EURO 2012 version?
It has been moved to an own [branch](https://github.com/SirCoemgen/tippspiel/tree/euro2012).

## What has been done?
 * Basic Structure for a django app
 * Install script that fetches the schedule from bundesliga.de and installs it into the database.
 * Some first drafts for views
 * Switched from bootstrap to jQuery Mobile

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

## External Sources
The project makes use of [jQuery](http://jquery.com/), [jQuery Mobile](http://jquerymobile.com/) and [django](https://www.djangoproject.com/). None of these are included in the project. Django has to be installed on the server, the jQuery files are loaded from the jQuery CDN.

The icons of the teams are property of their respective owners. They are not included in the project. However there is a script in `tippspiel/static/img/emblems` called `emblems.py` which allows you to download them from a website. You have to be aware, that you might not be allowed to use them.

## License
All of the code in this project, if not stated otherwise, is licensed under the terms of the MIT License.

    The MIT License (MIT)
    Copyright (c) 2012 Kevin Dungs (https://github.com/kdungs)

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    
