import pygame

# pygame init
pygame.init()
screen=pygame.display.set_mode((1000,600))
screen.fill((255,255,255))
pygame.display.set_caption("Test Game")
font=pygame.font.SysFont('microsoftjhenghei',50)
clock=pygame.time.Clock()
# programIcon=pygame.image.load('icon.png')
# pygame.display.set_icon(programIcon)

# variables
FPS=60
elements=[]


def show_text(text='',x=0,y=0,color=(0,0,0)):
    text=font.render(text,True,color)
    textRect=text.get_rect()
    textRect.center=(x,y)
    screen.blit(text,textRect)

# main loop

InGame=True
while InGame:
    screen.fill((255,255,255))
    
    # event in pygame
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
    
    pygame.display.flip()
    clock.tick(FPS)
