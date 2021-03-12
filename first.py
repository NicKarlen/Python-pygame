#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division
import pygame
import math
 
# Initialize Pygame.
pygame.init()
# Set size of pygame window.
X_background_Size = 1000
Y_background_Size = 900
screen=pygame.display.set_mode((X_background_Size,Y_background_Size))
# Create empty pygame surface.
background = pygame.Surface(screen.get_size())
# Fill the background white color.
background.fill((255, 255, 255))
# Convert Surface object to make blitting faster.
background = background.convert()
# Copy background to screen (position (0, 0) is upper left corner).
screen.blit(background, (0,0))
# Create Pygame clock object.  
clock = pygame.time.Clock()

# Score
hits = 0
Font = pygame.font.SysFont('Comic Sans MS', 30)

# List of Shot instances/objects and the number
NumberOfShots = 0
shotList = []


#----------------------------------------------------------Classes---------------------------------------------------------------

class Character:
    def __init__(self,size=None,colorSurface=None,colorCircle=None, StartingPos=None, StartingDirection=None):
        # Create a new surface
        if size is None:
            self.size = (50,50)
            self.CharacterSurface = pygame.Surface(self.size) 
        else:
            self.size = size
            self.CharacterSurface = pygame.Surface(self.size)

        # Color the surface
        if colorSurface is None:
            self.CharacterSurface.fill((255, 255, 255)) 
        else:
            self.CharacterSurface.fill((colorSurface))

        # Draw a circle on top of the surface
        if colorCircle is None:
            pygame.draw.circle(self.CharacterSurface, (0,0,0), (self.size[0]/2,self.size[1]/2),self.size[0]/2) 
        else:
            pygame.draw.circle(self.CharacterSurface, colorCircle, (self.size[0]/2,self.size[1]/2),self.size[0]/2) 

        # Convert the surface so it's easier displayed
        self.CharacterSurface.convert()

        if StartingPos is None:
            self.Pos = [100,100]
        else:
            self.Pos = []
            self.Pos.append(StartingPos[0])
            self.Pos.append(StartingPos[1])

        if StartingDirection is None:
            self.Direction = [1,1]
        else:
            self.Direction = []
            self.Direction.append(StartingDirection[0])
            self.Direction.append(StartingDirection[1])


class Shot:
    def __init__(self,StartingPos, Direction, HittingPlayer, Color):
        self.HittingPlayer = HittingPlayer
        self.edgeLength = 20
        self.ActualPos = list(StartingPos)
        self.Direction = list(Direction)
        self.noShow = False

        self.shotSurface = pygame.Surface((self.edgeLength,self.edgeLength)) # Create a new surface
        self.shotSurface.fill((255, 255, 255)) # Color the surface
        pygame.draw.circle(self.shotSurface, Color, (self.edgeLength/2,self.edgeLength/2),self.edgeLength/2) # Draw a circle on top of the surface
        self.shotSurface.convert() # Convert the surface so it's easier displayed
    
    # calc new position
    def newPosCalc(self, Speed):
        self.ActualPos[0] += self.Direction[0]*Speed
        self.ActualPos[1] += self.Direction[1]*Speed

    # Methode to check for a collision with self and other object
    def checkCollision(self,X2Pos,Y2Pos,Width2,Hight2):
        if self.ActualPos[0] + self.edgeLength > X2Pos and self.ActualPos[0] < X2Pos + Width2 and self.ActualPos[1] + self.edgeLength > Y2Pos and self.ActualPos[1] < Y2Pos + Hight2: #Collision
            return True
        return False

#-----------------------------------------------------------Functions------------------------------------------------------------


#def checkCollision (X1Pos,X2Pos,Y1Pos,Y2Pos,Width1,Width2,Hight1,Hight2):
#    if X1Pos + Width1 > X2Pos and X1Pos < X2Pos + Width2 and Y1Pos + Hight1 > Y2Pos and Y1Pos < Y2Pos + Hight2: #Collision
#        return True
#    return False

def getShotdirection(PlayerX,PlayerY,MousePosX,MousePosY):
    ShotDirectionX = MousePosX - PlayerX
    ShotDirectionY = MousePosY - PlayerY

    return (ShotDirectionX*(1/math.sqrt(ShotDirectionX**2+ShotDirectionY**2)),ShotDirectionY*(1/math.sqrt(ShotDirectionX**2+ShotDirectionY**2)))


#-----------------------------------------------------------MainLoop-------------------------------------------------------------
      
mainloop = True
# Desired framerate in frames per second. Try out other values.              
FPS = 30
# How many seconds the "game" is played.
playtime = 0.0

time = 0 #Time to release shot from enemy

GameOver = None

# Creat Instance of Character Class
Player = Character(StartingPos=(400,400))
Enemy = Character(size=(80,80),colorSurface=(255,255,255),colorCircle=(125,200,50),StartingPos=(600,600), StartingDirection=(1,1))

while mainloop:
    # Do not go faster than this framerate.
    milliseconds = clock.tick(FPS) 
    playtime += milliseconds / 1000.0 

    # Damit die Geschwindigkeit immer gleich ist
    Speed = round(milliseconds/7)

    # shot fired
    aiming_pos = (0,0) 
    EnemyShotFired = False  

    # Print background
    screen.blit(background, (0,0))

    # Key Events
    for event in pygame.event.get():
        # User presses QUIT-button.
        if event.type == pygame.QUIT:
            mainloop = False 
        elif event.type == pygame.KEYDOWN:
            # User presses ESCAPE-Key
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            if event.key == pygame.K_SPACE:
                print('space')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed() == (True,False,False):
                aiming_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed() == (False,False,True):
                print('rechts')



    # Schaut welche Keys das gedrückt sind, im for loop vom event wir nur 1 event getriggert beim dücken...
    PressedKey = pygame.key.get_pressed()
    if PressedKey[pygame.K_s] or PressedKey[pygame.K_DOWN] :
        Player.Pos[1] = Player.Pos[1] + Speed
    if PressedKey[pygame.K_w] or PressedKey[pygame.K_UP]:
        Player.Pos[1] = Player.Pos[1] - Speed
    if PressedKey[pygame.K_a] or PressedKey[pygame.K_LEFT]:
        Player.Pos[0] = Player.Pos[0] - Speed
    if PressedKey[pygame.K_d] or PressedKey[pygame.K_RIGHT]:
        Player.Pos[0] = Player.Pos[0] + Speed

    # Print Player in screen
    screen.blit(Player.CharacterSurface,(Player.Pos[0],Player.Pos[1]))

    # Print Enemy in screen and calc position
    if Enemy.Pos[0] > X_background_Size-Enemy.size[0]:
        Enemy.Direction[0] = -1
    elif Enemy.Pos[0] < 0:
        Enemy.Direction[0] = 1
    Enemy.Pos[0] = Enemy.Pos[0] + Speed*Enemy.Direction[0]*1.5

    if Enemy.Pos[1] > Y_background_Size-Enemy.size[1]:
        Enemy.Direction[1] = -1
    elif Enemy.Pos[1] < 0:
        Enemy.Direction[1] = 1
    Enemy.Pos[1] = Enemy.Pos[1] + Speed*Enemy.Direction[1]*1.5
    
    screen.blit(Enemy.CharacterSurface,(Enemy.Pos[0],Enemy.Pos[1]))

    # Print Shot on screen
    if aiming_pos != (0,0):
        #fuction getShotDirection ausführen
        ShotDirection = getShotdirection(Player.Pos[0]+15,Player.Pos[1]+15,aiming_pos[0]-10,aiming_pos[1]-10)
        # neues Shot object in Liste erstellen
        shotList.append(Shot((Player.Pos[0]+15,Player.Pos[1] +15),ShotDirection, False,(100,100,100)))

    time += 1
    if time == 15:
        time = 0
        EnemyShotFired = True

    if EnemyShotFired == True:
        #fuction getShotDirection ausführen
        ShotDirection = getShotdirection(Enemy.Pos[0]+15,Enemy.Pos[1]+15,Player.Pos[0]-10,Player.Pos[1]-10)
        # neues Shot object in Liste erstellen
        shotList.append(Shot((Enemy.Pos[0]+15,Enemy.Pos[1] +15),ShotDirection, True,(150,200,230)))

    if len(shotList) != 0:
        for i in range(len(shotList)): # Die Liste aller Shot objects durchlaufen
            if shotList[i].noShow == False:
                screen.blit(shotList[i].shotSurface,(shotList[i].ActualPos))
                shotList[i].newPosCalc(10)
                if shotList[i].ActualPos[0] > X_background_Size+100 or shotList[i].ActualPos[0] < -100 or shotList[i].ActualPos[1] > Y_background_Size+100 or shotList[i].ActualPos[1] < -100:
                    shotList[i].noShow = True

                if shotList[i].HittingPlayer == False:
                    if shotList[i].checkCollision(Enemy.Pos[0],Enemy.Pos[1],Enemy.size[0],Enemy.size[1]) == True:
                        shotList[i].noShow = True
                        hits += 1
                elif shotList[i].HittingPlayer == True:
                    if shotList[i].checkCollision(Player.Pos[0],Player.Pos[1],Player.size[0],Player.size[1]) == True:
                        shotList[i].noShow = True
                        Font = pygame.font.SysFont('Comic Sans MS', 100)
                        GameOver = Font.render('GAME OVER', False, (225,0,0))
                        screen.blit(GameOver,(250,300))
                        
                        

    # Print framerate and playtime in titlebar.
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)


    if hits > 10:
        Font = pygame.font.SysFont('Comic Sans MS', 100)
        GameOver = Font.render('WIN', False, (225,230,0))
        screen.blit(GameOver,(350,350))
        pygame.display.flip()
        pygame.time.wait(2000)
        mainloop = False

    if GameOver is None:
        # Display the Score
        Score = Font.render('Score is '+ str(hits), False, (255,0,0))
        screen.blit(Score,(10,10)) 

        #Update Pygame display
        pygame.display.flip()
    else:
        pygame.display.flip()
        pygame.time.wait(2000)
        mainloop = False
    

# Finish Pygame.  
pygame.quit()
