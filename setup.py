from distutils.core import setup
import py2app

NAME = 'KeePassHttpX'
SCRIPT = 'main.py'
VERSION = '0.1'
ID = 'KeePassHttpX'

plist = dict(
     CFBundleName                = NAME,
     CFBundleShortVersionString  = ' '.join([NAME, VERSION]),
     CFBundleGetInfoString       = NAME,
     CFBundleExecutable          = NAME,
     CFBundleIdentifier          = 'com.ha1t.%s' % ID,
     LSUIElement                 = '1', #makes it not appear in cmd-tab task list etc.
)

app_data = dict(script=SCRIPT, plist=plist)

setup(
   app = [app_data],
   options = {
       'py2app':{
           'resources':[
               'icon.png'
               ],
           'excludes':[
               ]
           }
       }
)
