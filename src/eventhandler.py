'''
Created on Jan 25, 2014

@author: gabriel
'''

from pymouse import PyMouse
from pykeyboard import PyKeyboard

MOTION_DOWN = 0
MOTION_MOVE = 1
MOTION_UP = 2

GESTURE_TAP = 0
GESTURE_DOUBLE_TAP = 1
GESTURE_LONG_PRESS = 2
GESTURE_SCROLL = 3
GESTURE_PINCH = 4

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
                self.performGesture(gestureType, pointers)
                return
        # Otherwise process pointer movement
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
    def performGesture(self, type, pointers):
        s_x, s_y = self.m.position()
        if type == GESTURE_TAP:
            # Primary click if one pointer
            if len(pointers) == 1:
                print "Primary click x:{x}, y:{y}".format(x=s_x, y=s_y)
                self.m.click(s_x, s_y, button=1)
            # Secondary click if two pointers
            elif len(pointers) == 2:
                print "Secondary click x:{x}, y:{y}".format(x=s_x, y=s_y)
                self.m.click(s_x, s_y, button=2)
            # Middle click if three pointers
            elif len(pointers) == 3:
                print "Middle click x:{x}, y:{y}".format(x=s_x, y=s_y)
                self.m.click(s_x, s_y, button=3)
        elif type == GESTURE_DOUBLE_TAP:
            # There is a preceding single tap so we only need to send one more for a double tap
            print "'Double' click x:{x}, y:{y}".format(x=s_x, y=s_y)
            self.m.click(s_x, s_y, button=1)
        elif type == GESTURE_LONG_PRESS:
            pass
        elif type == GESTURE_SCROLL:
            pass
    
    # Calculates the new screen position
    def newMoveScreenPosition(self, a_x, a_y):
        a_diff_x = a_x - self.a_first_x
        a_diff_y = a_y - self.a_first_y
        s_new_x = self.s_first_x + a_diff_x * self.moveSensitivity
        s_new_y = self.s_first_y + a_diff_y * self.moveSensitivity
        return int(s_new_x), int(s_new_y)
        
        