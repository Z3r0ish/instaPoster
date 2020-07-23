# instaPoster
An Instagram Poster made in python

# Requirements
* A *nix based OS (I'm using Arch linux)
* [Python and pip](https://www.python.org/downloads/ "Python and pip")
* [instabot (pip install instabot)](https://pypi.org/project/instabot/ "instabot (pip install instabot)")
* [You have to use my instaScraper to get the images / video so it can understand what to do](https://github.com/Z3r0ish/instaScraper "You have to use my instaScraper to get the images / video so it can understand what to do")

## How to use
1. Put the account login on line 1-2 of config.py
2. Put the filepath you want to save the files on line 3 of config.py
    * examples: ``/hdd/media/`` or ``/instagram/``
3. Change the minimum engagement rate (likes over followers) on line 4 of config.py
4. Change the minimum age (in days) of the scrapped post you're using on line 5 of config.py
5. Change the time between post (in seconds) on line 6 of config.py
6. Change the top caption on line 7 of config.py
    * It's an array to so if you want to switch up captions between post
7. Run it by doing ``python instaPoster.py``

### [WTFPL – Do What the Fuck You Want to Public License](http://www.wtfpl.net/ " WTFPL – Do What the Fuck You Want to Public License")
