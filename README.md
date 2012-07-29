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
The project includes [jQuery](http://jquery.com/) which is licensed under the [MIT License](http://jquery.org/license/) and [Bootstrap, from Twitter](http://twitter.github.com/bootstrap/) which is licensed under the [Apache License v2.0](http://www.apache.org/licenses/LICENSE-2.0). Bootstrap also includes Icons from Glyphicons Free which are licensed under [CC BY 3.0](http://creativecommons.org/licenses/by/3.0/).

jQuery and Bootstrap are included in the project. They are both licensed under the terms of their respective licenses.

## License
All of the code in this project, if not stated otherwise, is licensed under the terms of the [MIT License](tippspiel/MIT-LICENSE.txt). 

    The MIT License (MIT)
    Copyright (c) 2012 Kevin D. (https://github.com/SirCoemgen)

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    
