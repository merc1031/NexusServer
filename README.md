NexusServer
===========

Allows Nexus chrome extension to redirect where files will end up being stored

Install on linux (in progress)

sudo apt-get install libevent-dev
sudo easy_install gevent
sudo easy_install greenlet

then sudo apt-get install python-pip python-dev build-essential
sudo pip install --upgrade pip
sudo pip install --upgrade virtualenv
sudo pip install --upgrade bottle
sudo pip install --upgrade gevent
sudo pip install --upgrade greenlet



Install on windows (in progress)

install pyhton 2.6 on windows FOR YOUR USER  32 bit!!!!!!!!!!!
(http://www.python.org/getit/releases/2.6.6/)

Download the last pip version for python 2.6 from here: http://pypi.python.org/pypi/pip#downloads
Uncompress it
Download the last easy installer for Windows python 2.6: (download the .exe at the bottom of http://pypi.python.org/pypi/setuptools ). Install it.

add c:\Python2x to your PATH

go to the uncompressed pip directory and: python setup.py install
Add your python c:\Python2x\Scripts to the PATH


then install this for gevent
http://code.google.com/p/gevent/downloads/detail?name=gevent-1.0b2.win32-py2.6.msi&can=2&q=
and get the greenlet for 2.6 
http://pypi.python.org/pypi/greenlet/

pip install bottle

download latest chrome canary side by side build
https://tools.google.com/dlpage/chromesxs/
go to extensions and put it on developer mode
install unpacked extension > Nexus

set NexusServer to start at boot in whatever manner you want