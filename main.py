import pygame
import Element
# pygame init
pygame.init()
screen=pygame.display.set_mode((1000,600))
screen.fill((255,255,255))
pygame.display.set_caption("結構式繪圖軟體")
font=pygame.font.SysFont('cambriamath',36)
clock=pygame.time.Clock()
# programIcon=pygame.image.load('icon.png')
# pygame.display.set_icon(programIcon)

# variables
FPS=60
elements=[Element.Element()]
relativePos=Element.vec2D(480,290)

def show_text(text='',x=0,y=0,color=(0,0,0)):
    text=font.render(text,True,color)
    textRect=text.get_rect()
    textRect.center=(x+relativePos.x,y+relativePos.y)
    screen.blit(text,textRect)

# main loop

InGame=True
while InGame:
    screen.fill((255,255,255))
    
    # event in pygame
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
    
    # show elements
    for element in elements:
        show_text(element.text,element.pos.x,element.pos.y)
        # debug
        pygame.draw.rect(screen,(0,0,0),[element.pos.x+relativePos.x-20,element.pos.y+relativePos.y-20,45,45],1)
        
    
    pygame.display.flip()
    clock.tick(FPS)