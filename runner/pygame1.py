import pygame
from sys import exit        
from random import randint

class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1= pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2= pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk=[player_walk1,player_walk2]
        self.player_index = 0
        self.player_jump= pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect= self.image.get_rect(midbottom = (80,306))
        self.gravity=0
        
        self.jump_sound= pygame.mixer.Sound('sound/jump.mp3')
        self.jump_sound.set_volume(0.06)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >=306:
            self.gravity =-20
            self.jump_sound.play()
            
    def apply_gravity(self):
        self.gravity+=1
        self.rect.y+=self.gravity
        if self.rect.bottom >= 306 :  
            self.rect.bottom=306
            
    def animation_state(self):
        if self.rect.bottom<300:
            self.image=self.player_jump
        else:
            self.player_index +=0.1
            if self.player_index>=len(self.player_walk):
                self.player_index=0
            self.image=self.player_walk[int(self.player_index)]
            
    def fix_x(self):
        self.rect.bottom=306
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstical(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'fly':
            fly_surf1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
            fly_surf2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
            self.frames=[fly_surf1,fly_surf2]
            y=210
        else:
            snail_surf1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()   #first picture of the snail 
            snail_surf2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_surf1,snail_surf2]
            y=306
        
        self.animation_index = 0
        self.image=self.frames[self.animation_index]
        self.rect =self.image.get_rect(midbottom = (randint(900,1100),y))
        
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index=0
        self.image = self.frames[int(self.animation_index)]
        
    def distroy(self):
        if self.rect.x <-100:
            self.kill()

        
    def update(self):
        self.animation_state()
        self.rect.x -=6
        self.distroy()



def display_score():
    current_time=int((pygame.time.get_ticks()-start_time)/1000)
    score_surf = text_font.render(f'{current_time}',False,"Black")
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def collision():
    if pygame.sprite.spritecollide(player.sprite,obstical_group,True):
        obstical_group.empty()
        return False
    return True
    

pygame.init()   
screen = pygame.display.set_mode((800,400)) 
pygame.display.set_caption('runner')    
clock = pygame.time.Clock() 
game_active = True
start_time = 0
score = 0
background_music=pygame.mixer.Sound('sound/music.wav')
background_music.set_volume(0.04)
background_music.play(loops=-1)

player=pygame.sprite.GroupSingle()
player.add(Player())

obstical_group = pygame.sprite.Group()


sky_pic = pygame.image.load("graphics/Sky.jpg").convert_alpha()  
ground_pic = pygame.image.load('graphics/Ground.jpg').convert_alpha()    

game_over_surf = pygame.image.load("graphics/GameOver.jpg").convert_alpha()


text_font = pygame.font.Font('font/Pixeltype.ttf', 50)   

obstical_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstical_timer,1500)

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:     
            pygame.quit()
            exit()
        if game_active:                 
            if event.type== obstical_timer: 
                r = randint(0,4)
                if r in [1,2,3]:
                    obstical_group.add(Obstical('snail'))
                if r == 4:
                    obstical_group.add(Obstical('fly'))       
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active=True
                start_time=pygame.time.get_ticks()
     
     
                
    if game_active:
        
        screen.blit(sky_pic,(0,0)) 
        screen.blit(ground_pic,(0,306))
        
        score=display_score()
       
            
                    ####Player####
        player.draw(screen)
        obstical_group.draw(screen)
        
        player.update()
        obstical_group.update()
        
        game_active= collision()
        
    else:
        if score==0:
            score_surf=text_font.render('Press space to start',0,"White")
        else:
            score_surf=text_font.render(f'Your score: {score}',0,'White')
            
        screen.blit(game_over_surf,(0,0))
        score_rect=score_surf.get_rect(center=(400,390))
        screen.blit(score_surf,score_rect)

        player.sprite.fix_x()
        player.update()
        
    pygame.display.update() #so that the game updates per frame
    clock.tick(60)  #the frame per second