#mgld
import pygame,os,random

amm=200 #ilość obiektów
background_colour = (12, 182, 204) # background_colour
width, height = 1200, 600 # Screen size

# #setting screen on second monitor
# mx = 2600
# my = 50
# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (mx,my)

screen = pygame.display.set_mode((width, height)) #Setting Screen
screen.fill(background_colour)#Fills white to screen
clock = pygame.time.Clock()

# object
class obj(pygame.sprite.Sprite):

    def __init__(self, startpos, velocity, startdir):
        super().__init__()
        self.pos = pygame.math.Vector2(startpos)
        self.velocity = velocity
        self.minvel=self.velocity
        self.dir = pygame.math.Vector2(startdir).normalize()
        self.id=random.randrange(0,3)
        self.image = pygame.image.load("{}\\{}.png".format(os.path.dirname(__file__),['rck','prp','scr'][self.id])).convert_alpha()
        self.rect = self.image.get_rect(center = (round(self.pos.x), round(self.pos.y)))

    def reflect(self, NV):
        self.dir = self.dir.reflect(pygame.math.Vector2(NV))

    def update(self):
        self.pos += self.dir * self.velocity
        self.rect.center = round(self.pos.x), round(self.pos.y)
        self.velocity*=0.7
        self.velocity=max(self.minvel,self.velocity)
        self.dir.rotate_ip(random.randrange(-10,10))

    def chc(self,gr):
        for i in gr:
            if pygame.sprite.collide_rect(self, i):
                if self.id==0 and i.id==1:self.id=1
                elif self.id==1 and i.id==2:self.id=2
                elif self.id==2 and i.id==0:self.id=0
                self.dir*=-1
                self.velocity*=2
                self.image = pygame.image.load("{}\\{}.png".format(os.path.dirname(__file__),['rck','prp','scr'][self.id])).convert_alpha()                
                self.rect = self.image.get_rect(center = (round(self.pos.x), round(self.pos.y)))

all_groups = pygame.sprite.Group()
for i in range(amm):
    all_groups.add(obj((random.randrange(11,width-10),random.randrange(11,height-10)), random.randrange(1,4), (random.random(), random.random())))

running = True

while running:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    all_groups.update()

    for i in all_groups:
        if i.rect.left <= 0:
            i.reflect((1, 0))
            i.pos.x=10
        if i.rect.right >= width:
            i.reflect((-1, 0))
            i.pos.x=width-10
        if i.rect.top <= 0:
            i.reflect((0, 1))
            i.pos.y=10
        if i.rect.bottom >= height:
            i.reflect((0, -1))
            i.pos.y=height-10
        gr=[j for j in all_groups if j!=i]
        i.chc(gr)
    
    screen.fill(background_colour)
    all_groups.draw(screen)
    pygame.display.flip()        
    pygame.time.wait(5)    

pygame.quit()
exit()