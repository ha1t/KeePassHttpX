from Cocoa import *
from Foundation import NSObject

class PasswordDialogController(NSWindowController):

    counterTextField = objc.IBOutlet()
 
    def windowDidLoad(self):
        NSWindowController.windowDidLoad(self)
 
        # Start the counter
        self.count = 0
 
    @objc.IBAction
    def increment_(self, sender):
        self.count += 1
        self.updateDisplay()
 
    @objc.IBAction
    def decrement_(self, sender):
        self.count -= 1
        self.updateDisplay()
 
    def updateDisplay(self):
        self.counterTextField.setStringValue_(self.count)
 
