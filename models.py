# models.py
# Rui Chen and rc687, Tian Tan and tt474
# 12/8/2015
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self,x,y,width,height,linecolor,fillcolor):
        """**Constructor**: creates a new solid Paddle.
        
        parameter x: initial x value
        **Precondition**: x is an int or float.
        :param y: initial y value
        **Precondition**: y is an int or float.
        :param width: initial width value
        **Precondition**: width is an int or float.
        :param height: initial height value
        **Precondition**: height is an int or float.
        :param linecolor: initial linecolor value
        **Precondition**: linecolor is an instance of colormodel.
        :param fillcolor: initial fillcolor value
        **Precondition**: fillcolor is an instance of colormodel.   
        """
        GRectangle.__init__(self,x=x,y=y ,width=width,height=height,linecolor=linecolor,fillcolor=fillcolor)
           
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def collides(self,ball ):
        """Returns: True if the ball collides with this paddle
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        assert isinstance (ball, Ball)
        Truth=False
        if (not self.contains(ball.x+0.5*BALL_DIAMETER,ball.y+0.5*BALL_DIAMETER) and
            not self.contains(ball.x-0.5*BALL_DIAMETER,ball.y+0.5*BALL_DIAMETER)):

           if self.contains(ball.x+0.5*BALL_DIAMETER,ball.y-0.5*BALL_DIAMETER):
              Truth=True
           if self.contains(ball.x-0.5*BALL_DIAMETER,ball.y-0.5*BALL_DIAMETER):
              Truth=True
        return Truth
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY 
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
        
    # INITIALIZER TO CREATE A BRICK
    def __init__(self,x,y,width,height,linecolor,fillcolor):
        """**Constructor**: creates a new solid Brick.
        
        parameter x: initial x value
        **Precondition**: x is an int or float.
        :param y: initial y value
        **Precondition**: y is an int or float.
        :param width: initial width value
        **Precondition**: width is an int or float.
        :param height: initial height value
        **Precondition**: height is an int or float.
        :param linecolor: initial linecolor value
        **Precondition**: linecolor is an instance of colormodel.
        :param fillcolor: initial fillcolor value
        **Precondition**: fillcolor is an instance of colormodel.   
        """
        GRectangle.__init__(self,x=x,y=y ,width=width,height=height,linecolor=linecolor,fillcolor=fillcolor)
           
    # METHOD TO CHECK FOR COLLISION
    def collides(self,ball):
        """Returns: True if the ball collides with this brick
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        assert isinstance( ball, Ball)
        xr=ball.x+BALL_DIAMETER/2.0
        xl=ball.x-BALL_DIAMETER/2.0
        yt=ball.y+BALL_DIAMETER/2.0
        yb=ball.y-BALL_DIAMETER/2.0
        fact= self.contains(xr,yt) or self.contains(xr,yb) or self.contains(xl,yt) or self.contains(xl,yb)
        
        return fact
    
        # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
        
        
class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVx(self):
        """ return the velocity of x direction of the ball"""
        return self._vx
    
    def getVy(self ):
        """return the velocity of y direction of the ball"""
        return self._vy
    
    # INITIALIZER TO SET RANDOM VELOCITY, cited from game2d.py
    def __init__(self,x,y,diameter,fillcolor):
        """**Constructor**: creates a new solid ball.
        
        parameter x: initial x value
        **Precondition**: x is an int or float.
        :param y: initial y value
        **Precondition**: y is an int or float.
        :param diameter: initial diameter value
        **Precondition**: diameter is an int or float.
        :param linecolor: initial linecolor value
        **Precondition**: linecolor is an instance of colormodel.
        :param fillcolor: initial fillcolor value
        **Precondition**: fillcolor is an instance of colormodel.   
        """
        self._vx=random.uniform(1.0,5.0)
        self._vx=self._vx*random.choice([-1,1])
        self._vy=-5.0
        GEllipse.__init__(self,x=x,y=y,width=diameter,height=diameter,fillcolor=fillcolor)
    
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def change_Xdirection(self):
       """it changes the x direction of the velocity
       
       this method changes the direction x of the ball's moving to completely opposite
       by multiplying factor (-1)
       """
       self._vx=(-1)*self._vx
         
    def change_Ydirection(self):
       """it changes the y direciton of the velocity
       
       this method changes the direction y of the ball's moving to completely opposite
       by multiplying factor (-1)
       """
       self._vy=(-1)*self._vy
    

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE