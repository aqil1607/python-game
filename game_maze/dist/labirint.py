from pygame import *

win_width = 700
win_height = 500
display.set_caption('Maze')
window = display.set_mode((win_width, win_height))
background = (119, 210,223)


class GameSprite(sprite.Sprite):
   #class constructor
   def __init__(self, player_image, player_x, player_y, size_x, size_y):
       # Calling the class constructor (Sprite):
       sprite.Sprite.__init__(self)
       # each sprite must store an image property
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
  
       # each sprite must store the rect property - the rectangle which it's inscribed in
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   # the method that draws the character in the window
   def show(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
   #the method where the sprite is controlled by the arrow keys of the keyboard
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
       # Calling the class constructor (Sprite):
       GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

       self.x_speed = player_x_speed
       self.y_speed = player_y_speed
    def update(self):
      ''' moves the character by applying the current horizontal and vertical speed '''
      #horizontal movement first
      if player.rect.x <= win_width-80 and player.x_speed > 0 or player.rect.x >= 0 and player.x_speed < 0:
        self.rect.x += self.x_speed
      #if we go behind the wall, we'll stand right up to it
      platforms_touched = sprite.spritecollide(self, walls, False)
      if self.x_speed > 0: #we're going to the right, the character's right edge appears right up to the left edge of the wall
          for p in platforms_touched:
              self.rect.right = min(self.rect.right, p.rect.left) #if several walls were touched at once, then the right edge is the minimum possible
      elif self.x_speed < 0: #we're going to the left, then put the character's left edge right up to the right edge of the wall
          for p in platforms_touched:
              self.rect.left = max(self.rect.left, p.rect.right) #if several walls have been touched, then the left edge is the maximum
      if player.rect.y <= win_height-80 and player.y_speed > 0 or player.rect.y >= 0 and player.y_speed < 0:
       self.rect.y += self.y_speed
      #if we go behind the wall, we'll stand right up to it
      platforms_touched = sprite.spritecollide(self, walls, False)
      if self.y_speed > 0: # going down
          for p in platforms_touched:
              #We're checking which of the platforms is the highest from the ones below, aligning with it, and then take it as our support:
              self.rect.bottom = min(self.rect.bottom, p.rect.top)
      elif self.y_speed < 0: #going up
          for p in platforms_touched:
              self.rect.top = max(self.rect.top, p.rect.bottom) #aligning the upper edge along the lower edges of the walls that were touched
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15 )
        bullets.add(bullet)
        
        
# the bullet sprite's class  
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
    # Calling the class constructor (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
 #movement of an enemy
    def update(self):
        self.rect.x += self.speed
     # disappears after reaching the edge of the screen
        if self.rect.x > win_width+10:
            self.kill()
    
    
# the enemy sprite class   
class Enemy(GameSprite):
 side = "left"
 def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
     # Calling the class constructor (Sprite):
     GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
     self.speed = player_speed


  #movement of an enemy
 def update(self):
     if self.rect.x <= 420: #w1.wall_x + w1.wall_width
         self.side = "right"
     if self.rect.x >= win_width - 85:
         self.side = "left"
     if self.side == "left":
         self.rect.x -= self.speed
     else:
         self.rect.x += self.speed

walls = sprite.Group()

bullets = sprite.Group()

enemies = sprite.Group()

w1 = GameSprite('wall.png',117,  250,  300,  50)
w2 = GameSprite('wall.png', 370, 100, 50, 400)

walls.add(w1,w2)



player = Player('superhero.png', 5, win_height - 80, 80, 80, 0, 0)
monster1 = Enemy('avatar.png', win_width - 80, 180, 80, 80, 10)
monster2 = Enemy('avatar.png', win_width - 80, 300, 80, 80, 10)
final_sprite = GameSprite('dinosaur.png', win_width - 85, win_height - 100, 80, 80)
enemies.add(monster1,monster2)

finish = False
run = True
while run:
    time.delay(50)
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
           if e.key == K_LEFT:
               player.x_speed = -10
           elif e.key == K_RIGHT:
               player.x_speed = 10
           elif e.key == K_UP:
               player.y_speed = -10
           elif e.key == K_DOWN:
               player.y_speed = 10
           elif e.key == K_SPACE:
               player.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT: 
                player.x_speed = 0
            elif e.key == K_RIGHT:
                player.x_speed = 0
            elif e.key == K_UP:
                player.y_speed = 0
            elif e.key == K_DOWN:
                player.y_speed = 0
            
                
    if not finish:
        window.fill(background)
        player.show()
        player.update()
        walls.draw(window)
        final_sprite.show()
        bullets.update()
        bullets.draw(window)
        sprite.groupcollide(bullets,walls, True,False)
        enemies.update()
        enemies.draw(window)
        sprite.groupcollide(enemies, bullets, True, True)
        
        
        if sprite.spritecollide(player, enemies, True):
            finish = True
            #calculate the ratio
            img = image.load('gameover.jpg')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))
            

        if sprite.collide_rect(player, final_sprite):
            finish = True
            img = image.load('victory.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
            
        
                
    display.update()