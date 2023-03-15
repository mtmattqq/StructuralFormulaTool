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
bonds[0].type=0
relativePos=Element.vec2D(480,290)
selectedElement=Element.Element()

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
        elif op==1 and not element.left:
            if selectedElement==element:
                newElement=Element.Element(Element.vec2D(element.pos.x-100,element.pos.y))
                newBond=Element.Bond(element,newElement)
                element.left=newElement.right=True
                bonds.append(newBond)
                elements.append(newElement)
        elif op==2 and not element.right:
            # debug
            newElement=Element.Element(Element.vec2D(element.pos.x+100,element.pos.y))
            newBond=Element.Bond(element,newElement)
            element.right=newElement.left=True
            bonds.append(newBond)
            elements.append(newElement)
        elif op==3 and not element.up:
            # debug
            newElement=Element.Element(Element.vec2D(element.pos.x,element.pos.y-100))
            newBond=Element.Bond(element,newElement)
            element.up=newElement.down=True
            bonds.append(newBond)
            elements.append(newElement)
        elif op==4 and not element.down:
            # debug
            newElement=Element.Element(Element.vec2D(element.pos.x,element.pos.y+100))
            newBond=Element.Bond(element,newElement)
            element.down=newElement.up=True
            bonds.append(newBond)
            elements.append(newElement)

def add_bond_only():
    if selectedElement.selected!=0:
        return
    for element in elements:
        t=pygame.mouse.get_pos()
        op=element.detect_mouse(Element.vec2D(t[0]-relativePos.x,t[1]-relativePos.y))
        if op==0:
            continue
        elif op==1 and not element.left:
            element.selected=1
            selectedElement=element
            return
        elif op==2 and not element.right:
            element.selected=2
            selectedElement=element
            return
        elif op==3 and not element.up:
            element.selected=3
            selectedElement=element
            return
        elif op==4 and not element.down:
            element.selected=4
            selectedElement=element
            return

# main loop

InGame=True
while InGame:
    screen.fill((255,255,255))
    
    # event in pygame
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
        if event.type==pygame.MOUSEBUTTONUP:
            mouse_click()
        if event.type==pygame.MOUSEBUTTONDOWN:
            add_bond_only()

    
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

    # show bond
    for bond in bonds:
        if bond.type==0:
            continue
        v=Element.vec2D(bond.ede.pos.x-bond.ste.pos.x,bond.ede.pos.y-bond.ste.pos.y)
        v*=0.3
        n=Element.vec2D(v.y,-v.x)
        n.set(n.x,n.y,5)

        st=Element.vec2D(bond.ste.pos.x,bond.ste.pos.y)
        st+=relativePos
        st+=v
        ed=Element.vec2D(bond.ede.pos.x,bond.ede.pos.y)
        ed+=relativePos
        ed-=v

        if bond.type>=1:
            pygame.draw.line(screen,(0,0,0),st.get_tuple(),ed.get_tuple())
        if bond.type>=2:
            st+=n; ed+=n
            pygame.draw.line(screen,(0,0,0),st.get_tuple(),ed.get_tuple())
        if bond.type==3:
            st+=n; ed+=n
            pygame.draw.line(screen,(0,0,0),st.get_tuple(),ed.get_tuple())
    
    
    pygame.display.flip()
    clock.tick(FPS)