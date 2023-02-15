import pygame
from random import randint

pygame.init()

WIDTH, HEIGHT = 750, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders By Aashakt")
icon = pygame.image.load("SpaceInvaderIcon.ico")
pygame.display.set_icon(icon)

RocketImg = pygame.image.load("C:\MyFolder\PythonProgramming\SpaceInvaders\Images\Rocket.png")
RocketImg = pygame.transform.scale(RocketImg, (50, 50))

AlienImg = pygame.image.load("C:\MyFolder\PythonProgramming\SpaceInvaders\Images\Alien.png")
AlienImg = pygame.transform.scale(AlienImg, (50, 50))

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.rect = [self.x, self.y, 2, 15]
        self.speed = 4
        self.direction = direction

    def Draw(self):
        pygame.draw.rect(WIN, (255, 255, 255), self.rect)  

    def Movement(self):
        self.rect[1] += (self.speed * self.direction) 

    def Update(self):
        self.Movement()
        self.Draw()          

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = [self.x, self.y, 50, 50]
        self.speed = 4
        self.BulletList = []

    def Draw(self):
        WIN.blit(RocketImg, (self.rect[0], self.rect[1]))  

    def Movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.rect[0] <= WIDTH-50:
            self.rect[0] += self.speed
        elif keys[pygame.K_a] and self.rect[0] >= 0:
            self.rect[0] -= self.speed    

    def Shoot(self):
        bullet = Bullet(self.rect[0]+25, self.rect[1], -1)
        if len(self.BulletList) < 1:
            self.BulletList.append(bullet)

    def Update(self):
        self.Movement()
        for b in self.BulletList:
            b.Update()
            if b.rect[1] <= 0:
                self.BulletList.remove(b)
        self.Draw()   

class Alien:
    def __init__(self, x, y, posOffset):
        self.x = x
        self.y = y
        self.rect = [self.x, self.y, 38, 29]
        self.BulletList = []
        self.direction = 1
        self.pOff = posOffset

    def Draw(self):
        WIN.blit(AlienImg, (self.rect[0]-5, self.rect[1]-11))    

    def Movement(self):
        self.rect[0] += 0.5 * self.direction
        if self.rect[0] >= WIDTH - (38*self.pOff[0]+self.pOff[0]*5):
            self.direction = -1
            self.rect[1] += 10
        if self.rect[0] <= (38*self.pOff[1]+self.pOff[1]*5):
            self.direction = 1  
            self.rect[1] += 10 

    def Shoot(self):
        ShootRandom = randint(0, 1000)
        if ShootRandom > 999:
            bullet = Bullet(self.rect[0]+19, self.rect[1]+29, 1)
            self.BulletList.append(bullet)

    def Update(self):
        self.Movement()
        self.Shoot()
        for b in self.BulletList:
            b.Update()
            if b.rect[1] >= 490:
                self.BulletList.remove(b)
        self.Draw()

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.BoxList = []
        self.BoxList = self.getList()

    def getList(self):
        for i in range(5):
            for j in range(5):
                Box = pygame.draw.rect(WIN, (0, 255, 0), [j*10+self.x,i*10+self.y,10,10])
                self.BoxList.append(Box)
        return self.BoxList    

    def Update(self):
        for Box in self.BoxList:
            pygame.draw.rect(WIN, (0,255,0), [Box.x, Box.y, 10, 10])            

def Text(msg, pos):
    font = pygame.font.SysFont("Aerial", 40)
    text = font.render(msg, True, (255, 255, 255))
    WIN.blit(text, pos)

def MenuScreen():
    run1 = True
    Bcolor = (255,255,255)
    while run1:
        mouse = pygame.mouse.get_pos()
        Text("Space Invaders", (270, 20))
        pygame.draw.rect(WIN, Bcolor, [320, 220, 100, 50], 2, 10)
        Text("Play", (340, 232))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run1 = False
                pygame.quit()
                quit()
        if 320 < mouse[0] < 420:
            if 220 < mouse[1] < 270:
                Bcolor = (195, 195, 195)
                if pygame.mouse.get_pressed()[0]:
                    run1 = False
                    WIN.fill((0,0,0))
                    Main() 
            else:       
                Bcolor = (255,255,255)            
        pygame.display.update() 

def Main():
    run = True
    clock = pygame.time.Clock()
    FPS = 60

    AlienList = []
    ObstacleList = []

    player = Player(225, 425)

    for i in range(1, 6):
        obstacle = Obstacle(i*120, 325)
        ObstacleList.append(obstacle)

    Lives = 10
    Score = 0

    for i in range(5):
        for j in range(12):
            alien = Alien(j*38+j*5, i*29+i*10, [12-j, j])
            AlienList.append(alien)

    while run:
        WIN.fill((0, 0, 0))
        Text(f"Lives: {Lives}", (20, 460))
        Text(f"Score: {Score}", (WIDTH-150, 460))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.Shoot() 

        for a in AlienList:
            for b in a.BulletList:
                if pygame.draw.rect(WIN,(0,0,0),player.rect).colliderect(b):
                    Lives -= 1
                    a.BulletList.remove(b)
        player.Update()
        for a in AlienList: 
            for b in player.BulletList:
                if pygame.draw.rect(WIN,(0, 0, 0),a.rect).colliderect(b):
                    player.BulletList.remove(b)
                    AlienList.remove(a)
                    Score += 1
            a.Update()
        for ob in ObstacleList:
            for o in ob.BoxList:
                for b in player.BulletList:
                    if pygame.draw.rect(WIN,(0,0,0),[o.x,o.y,10,10]).colliderect(b):
                        player.BulletList.remove(b)
                        ob.BoxList.remove(o)
        for ob in ObstacleList:                
            for o in ob.BoxList:
                for a in AlienList:
                    for b in a.BulletList:
                        if pygame.draw.rect(WIN,(0,0,0),[o.x,o.y,10,10]).colliderect(b):
                            a.BulletList.remove(b)
                            ob.BoxList.remove(o)              
        if Lives <= 0:
            run = False 
            WIN.fill((0, 0, 0))  
            GameOverScreen()
        if Score >= 60:
            run = False
            WIN.fill((0,0,0))
            GameWonScreen()    
        for o in ObstacleList:
            o.Update()  
        pygame.display.update()
        clock.tick(FPS)

def GameOverScreen():
    run1 = True
    while run1:
        Text("Game Over", (320, 220))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run1 = False
                pygame.quit()
                quit()
        pygame.display.update() 

def GameWonScreen():
    run2 = True
    while run2:
        Text("You Won", (320, 220))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run2 = False
                pygame.quit()
                quit()
        pygame.display.update()

MenuScreen()   
