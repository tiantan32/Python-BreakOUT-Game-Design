# play.py
# Rui Chen and rc687, Tian Tan and tt474
# 12/8/2015
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
    
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getPaddle(self):
        """Return: the paddle to handle"""
        return self._paddle
    
    def getBricks(self):
        """Return: the list of the bricks remaining"""
        return self._bricks
    
    def getBall(self):
        """Return: the ball to play"""
        return self._ball
        
    def getTries(self):
        """Return: the life that the play has left"""
        return self._tries
    
    def getMusic(self):
        """Return: the sound of the bouncing and breaking"""
        return self._music
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """Initializer: to create paddle and bricks.
        
        This function creates a paddle and a 2 dimensional list of bricks. When they are created, they can be drawed
        by a draw method. Moreover, it also assign default values to music and tries attributes.
        """
        bricks_list=[]
        for row in range(BRICK_ROWS):
            color=(row if row<10 else row%10)
            for column in range(BRICKS_IN_ROW):
                b=Brick(BRICK_SEP_H/2.0+column*(BRICK_WIDTH+BRICK_SEP_H)+BRICK_WIDTH/2.0,
                                 GAME_HEIGHT-BRICK_Y_OFFSET-BRICK_HEIGHT/2.0-row*BRICK_HEIGHT-row*BRICK_SEP_V,
                                 BRICK_WIDTH, BRICK_HEIGHT, BRICK_COLOR[color], BRICK_COLOR[color])
                bricks_list+=[b]
        self._bricks=bricks_list
        self._paddle=Paddle(GAME_WIDTH/2.0,PADDLE_OFFSET,PADDLE_WIDTH,PADDLE_HEIGHT, colormodel.BLACK,colormodel.BLACK)
        self._tries=3
        self._music=None 
            
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self,inputkey):
        """animinate the paddle
        parameter inputkey: an indicator of keyboard information
        precondition: inputkey is an object of class GInput"""
        if inputkey.is_key_down('right'):
            self._paddle.x=min(self._paddle.x+PADDLE_V , GAME_WIDTH-PADDLE_WIDTH/2.0)
        if inputkey.is_key_down('left'):
            self._paddle.x=max(self._paddle.x-PADDLE_V, PADDLE_WIDTH/2.0)
            
    def updateBall(self):
        """This method animinate the ball
        
        checking the dynamic condition of the ball and animate it
        moving or hit the obstacle and change the direction of the ball"""
        self._ball.x=self._ball.x+self._ball.getVx()
        self._ball.y=self._ball.y+self._ball.getVy()
        state = None
        for b in self._bricks:
            if b.collides(self._ball):
                self._ball.change_Ydirection()
                self._bricks.remove(b)
                state = "brick"
        if self._paddle.collides(self._ball):
            self._ball.change_Ydirection()
            state = "paddle"
        if self._ball.x>=GAME_WIDTH-BALL_DIAMETER/2.0 or self._ball.x<=BALL_DIAMETER/2.0:
            self._ball.change_Xdirection()
        if self._ball.y>=GAME_HEIGHT-BALL_DIAMETER/2.0:
            self._ball.change_Ydirection()
        if self._ball.y<=BALL_DIAMETER/2.0:
            self._tries=self._tries-1
        return state
            
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def draw(self,view):
        """draw the paddle and bricks
        parameter view:the contents that this method is going to draw
        precondition: view is an object of class GameApp"""
        for brick in self._bricks:
            brick.draw(view)
        self._paddle.draw(view)
     
    def drawBall(self,view):
        """draw the ball
        parameter view: the contents that this method is going to draw
        precondition: view is an object of class GameApp"""
        if self.getBall() is not None:
            self.getBall().draw(view)
               
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def serveBall(self):
        """Initializer for ball: create a ball.
        
        This method provides the ball on the screen.
        """
        self._ball=Ball(0.5*GAME_WIDTH,0.5*GAME_WIDTH,
                        BALL_DIAMETER,colormodel.BLUE)