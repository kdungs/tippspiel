# tippspiel
## EURO 2012
An online game of betting on football matches. This version is based on [Flask](http://flask.pocoo.org/) and ran during the EURO2012. With about 20 active players we seldomly had problems. The only few issues might have occured due to sqlite's file-based nature. Further versions will therefore make use of a different database.


## Warnings
In order to avoid false expectations, allow me to say one or two things about the code.

### Language
There is **no localization**. Although I write my code in English, you will encounter some sentences of German, as all players were, in fact, from Germany.

### Code
Everything was kept _really_ simple and implemented in a short period of time. If you encouter errors or bugs please let me know so I can avoid them in future versions.


## Installation
First, you might want to modify line 476 of `tippspiel.py` to create your own administrative account. The default username is `Admin` and its password `default`. You might also want to set your own `SECRET_KEY` on line 21.

Installation then is as simple as starting Python from the command line and running
    
    >>> from tippspiel import setup
    >>> setup()
    [Setup tippspiel]
    Continue? yes

and you are done. The game can then be run locally (on port 5000) by just executing

    $ python tippspiel.py

in a shell.

## External Sources
The UI hugely benefits from [Twitter's Bootstrap](http://twitter.github.com/bootstrap/) which is licensed under the [Apache License v2.0](http://www.apache.org/licenses/LICENSE-2.0) and brings along Glyphicons Free which are licensed under [CC BY 3.0](http://creativecommons.org/licenses/by/3.0/). The flag icons are from [famfamfam.com](http://www.famfamfam.com/) and "available for free use for any purpose with no requirement for attribution". The ball icon on the homepage is from [artua.com](http://www.artua.com/freeicons/).


## License
All of the code that is not from an external source and therefore written by me is licensed under the terms of the [MIT License](http://opensource.org/licenses/mit-license.php). 

    The MIT License (MIT)
    Copyright (c) 2012 Kevin D. (https://github.com/SirCoemgen)

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    