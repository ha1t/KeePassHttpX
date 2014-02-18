# -*- coding: utf-8 -*-

import objc
# import sys
from AppKit import *
from PyObjCTools.KeyValueCoding import *
from PyObjCTools import AppHelper

import openfile
from keepass_http import KeePassHttpServer
from password_dialog import PasswordDialogController

import threading

from storage import Storage

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

        self.menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Change DB', 'clicked:', '')
        self.menubarMenu.addItem_(self.menuItem)

        self.quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
        self.menubarMenu.addItem_(self.quit)

        #add menu to statusitem
        self.statusitem.setMenu_(self.menubarMenu)
        self.statusitem.setToolTip_('KeePassHttpX')

    def clicked_(self, notification):
        db_path = openfile.openfile();
        # NSLog('clicked!')

def start(db_path, password):
    server = KeePassHttpServer(db_path, password)
    server.activate()

if __name__ == "__main__":

    app = KeePassHttpX.sharedApplication()

    # Bring app to top
    NSApp.activateIgnoringOtherApps_(True)

    viewController = PasswordDialogController.alloc().initWithWindowNibName_('PasswordDialog')
    viewController.showWindow_(viewController)
    #viewController.worksWhenModal = True

    defaults = NSUserDefaultsController.sharedUserDefaultsController().values()
    db_path = getKey(defaults, 'db_path')

    if db_path is None:
        db_path = openfile.open_file();
        defaults.setValue_forKey_(db_path, 'db_path');

    #password = getKey(defaults, 'password')
    #print getKey(defaults, 'password')

    print "KeePass DB v1 path:" + db_path

    t = threading.Thread(target=start, args=(db_path, password))
    t.setDaemon(True)
    t.start()
    AppHelper.runEventLoop()

