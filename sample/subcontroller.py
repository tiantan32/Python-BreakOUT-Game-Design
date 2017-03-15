# animation.py
# Walker M. White (wmw2)
# November 17, 2015
"""Module to show off how to use a subcontroller to pause an animation.

As we can see in the state.py module, combining animation with click management
can be quite complicated.  It is often easier to handle animation in a subcontroller
and turn it off in the main app.

The subcontroller should always be a subclass of object.  Instances of GameApp create
a window to draw in, and we only want one window for drawing."""
import colormodel
import random
import math
from game2d import *

############# CONSTANTS #############
# Window Size
WINDOW_WIDTH  = 512
WINDOW_HEIGHT = 512

# Distance from Window Center
ANIMATION_RADIUS = 100
# Amount to change the angle
ANIMATION_STEP   = 0.1
# Ellipse Radius
ELLIPSE_RADIUS = 20

class MainApp(GameApp):
    """Instances represent the main application with a drawing window.
    
    This application listens for touches, pausing and restarting the animation
    every time there is a click.
    
    INSTANCE ATTRIBUTES:
        _animation [Animation]: The subcontroller to process the animation
        _label     [GLabel]:    A label to indicate that the animation is paused
        _paused    [boolean]:   Whether or not the animation is paused
        _last      [GPoint, or None if mouse button is not down]:  
                    the last mouse position (if Button is pressed)
                    
    NOTE: Attributes are hidden in this example, because we have more than one
    class.  The rule is that, when you have more than one class, the one class
    cannot access the hidden attributes or methods of another.
    """
    
    # THREE MAIN METHODS
    def start(self):
        """Initialize the App with all of its attributes"""
        # We have to track key presses for pause to work properly
        self._last = 0
        
        # Create the subcontroller for animation
        self._animation = Animation(self.width,self.height)
        
        # We are not paused, but make label anyway
        self._paused = False
        self._label = GLabel(text="Paused...",font_size=24, left=5, bottom=5)
    
    def update(self,dt):
        """Determines the current state and runs the animation IF not paused.
        
        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float."""
        self._checkPaused()
        
        # Only run the animation if not paused.
        if not self._paused:
            self._animation.update()
    
    def draw(self):
        """Draws the animation and pause label as necessary.
        
        Note that we ALWAYS tell the animation controller to draw, even if
        paused.  That is how we get it to look like it is frozen in place.
        """
        if self._paused:
            self._label.draw(self.view)
        
        self._animation.draw(self.view)
    
    
    # HELPER METHODS
    def _checkPaused(self):
        """Determines if the animation is paused, setting the attribute.
        
        The animation is paused when the user presses a key.  The rules for
        pressing a key are the same as state.py.  A key press is when a key is
        pressed for the FIRST TIME. We do not want the animation to pause and
        unpause while we hold down the key.  The user must release the key and
        press it again to pause or unpause."""
        # Determine the current number of keys pressed
        curr_keys = self.input.key_count
        
        # Only change if we have just pressed the keys this animation frame
        change = curr_keys > 0 and self._last == 0
        
        if change:
            self._paused = not self._paused
        
        # Update last_keys
        self._last = curr_keys


class Animation(object):
    """Instances are a subcontroller to animate an ellipse about a center.
    
    At each step, the update() method computes a new angle.  It finds the (x,y)
    coordinate that corresponds to the polar coordinate (ANIMATION_RADIUS,angle)
    and puts the ellipse there.
    
    INSTANCE ATTRIBUTES:
        _angle   [float]:     ellipse angle from center 
        _width   [float > 0]: the width of the window to animate in
        _height  [float > 0]: the height of the window to animate in
        _ellipse [GEllipse, center is (RADIUS,self.angle) in polar coords]: 
            the ellipse to animate
    
    NOTE: Attributes are hidden in this example, because we have more than one
    class.  The rule is that, when you have more than one class, the one class
    cannot access the hidden attributes or methods of another.
    """
    
    def __init__(self,width,height):
        """Initializer: Creates the animation subcontroller.
        
        Note that this is a proper initializer, because Animation is NOT a subclass
        of GameApp (we only want one Window).  However, it needs to know the width
        and height of the window, so we pass them as arguments.
        
        Parameter width: The window width
        Precondition: width is a float > 0
        
        Parameter height: The window height
        Precondition: height is a float > 0.
        """
        self._angle = 0
        self._width  = width
        self._height = height
        
        pos=self._polar_to_coord(ANIMATION_RADIUS,self._angle)
        self._ellipse = GEllipse(x=pos[0],y=pos[1],
                                 width=ELLIPSE_RADIUS,height=ELLIPSE_RADIUS,
                                 fillcolor=colormodel.RED)
    
    # Parallel methods to main controller
    def update(self):
        """Animates the ellipse."""
        # Change the angle
        self._angle = self._angle+ANIMATION_STEP % (2*math.pi)
        pos=self._polar_to_coord(ANIMATION_RADIUS,self._angle)
        self._ellipse.x = pos[0]
        self._ellipse.y = pos[1]
    
    def draw(self,view):
        """Draws the ellipse to the application window (view).
        
        Parameter: The view window
        Precondition: view is a GView."""
        self._ellipse.draw(view)
    
    
    # Helper methods
    def _polar_to_coord(self,r,a):
        """Returns: Tuple (x,y) equal to polar coord (r,a)
        
        Parameter r: The radius in polar coordinates
        Precondition: r is a float >= 0
        
        Parameter a: The angle in polar coordinates
        Precondition: a is a float
        """
        return (r*math.cos(a)+self._width/2.0,r*math.sin(a)+self._height/2.0)


# Application Code
if __name__ == '__main__':
    MainApp(width=WINDOW_WIDTH,height=WINDOW_HEIGHT,fps=60.0).run()
