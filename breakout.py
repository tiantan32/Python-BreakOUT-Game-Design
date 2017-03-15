# breakout.py
# Rui Chen rc687 and Tian Tan tt474
# 12/8/2015
"""Primary module for Breakout application

This module contains the main controller class for the Breakout application. There is no
need for any any need for additional classes in this module.  If you need more classes, 
99% of the time they belong in either the play module or the models module. If you 
are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from game2d import *
from play import *


# PRIMARY RULE: Breakout can only access attributes in play.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
                the current state of the game represented a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle, ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or STATE_COUNTDOWN.
    
    For a complete description of how the states work, see the specification for the
    method update().
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    Additional ATTRIBUTES:
         _frames  [integer>=0]:
                  the number of frames that have elapsed since the state was switched
                  to STATE_COUNTDOWN
        last_key  [integer>=0]:
                  the number of keys detected at the last frame.
        _mssg2    [GLabel, or None if there is no message to dispay]
                  the current score that the play hit
        _mssg3    [GLabel,or None if there is no message to display]
        _music1   [Sound, or None if there is no music to display]
                  the sound was played when hit the paddle
        _music2   [Sound, or None if there is no music to display]
                  the sound was played when hit the bricks
    Additional INVARIANTS:
        _mssg2 is only None if _state is STATE_INACTIVE
        _mssg3 is only not None if _state is STATE_COMPLETE
    
    """
    
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _mssg) saying that the user should press to play a game."""
        # IMPLEMENT ME
        self._state=STATE_INACTIVE
        self._game=None
        self._mssg=GLabel(text='Welcome and Press Any Key to Play',
                          x=GAME_WIDTH/2.0, y=GAME_HEIGHT/2.0,font_name='Zapfino.ttf')
        self._frames=0
        self.last_key=0
        self._mssg2=None
        self._mssg3=None
        self._music1=Sound('bounce.wav')
        self._music2=Sound('cup1.wav')
        
    def update(self,dt):
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Play.  The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Play object _game to play the game.
        
        As part of the assignment, you are allowed to add your own states.  However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWGAME,
        STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does its own
        thing, and so should have its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows it on the screen.  
        This state only lasts one animation frame before switching to STATE_COUNTDOWN.
        
        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is 
        served.  The player can move the paddle during the countdown, but there is no
        ball on the screen.  Paddle movement is handled by the Play object.  Hence the
        Play class should have a method called updatePaddle()
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).  Hence
        the Play class should have methods named updatePaddle() and updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so long
        as the player never presses a key.  In addition, the application switches to 
        this state if the previous state was STATE_ACTIVE and the game is over 
        (e.g. all balls are lost or no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent 3
        seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are still
        some tries remaining.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # IMPLEMENT ME
        assert type(dt)==int or type(dt)==float
        if self._state==STATE_INACTIVE:
            self._determineState()
            if self._state==STATE_NEWGAME:
               self.draw()
        elif self._state==STATE_NEWGAME:
            self._game=Play()
            self.messagePlay()
            self._state=STATE_COUNTDOWN
        elif self._state==STATE_COUNTDOWN:
            self.messagePlay()
            self._game.updatePaddle(self.input)
            self._frames+=1
            if self._frames%180==0:
               self._game.serveBall()
               self._state=STATE_ACTIVE
        elif self._state==STATE_ACTIVE:
            self._game.updatePaddle(self.input)
            self.messagePlay()
            old_tries=self._game.getTries()
            state = self._game.updateBall()
            if state == "brick":
                self._music2.play()
            if state == "paddle":
                self._music1.play()
            if len(self._game.getBricks())==0:
                self._state=STATE_COMPLETE
            elif old_tries!=self._game.getTries():
                self._state=(STATE_PAUSED if self._game.getTries()>0 else STATE_COMPLETE)
        elif self._state==STATE_PAUSED:
            self.messagePlay()
            self._determineState()
        elif self._state==STATE_COMPLETE:
            if len(self._game.getBricks())==0:
               self._mssg=GLabel(text='LOL YOU WIN',x=GAME_WIDTH/2.0,
                                 y=GAME_HEIGHT/2.0,font_name='Zapfino.ttf')
               self._mssg2=None
            else:
               self._mssg=GLabel(text='Game Over '+'YOU HAVE '+str(len
                                (self._game.getBricks()))+' BRICKS REMAINING'
                                 ,x=GAME_WIDTH/2.0, y=GAME_HEIGHT/2.0)
            self.messagePlay()
            
        # Process the states.  Send to helper methods
        
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play. 
        In order to draw them, you either need to add getters for these attributes or you 
        need to add a draw method to class Play.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        # IMPLEMENT ME
        if self._mssg is not None:
            self._mssg.draw(self.view)
        if not self._game is None: 
            self._game.draw(self.view)
        if self._state==STATE_ACTIVE:    
            self._game.drawBall(self.view)
        if self._mssg2 is not None:
            self._mssg2.draw(self.view)
        if self._mssg3 is not None:
            self._mssg3.draw(self.view)
             
    # HELPER METHODS FOR THE STATES GO HERE
    #cited from states.py from course website.
    def _determineState(self):
        """Determines the current state and assigns it to self.state
        
        This method checks for a key press, and if there is one, changes the state 
        to the next value.  A key press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as we hold down the key.  The
        user must release the key and press it again to change the state."""
        curr_keys = self.input.key_count
        # Only change if we have just pressed the keys this animation frame
        change=curr_keys >0 and self.last_keys==0
        if change:
            # Click happened.  Change the state
            if self._state==STATE_INACTIVE:
                self._state = STATE_NEWGAME
            if self._state==STATE_PAUSED:
                self._state=STATE_COUNTDOWN
            self._mssg= None
        self.last_keys=curr_keys
        
    def messagePlay(self):
        """ play the message that is wanted on the screen
        
        this method checks for a state to play proper message
        as message changes by time.
        For example. When the state switch to STATE_NEWGAME,
        the we want' Remaining Bricks (number) 'to display
        """
        if self._state==STATE_NEWGAME:
            self._mssg2=GLabel(text='Remaining Bricks '+str
                               (len(self._game.getBricks())), x=GAME_WIDTH/2.0,
                y=GAME_HEIGHT-BRICK_Y_OFFSET/2.0,font_name='Zapfino.ttf')
        if self._state==STATE_COUNTDOWN:
            self._mssg==None
        if self._state==STATE_ACTIVE:
            self._mssg2=GLabel(text='Remaining Bricks '+str
                               (len(self._game.getBricks())), x=GAME_WIDTH/2.0,
                               y=GAME_HEIGHT-BRICK_Y_OFFSET/2.0,font_name='Zapfino.ttf')   
        if self._state==STATE_PAUSED:
            self._mssg=GLabel(text='Press Any Key to get a new ball, you have '+
                              str(self._game.getTries())+' chance'
                              ,x=GAME_WIDTH/2.0, y=GAME_HEIGHT/2.0,font_name='Zapfino.ttf')
        if self._state==STATE_COMPLETE:
            self._mssg3=GLabel(text='Thank you for the whole semester',
                               x=GAME_WIDTH*0.5, y=GAME_HEIGHT*0.25,
                               font_name='Zapfino.ttf')
    
            
    
            