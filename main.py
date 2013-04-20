# -*- coding: utf-8 -*-

import objc
import sys
import getpass
from AppKit import *
from PyObjCTools.KeyValueCoding import *
from PyObjCTools import AppHelper

import keepass_http
from keepass_http import KeePassHttpServer

import threading

class KeePassHttpX(NSApplication):

    def finishLaunching(self):
        # Make statusbar item
        statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        self.icon = NSImage.alloc().initByReferencingFile_('icon.png')
        self.icon.setScalesWhenResized_(True)
        self.icon.setSize_((20, 20))
        self.statusitem.setImage_(self.icon)

        #make the menu
        self.menubarMenu = NSMenu.alloc().init()

        #self.menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Click Me', 'clicked:', '')
        #self.menubarMenu.addItem_(self.menuItem)

        self.quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
        self.menubarMenu.addItem_(self.quit)

        #add menu to statusitem
        self.statusitem.setMenu_(self.menubarMenu)
        self.statusitem.setToolTip_('KeePassHttpX')

    def clicked_(self, notification):
        NSLog('clicked!')

def start(db_path, password):
    server = KeePassHttpServer(db_path, password)
    server.activate()

if __name__ == "__main__":

    db_path = sys.argv[1]
    print "KeePass DB v1 path:" + db_path

    defaults = NSUserDefaultsController.sharedUserDefaultsController().values()
    password = getKey(defaults, 'password')

    if password is None:
        password = getpass.getpass("Enter Password: ")
        defaults.setValue_forKey_(password, 'password');

    print getKey(defaults, 'password')

    app = KeePassHttpX.sharedApplication()
    t = threading.Thread(target=start, args=(db_path, password))
    t.setDaemon(True)
    t.start()
    AppHelper.runEventLoop()
