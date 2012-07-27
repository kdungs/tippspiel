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

Installation then is as simple as starting python from the command line and running
    
    >>> from tippspiel import setup
    >>> setup()
    [Setup tippspiel]
    Continue? yes

and you are done. The game can then be run locally by just typing

    $ python tippspiel.py

and the game will run locally on port 5000.


## External Sources
The UI hugely benefits from [Twitter's Bootstrap](http://twitter.github.com/bootstrap/) which is licensed under the [http://twitter.github.com/bootstrap/](http://www.apache.org/licenses/LICENSE-2.0) and brings along Glyphicons Free which are licensed under [http://twitter.github.com/bootstrap/](http://creativecommons.org/licenses/by/3.0/). The flag icons are from [famfamfam.com](http://www.famfamfam.com/) and "available for free use for any purpose with no requirement for attribution". The ball icon on the homepage is from [artua.com](http://www.artua.com/freeicons/).


## License
All of the code that is not from an external source and therefore written by me is licensed under the terms of the [WTFPL](http://sam.zoy.org/wtfpl/). This means that you can do **whatever the fuck you want** to do with this code. However I wouldn't mind attribution.

    DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
                       Version 2, December 2004 

    Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 

    Everyone is permitted to copy and distribute verbatim or modified 
    copies of this license document, and changing it is allowed as long 
    as the name is changed. 

               DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
      TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

     0. You just DO WHAT THE FUCK YOU WANT TO.
