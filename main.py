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
bonds=[Element.Bond()]
relativePos=Element.vec2D(480,290)

def show_text(text='',x=0,y=0,color=(0,0,0)):
    text=font.render(text,True,color)
    textRect=text.get_rect()
    textRect.center=(x+relativePos.x,y+relativePos.y)
    screen.blit(text,textRect)

def mouse_click():
    # add new bond
    for element in elements:
        t=pygame.mouse.get_pos()
        op=element.detect_mouse(Element.vec2D(t[0]-relativePos.x,t[1]-relativePos.y))
        if op==0:
            continue
        elif op==1:
            # debug
            newElement=Element.Element(Element.vec2D(element.pos.x-100,element.pos.y))
            newBond=Element.Bond(element,newElement)
            bonds.append(newBond)
            elements.append(newElement)
        elif op==2:
            # debug
            newElement=0
        elif op==3:
            # debug
            newElement=0
        elif op==4:
            # debug
            newElement=0
        print(op)

# main loop

InGame=True
while InGame:
    screen.fill((255,255,255))
    
    # event in pygame
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_click()

    
    # show elements
    for element in elements:
        show_text(element.text,element.pos.x,element.pos.y)
        # debug
        pygame.draw.rect(screen,(0,0,0),[element.pos.x+relativePos.x-20,element.pos.y+relativePos.y-20,45,45],1)
    
    # show button when mouse get close
    for element in elements:
        t=pygame.mouse.get_pos()
        op=element.detect_mouse(Element.vec2D(t[0]-relativePos.x,t[1]-relativePos.y))
        if op==0:
            continue
        elif op==1:
            # debug
            pygame.draw.rect(screen,(255,0,0),[element.pos.x+relativePos.x-40,element.pos.y+relativePos.y-20,20,45],1)
        elif op==2:
            # debug
            pygame.draw.rect(screen,(0,255,0),[element.pos.x+relativePos.x+25,element.pos.y+relativePos.y-20,20,45],1)
        elif op==3:
            # debug
            pygame.draw.rect(screen,(0,0,255),[element.pos.x+relativePos.x-20,element.pos.y+relativePos.y-40,45,20],1)
        elif op==4:
            # debug
            pygame.draw.rect(screen,(255,0,255),[element.pos.x+relativePos.x-20,element.pos.y+relativePos.y+25,45,20],1)
        print(op)

    
    
    pygame.display.flip()
    clock.tick(FPS)