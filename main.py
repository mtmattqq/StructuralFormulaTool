import pygame
from tkinter import filedialog as fd
import Element
import io
from PIL import Image

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
FPS=120
elements=[Element.Element()]
elements[0].isDefault=True
bonds=[Element.Bond()]
bonds[0].type=0
relativePos=Element.vec2D(480,290)
selectedElement=elements[0]
selectedPos=Element.vec2D(0,0)
bufferString=""

# def file_path():
#     filename=
#     return filename

def show_text(text='',x=0,y=0,color=(0,0,0)):
    text=font.render(text,True,color)
    textRect=text.get_rect()
    textRect.center=(x+relativePos.x,y+relativePos.y)
    screen.blit(text,textRect)

def mouse_click():
    global selectedElement,selectedPos,bufferString
    # add new bond
    for element in elements:
        t=pygame.mouse.get_pos()
        op=element.detect_mouse(Element.vec2D(t[0]-relativePos.x,t[1]-relativePos.y))
        if op==0:
            element.selected=0
            element.highlight=False
            continue
        elif op==1:
            if selectedElement.id==element.id and not element.left:
                newElement=Element.Element(Element.vec2D(element.pos.x-100,element.pos.y))
                newBond=Element.Bond(element,newElement)
                # element.left=newElement.right=True
                bonds.append(newBond)
                elements.append(newElement)
            else:
                selectedElement.selected=0
                newBond=Element.Bond(element,selectedElement)
                bonds.append(newBond)
        elif op==2:
            if selectedElement.id==element.id and not element.right:
                newElement=Element.Element(Element.vec2D(element.pos.x+100,element.pos.y))
                newBond=Element.Bond(element,newElement)
                # element.right=newElement.left=True
                bonds.append(newBond)
                elements.append(newElement)
            else:
                newBond=Element.Bond(element,selectedElement)
                bonds.append(newBond)
        elif op==3:
            if selectedElement.id==element.id and not element.up:
                newElement=Element.Element(Element.vec2D(element.pos.x,element.pos.y-100))
                newBond=Element.Bond(element,newElement)
                # element.up=newElement.down=True
                bonds.append(newBond)
                elements.append(newElement)
            else:
                selectedElement.selected=0
                newBond=Element.Bond(element,selectedElement)
                bonds.append(newBond)
        elif op==4:
            if selectedElement.id==element.id and not element.down:
                newElement=Element.Element(Element.vec2D(element.pos.x,element.pos.y+100))
                newBond=Element.Bond(element,newElement)
                # element.down=newElement.up=True
                bonds.append(newBond)
                elements.append(newElement)
            else:
                selectedElement.selected=0
                newBond=Element.Bond(element,selectedElement)
                bonds.append(newBond)
        elif op==5:
            # element is choosed
            if element.highlight:
                element.highlight=False
                selectedPos=Element.vec2D(0,0)
            else:
                element.highlight=True
                bufferString=""
                selectedPos=Element.vec2D(t[0]-relativePos.x,t[1]-relativePos.y)
        elif op==6:
            if not element.isDefault:
                for bond in bonds:
                    if bond.ste.id==element.id or bond.ede.id==element.id:
                        bond.ste.left=bond.ste.right=bond.ste.up=bond.ste.down=False
                        bond.ede.left=bond.ede.right=bond.ede.up=bond.ede.down=False
                        bond.type=0
                    print(bond.ste.id,bond.ede.id,element.id)
                elements.remove(element)
        element.selected=0
    selectedElement=Element.Element()
    Element.id-=1
    selectedElement.isDefault=True
    
    if t[0]<30 and t[0]>0 and t[1]<15 and t[0]>0:
        # file=fd.asksaveasfile(filetypes=(('png files', '*.png'),('jpeg files', '*.jpeg')))
        # tp=io.BytesIO()
        f=pygame.image.tostring(screen,"RGB")
        tp=list(f)
        # png.from_array('L').save
        print(tp)
        # file.write(tp)

def add_bond_only():
    global selectedElement,selectedPos
    if selectedElement.selected!=0:
        return
    for element in elements:
        t=pygame.mouse.get_pos()
        op=element.detect_mouse(Element.vec2D(t[0]-relativePos.x,t[1]-relativePos.y))
        if op==0:
            element.selected=0
            continue
        elif op==1 and not element.left:
            element.selected=1
            selectedElement=element
        elif op==2 and not element.right:
            element.selected=2
            selectedElement=element
        elif op==3 and not element.up:
            element.selected=3
            selectedElement=element
        elif op==4 and not element.down:
            element.selected=4
            selectedElement=element
        


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
        if event.type==pygame.KEYDOWN:
            keys=pygame.key.get_pressed()
            if keys[pygame.K_BACKSPACE]:
                bufferString=bufferString[:-1]
            else:
                bufferString+=event.unicode
            for element in elements:
                if element.highlight:
                    element.text=bufferString

    
    # show elements
    for element in elements:
        show_text(element.text,element.pos.x,element.pos.y)
        if element.highlight:
            pygame.draw.rect(screen,(0,0,0),[element.pos.x+relativePos.x-20,element.pos.y+relativePos.y-20,45,45],1)
        # print(element.id)
    
    # show button when mouse get close
    t=pygame.mouse.get_pos()
    for element in elements:
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
        elif op==5 and element.highlight and pygame.mouse.get_pressed()[0]:
            # t=pygame.mouse.get_pos()
            if selectedPos!=Element.vec2D(0,0):
                difference=Element.vec2D((t[0]-relativePos.x)-selectedPos.x,(t[1]-relativePos.y)-selectedPos.y)
                # print(difference.get_tuple())
                element.pos+=difference
            selectedPos=Element.vec2D(t[0]-relativePos.x,t[1]-relativePos.y)
        elif op==6 and element.highlight:
            # debug
            pygame.draw.rect(screen,(0,255,255),[element.pos.x+relativePos.x+25,element.pos.y+relativePos.y-40,20,20],1)
        # print(op)
    
    # show bond
    for bond in bonds:
        if bond.type==0:
            continue
        v=Element.vec2D(bond.ede.pos.x-bond.ste.pos.x,bond.ede.pos.y-bond.ste.pos.y)
        v*=0.3
        if Element.dis(Element.vec2D(0,0),v)>50:
            v.set(v.x,v.y,50)
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

    pygame.draw.rect(screen,(200,200,200),[0,0,30,15],2)
    
    
    pygame.display.flip()
    clock.tick(FPS)