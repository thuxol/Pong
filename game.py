import pygame
from pygame.locals import *
import pygame.freetype
import random

class Ball(pygame.Rect):
    width = 15
    height = 15
    COLOR = (255,255,255)
    lastcollide = -1
    maxspeed = 5
    def __init__ (self, v_x, v_y, x,y):
        self.v_x = v_x
        self.v_y = v_y
        self.fx = float(x)
        self.fy = float(y)

        super().__init__([x,y,self.width,self.height])
    
    def draw (self, surface):
        pygame.draw.ellipse(surface, self.COLOR, [self.fx,self.fy,self.width,self.height])
    
    def move(self, board_width, board_height, paddles):
        
       if( not 0 < self.fy + self.v_y < board_height):
           self.v_y = -self.v_y  
                      
       self.fx += self.v_x
       self.fy += self.v_y
       self.x = self.fx
       self.y = self.fy
       
       #check paddle collision
       for paddle in paddles:
           if self.colliderect(paddle) and self.lastcollide != paddle.id:
               self.v_x = min(1.1 * (- self.v_x),self.maxspeed)
               self.v_y = min(1.1 * self.v_y, self.maxspeed)
               self.lastcollide = paddle.id
               continue
       
       if( self.fx < 0):
           return -1
       if (self.fx > board_width):
           return 1
       
       return 0
    
        
class Paddle(pygame.Rect):
    width = 15
    height = 80
    COLOR = (255,255,0)
    ai_move = None
    def __init__(self, v, up_key, down_key, x, y, id, ai_move = None):
        self.v = v
        self.up_key = up_key
        self.down_key = down_key
        self.fx = float(x)
        self.fy = float(y)
        self.id = id
        self.ai_move = ai_move
        super().__init__([x,y,self.width,self.height])
    
    def draw (self, surface):
        pygame.draw.rect(surface, self.COLOR, [self.fx,self.fy,self.width,self.height])

 
    def move (self, board_height, gamestate=None):
        down, up = False, False
        diff = 0
        
        if self.ai_move:
            down, up = self.ai_move(gamestate, self.id)
        else:
            keys = pygame.key.get_pressed()
            down, up = keys[self.down_key], keys[self.up_key]
        if up:
            diff = - self.v
        elif down:
            diff = self.v
        
        if 0 < self.fy + diff < board_height - self.height:
            self.fy += diff
        
        self.y = self.fy

class AI():
    #stupid AI: just follows the ball -> go up if ball.y < paddle.y
    def tracking(self, game, id):
        if game.balls[0].y < game.paddles[id].y:
            return (False, True)
        elif game.balls[0].y > game.paddles[id].y:
            return (True, False)
        
        return (False, False)
        

class Pong():
    HEIGHT = 600
    WIDTH = 800
    BACKGROUND_COLOR = (0,0,0)
    running = True
    score = 0
    def __init__(self):
        pygame.init()  
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        
        up_keys = [K_UP, K_w]
        down_keys = [K_DOWN, K_s]
        x_positions = [10, self.WIDTH - Paddle.width-10]
        y_positions = [self.HEIGHT/2 - Paddle.height/2] * 2
        
        
        self.paddles = [ Paddle(
                1,
                up_keys[i],
                down_keys[i],
                x_positions[i],
                y_positions[i],
                i)
                for i in range(2)]
        
        ai = AI()
        self.paddles[0].ai_move = ai.tracking
    
        self.balls = [ Ball(random.uniform(0.15,0.35),
                            random.uniform(0.15,0.35),
                            self.WIDTH/2 - Ball.width/2,
                            self.HEIGHT/2 - Ball.height/2)
                     ]
        
        self.GAME_FONT = pygame.freetype.SysFont('Consolas',24)
        
    def drawscore(self):
        self.GAME_FONT.render_to(self.screen, (50,50), str(self.score), (50,80,0))
    
    def reset(self):
        self.__init__()
    
    def game_loop(self):
        while(self.running):
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                elif event.type == QUIT:
                    self.running = False
            self.screen.fill(self.BACKGROUND_COLOR)
            
            for paddle in self.paddles:
                paddle.draw (self.screen)
                paddle.move(self.HEIGHT, self)
            
            for ball in self.balls:
                ball.draw (self.screen)
                scoreupdate = ball.move(self.WIDTH, self.HEIGHT, self.paddles) 
                if (scoreupdate != 0):
                    self.score += scoreupdate
                    self.reset()
                    continue
            
            self.drawscore()
            pygame.display.flip()
        
        self.clock.tick(60)
        
        pygame.quit()



if __name__ == '__main__':
    pong = Pong()
    pong.game_loop()        
