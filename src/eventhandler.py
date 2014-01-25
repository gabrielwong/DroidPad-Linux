'''
Created on Jan 25, 2014

@author: gabriel
'''

from pymouse import PyMouse
from pykeyboard import PyKeyboard

class EventHandler:
    m = PyMouse()
    k = PyKeyboard()
    
    def handle(self, event):
        pointers = event["pointers"]
        gesture = event["gesture"]
        
        # Test for valid input
        if pointers == None or len(pointers) == 0:
            print "No pointers given"
            return
        
        prev_x, prev_y = self.m.position()
        
        # Interpret gestures if present
        if gesture != None:
            gestureType = gesture["type"]
            if gestureType != None:
                self.performGesture(type, prev_x, prev_y)
        
        self.m.move(pointers[0]["x"], pointers[0]["y"])
            
    def performGesture(self, type, prev_x, prev_y):
        if type == 0:
            print "Primary click x:{x}, y:{y}".format(x=prev_x, y=prev_y)
            self.m.click(prev_x, prev_y, button=1)
        elif type == 1:
            print "Right click x:{x}, y:{y}".format(x=prev_x, y=prev_y)
            self.m.click(prev_x, prev_y, button=2)
    


        