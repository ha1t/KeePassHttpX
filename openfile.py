# http://ka010.wordpress.com/2009/03/29/simple-openfile-dialog-in-pyobjc/

from Cocoa import *

def open_file():
    panel = NSOpenPanel.openPanel()
    panel.setCanCreateDirectories_(True)
    panel.setCanChooseDirectories_(True)
    panel.setCanChooseFiles_(True)
    panel.setAllowedFileTypes_(['kdb'])

    if panel.runModal() == NSOKButton:
        return panel.filename()
        # return panel.directory()
    return

if __name__ == "__main__":
    file = open_file()
    print file

