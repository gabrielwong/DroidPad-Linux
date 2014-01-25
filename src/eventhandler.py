'''
Created on Jan 25, 2014

@author: gabriel
'''

from pymouse import PyMouse
from pykeyboard import PyKeyboard

MOTION_DOWN = 0
MOTION_MOVE = 1
MOTION_UP = 2

class EventHandler:
    m = PyMouse()
    k = PyKeyboard()
    
    # Android coordinates on down
    a_first_x = 0
    a_first_y = 0
    
    # Screen coordinates on down
    s_first_x = 0
    s_first_y = 0
    
    moveSensitivity = 1.
    
    def handle(self, event):
        pointers = event.get("pointers")
        gesture = event.get("gesture")
        
        # Test for valid input
        if pointers == None or len(pointers) == 0:
            print "No pointers given"
            return
        
        # Interpret gestures if present
        if gesture != None:
            gestureType = gesture.get("type")
            if gestureType != None:
                s_x, s_y = self.m.position()
                self.performGesture(type, s_x, s_y)
        else: # Otherwise process pointer movement
            pointer = pointers[0]
            
            # Store initial coordinates
            if pointer["motionEvent"] == MOTION_DOWN:
                self.a_first_x = pointer["x"]
                self.a_first_y = pointer["y"]
                self.s_first_x, self.s_first_y = self.m.position()
                
            # Move the mouse
            elif pointer["motionEvent"] == MOTION_MOVE:
                s_new_x, s_new_y = self.newMoveScreenPosition(pointer["x"], pointer["y"])
                print "Moving cursor to x:{x}, y:{y}".format(x=s_new_x, y=s_new_y)
                self.m.move(s_new_x, s_new_y)

    # Process Gestures
    def performGesture(self, type, prev_x, prev_y):
        if type == 0:
            print "Primary click x:{x}, y:{y}".format(x=prev_x, y=prev_y)
            self.m.click(prev_x, prev_y, button=1)
        elif type == 1:
            print "Right click x:{x}, y:{y}".format(x=prev_x, y=prev_y)
            self.m.click(prev_x, prev_y, button=2)
    
    # Calculates the new screen position
    def newMoveScreenPosition(self, a_x, a_y):
        a_diff_x = a_x - self.a_first_x
        a_diff_y = a_y - self.a_first_y
        s_new_x = self.s_first_x + a_diff_x * self.moveSensitivity
        s_new_y = self.s_first_y + a_diff_y * self.moveSensitivity
        return int(s_new_x), int(s_new_y)
        
        