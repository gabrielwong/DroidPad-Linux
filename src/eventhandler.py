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
GESTURE_LONG_PRESS_DRAG = 3
GESTURE_SCROLL = 4
GESTURE_RIGHT_CLICK = 5

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
    scrollSensitivity = 0.1
    
    isDragging = False
    
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
            #Move mouse
            print "Moving cursor to x:{x}, y:{y}".format(x=s_new_x, y=s_new_y)
            self.m.move(s_new_x, s_new_y)
            
        elif pointer["motionEvent"] == MOTION_UP:
            # Release the mouse for drag
            s_x, s_y = self.m.position()
            self.m.release(s_x, s_y, 1)
            self.isDragging = False

    # Process Gestures
    def performGesture(self, type, pointers):
        s_x, s_y = self.m.position()
        if type == GESTURE_TAP:
            # Primary click if one pointer
            if len(pointers) == 1:
                print "Primary click x:{x}, y:{y}".format(x=s_x, y=s_y)
                self.m.click(s_x, s_y, button=1)
        elif type == GESTURE_DOUBLE_TAP:
            # Perform double click
            print "'Double' click x:{x}, y:{y}".format(x=s_x, y=s_y)
            self.m.click(s_x, s_y, button=1, n = 2)
        elif type == GESTURE_RIGHT_CLICK:
            # Secondary click
            print "Secondary click x:{x}, y:{y}".format(x=s_x, y=s_y)
            self.m.click(s_x, s_y, button=2)
        elif type == GESTURE_LONG_PRESS_DRAG:
            if not self.isDragging:
                self.isDragging = True
                self.m.press(s_x, s_y, 1)
                
                #Store beginning variables
                self.a_first_x = pointers[0]["x"]
                self.a_first_y = pointers[0]["y"]
                self.s_first_x = s_x
                self.s_first_y = s_y
            else:
                # Drag
                s_new_x, s_new_y = self.newMoveScreenPosition(pointers[0]["x"], pointers[0]["y"])
                self.m.move(s_new_x, s_new_y)
        elif type == GESTURE_SCROLL:
            #Scroll
            if len(pointers) == 2:
                # Release if dragging
                if self.isDragging:
                    self.m.release(s_x, s_y, 1)
                    self.isDragging = False
                
                # Average location of both pointers to determine scroll
                a_x = (pointers[0]["x"] + pointers[1]["x"])/2
                a_y = (pointers[0]["y"] + pointers[1]["y"])/2
                
                vertical = (a_y - self.a_first_y) * self.scrollSensitivity
                horizontal = (a_x - self.a_first_x) * self.scrollSensitivity
                
                print "Scrolling vertical:{y} horizontal:{x}".format(x=a_x, y=a_y)
                self.m.scroll(vertical=vertical, horizontal=horizontal)
                
                # Update previous scroll location
                self.a_first_x = a_x
                self.a_first_y = a_y
            
    
    # Calculates the new screen position
    def newMoveScreenPosition(self, a_x, a_y):
        a_diff_x = a_x - self.a_first_x
        a_diff_y = a_y - self.a_first_y
        s_new_x = self.s_first_x + a_diff_x * self.moveSensitivity
        s_new_y = self.s_first_y + a_diff_y * self.moveSensitivity
        
        # Stop at border
        if s_new_x < 0:
            s_new_x = 0
            self.s_first_x = 0
            self.a_first_x = a_x
        if s_new_y < 0:
            self.s_first_y = 0
            s_new_y = 0
            self.a_first_y = a_y
        
        return int(s_new_x), int(s_new_y)
        
        