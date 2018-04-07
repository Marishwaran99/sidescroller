import pygame,random,time
pygame.init()
black=(0,0,0)
red=(255,0,0)
white=(255,255,255)
yellow=(255,255,0)
green=(0,255,0)
yellow=(255,255,0)
blue=(0,0,255)
purple=(255,0,255)
light_blue=(0,255,255)
dh=447
dw=600
pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode([dw,dh])
pygame.display.set_caption("side scroller game")
clock=pygame.time.Clock()
bg=pygame.image.load('bg.png')
bw,bh=bg.get_rect().size
sw=bw
vec=pygame.math.Vector2
rpimg=[pygame.image.load(str(i)+'.png').convert_alpha() for i in range(8,16)]
jpimg=[pygame.image.load(str(i)+'.png').convert_alpha() for i in range(1,8)]
sawimg=[pygame.image.load("saw"+str(i)+'.png').convert_alpha() for i in range(4)]
class Player(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.game=game
        self.image=rpimg[0]
        self.rect=self.image.get_rect()
        self.rect.x=200
        self.rect.y=dh-200
        self.vel=vec(0,0)
        self.acc=vec(0,0)
        self.pos=vec(self.rect.x,self.rect.y)
        self.ri=0
        self.si=0
        self.ji=0
        self.jh=20
        self.jump=0
        self.running=1
    def update(self):
        self.acc=vec(0,0.1)
        keys=pygame.key.get_pressed()
        if self.pos.y<dh-130:
            if self.ji+1<108:
                self.image=jpimg[self.ji//18]
                self.ji+=1
            else:
                self.ji=0
            self.jump=0
            self.running=0
        elif self.pos.y==dh-130:
            self.jump=1
            self.running=1
            if keys[pygame.K_SPACE] and self.jump==1:
                self.vel.y=-6               
                self.running=0
        else:
            self.running=1
        self.vel+=self.acc
        self.pos+=self.vel+0.5*self.acc
        if self.pos.y>dh-130:
            self.pos.y=dh-130
        self.rect.x,self.rect.y=self.pos.x,self.pos.y
        if self.running:
           self.run()
        self.mask=pygame.mask.from_surface(self.image)
    def run(self):       
        if self.ri+1>42:
           self.ri=0           
        else:
           self.image=rpimg[self.ri//6]
           self.ri+=1
class Obstacles(pygame.sprite.Sprite):
   def __init__(self,x,y):
      super().__init__()
      self.image=sawimg[0]
      self.rect=self.image.get_rect()
      self.rect.x=x
      self.rect.y=y
      self.i=0
      self.vx=-2
   def update(self):
      if self.i+1<12:
         self.image=sawimg[self.i//3]
         self.i+=1
      else:
         self.i=0
      self.rect.x+=self.vx
      self.mask=pygame.mask.from_surface(self.image)
class Game:
    def __init__(self):
        self.score=0
    def saw(self):
        self.obs=pygame.sprite.Group()
        self.ob=Obstacles(700,253)
        self.obs.add(self.ob)
        self.all_sprites.add(self.ob)
    def new(self):
        self.all_sprites=pygame.sprite.Group()
        self.obs=pygame.sprite.Group()
        self.player=Player(self)
        self.ob=Obstacles(700,253)
        self.obs.add(self.ob)
        self.all_sprites.add(self.ob)
        self.all_sprites.add(self.player)
        self.bgx=0        
    def obsgenerate(self):
        if self.ob.rect.x<self.ob.rect.width:
            self.saw()
            self.score+=1
        elif self.collide():
            self.saw()
            self.score-=1
            
    def events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
    def collide(self):
        hits=pygame.sprite.spritecollide(self.player,self.obs,False,pygame.sprite.collide_mask)
        if hits:
            return 1
    def update(self):
        self.obsgenerate()
        self.all_sprites.update()
        relx=self.bgx%bw
        screen.blit(bg,(relx-bw,0))
        if relx<dw:
           screen.blit(bg,(relx,0))
        self.bgx-=2
    def msg(self,txt,color,size,x,y):
        self.font=pygame.font.SysFont("comicsansms",size,bold=1)
        msgtxt=self.font.render(txt,1,color)
        msgrect=msgtxt.get_rect()
        msgrect.x=x
        msgrect.y=y
        screen.blit(msgtxt,msgrect)
        
    def draw(self):
        
        self.all_sprites.draw(screen)
        self.msg('Score:'+str(self.score),blue,30,250,10)
        pygame.display.flip()
    def run(self):
        while 1:
            clock.tick(60)
            self.events()
            self.update()
            self.draw()
            pygame.display.flip()
g=Game()
while g.run:
    g.new()
    g.run()
