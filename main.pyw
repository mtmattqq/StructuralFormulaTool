import pygame
from tkinter import filedialog as fd
import Element
import os
import zlib
from PIL import Image

# pygame init
pygame.init()
screen=pygame.display.set_mode((1000,600))
screen.fill((255,255,255))
pygame.display.set_caption("結構式繪圖軟體")
font=pygame.font.SysFont('cambriamath',36)
clock=pygame.time.Clock()
programIcon=pygame.image.load('icon.jpg')
pygame.display.set_icon(programIcon)
# ICON=os.path.join(os.getcwd(),"icon.jpg")

# variables
FPS=120
elements=[Element.Element()]
elements[0].isDefault=True
bonds=[Element.Bond()]
bonds[0].type=0
buttons=[Element.Button()]
buttons[0].type=0
benzenes=[Element.Benzene(Element.vec2D(200,0))]
# benzenes.pop()
relativePos=Element.vec2D(480,290)
selectedElement=elements[0]
selectedBond=bonds[0]
selectedPos=Element.vec2D(0,0)
bufferString=""

# def file_path():
#     filename=
#     return filename

def show_text(text='',x=0,y=0,color=(0,0,0)):
    text=font.render(text,True,color)
    textRect=text.get_rect()
    textRect.topleft=(x+relativePos.x-10,y+relativePos.y-20)
    screen.blit(text,textRect)

def delete_element(element):
    for bond in bonds:
        if bond.ste.id==element.id or bond.ede.id==element.id:
            bond.ste.left=bond.ste.right=bond.ste.up=bond.ste.down=False
            bond.ede.left=bond.ede.right=bond.ede.up=bond.ede.down=False
            bond.type=0
        # print(bond.ste.id,bond.ede.id,element.id)
    if element.id<10000000:
        elements.remove(element)

def mouse_click():
    global selectedElement,selectedPos,bufferString
    # add new bond
    operate=False
    t=pygame.mouse.get_pos()
    for element in elements:
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
        elif op==6 and element.highlight:
            if len(elements)>1:
                delete_element(element)
        if op>=1 and op<=6:
            operate=True
        element.selected=0
    
    for benzene in benzenes:
        op=benzene.detect_mouse(Element.vec2D(t[0]-relativePos.x,t[1]-relativePos.y))
        if op==-1:
            benzene.highlight=False
            continue
        elif op>=0 and op<=5:
            # some element been selected
            pos1=benzene.elements[op].pos
            dif=Element.vec2D(pos1.x-benzene.pos.x,pos1.y-benzene.pos.y)
            dif*=-1
            if selectedElement.id==benzene.elements[op].id:
                newElement=Element.Element(Element.vec2D(benzene.elements[op].pos.x-dif.x,benzene.elements[op].pos.y-dif.y))
                newBond=Element.Bond(benzene.elements[op],newElement)
                bonds.append(newBond)
                elements.append(newElement)
            else:
                selectedElement.selected=0
                newBond=Element.Bond(benzene.elements[op],selectedElement)
                bonds.append(newBond)
            operate=True
        elif op==6:
            difference=Element.vec2D((t[0]-relativePos.x)-selectedPos.x,(t[1]-relativePos.y)-selectedPos.y)
            benzene.pos+=difference
            if benzene.highlight:
                benzene.highlight=False
            else:
                benzene.highlight=True
        elif op==7:
            benzenes.remove(benzene)
    Element.id-=1
    selectedElement.isDefault=True
    selectedElement=Element.Element()

    if operate:
        return

    for button in buttons:
        op=button.detect_mouse(Element.vec2D(t[0]-relativePos.x,t[1]-relativePos.y))
        if op:
            if button.text=="|":
                button.bond.type=1
            elif button.text=="||":
                button.bond.type=2
            elif button.text=="|||":
                button.bond.type=3
            elif button.text=="x":
                button.bond.type=0

    if operate:
        return

    buttons.clear()
    for bond in bonds:
        op=bond.detect_mouse(Element.vec2D(t[0]-relativePos.x,t[1]-relativePos.y))
        if op:
            newButton=Element.Button("|",Element.vec2D(t[0]-relativePos.x,t[1]-relativePos.y+20),[0,0,0],bond)
            buttons.append(newButton)
            newButton=Element.Button("||",Element.vec2D(t[0]-relativePos.x+20,t[1]-relativePos.y+20),[0,0,0],bond)
            buttons.append(newButton)
            newButton=Element.Button("|||",Element.vec2D(t[0]-relativePos.x+40,t[1]-relativePos.y+20),[0,0,0],bond)
            buttons.append(newButton)
            newButton=Element.Button("x",Element.vec2D(t[0]-relativePos.x+60,t[1]-relativePos.y+20),[0,0,0],bond)
            buttons.append(newButton)
            
    
    if t[0]<40 and t[0]>0 and t[1]<20 and t[0]>0:
        file=fd.asksaveasfile(filetypes=(('png files', '*.png'),('jpeg files', '*.jpeg')))
        if file==None:
            file.close()
            return
        file_path=fd.askopenfilename()
        # tp=io.BytesIO()
        f=pygame.image.tostring(screen,"RGBA")
        # tp=list(f)
        img=Image.frombytes("RGBA",(1000,600),f)
        img.save(file_path)

        # image_str = pygame.image.tostring(screen,"RGB")
        # compressed_image_str = zlib.compress(image_str)
        
        # png.from_array('L').save
        # print(tp)
        # file.write(tp)

def add_bond_only():
    global selectedElement,selectedPos
    if selectedElement.selected!=0:
        return
    t=pygame.mouse.get_pos()
    for element in elements:
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
    for benzene in benzenes:
        op=benzene.detect_mouse(Element.vec2D(t[0]-relativePos.x,t[1]-relativePos.y))
        if op>=0 and op<=5:
            benzene.elements[op].selected=1
            selectedElement=benzene.elements[op]
        elif op==6 and pygame.mouse.get_pressed()[0]:
            difference=Element.vec2D((t[0]-relativePos.x)-selectedPos.x,(t[1]-relativePos.y)-selectedPos.y)
            benzene.pos+=difference

# main loop
InGame=True
while InGame:
    screen.fill((255,255,255))
    
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
            # if selectedPos!=Element.vec2D(0,0):
            difference=Element.vec2D((t[0]-relativePos.x)-selectedPos.x,(t[1]-relativePos.y)-selectedPos.y)
            # print(difference.get_tuple())
            element.pos+=difference
            
        elif op==6 and element.highlight:
            # debug
            pygame.draw.rect(screen,(0,255,255),[element.pos.x+relativePos.x+25,element.pos.y+relativePos.y-40,20,20],1)
        # print(op)
    
    # show elements
    for element in elements:
        show_text(element.text,element.pos.x,element.pos.y)
        if element.highlight:
            pygame.draw.rect(screen,(0,0,0),[element.pos.x+relativePos.x-20,element.pos.y+relativePos.y-20,45,45],1)
        # print(element.id)

    # move benzene
    for benzene in benzenes:
        benzene.set()
        op=benzene.detect_mouse(Element.vec2D(t[0]-relativePos.x,t[1]-relativePos.y))
        if op>=0 and op<=5:
            # some element been focused
            pos1=benzene.elements[op].pos
            pygame.draw.circle(screen,(0,255,0),[pos1.x+relativePos.x,pos1.y+relativePos.y],15,1)
            a=0
        elif op==6 and pygame.mouse.get_pressed()[0]:
            difference=Element.vec2D((t[0]-relativePos.x)-selectedPos.x,(t[1]-relativePos.y)-selectedPos.y)
            benzene.pos+=difference
            benzene.set()

    # show benzene
    for benzene in benzenes:
        for i in range(6):
            pos1=benzene.elements[i].pos
            pos2=benzene.elements[(i+1)%6].pos
            pygame.draw.line(screen,(0,0,0),
                [pos1.x+relativePos.x,pos1.y+relativePos.y],
                [pos2.x+relativePos.x,pos2.y+relativePos.y]
            )
        pygame.draw.circle(screen,(0,0,0),[benzene.pos.x+relativePos.x,benzene.pos.y+relativePos.y],30,1)
        if benzene.highlight:
            pygame.draw.circle(screen,(255,0,0),[benzene.pos.x+relativePos.x+50,benzene.pos.y+relativePos.y-50],10,1)

    # show button
    for button in buttons:
        if button.type==0:
            continue
        ft=pygame.font.SysFont('cambriamath',14)
        text=ft.render(button.text,True,button.color)
        textRect=text.get_rect()
        textRect.topleft=(button.pos.x+relativePos.x,button.pos.y+relativePos.y)
        pygame.draw.rect(screen,(0,0,0),[button.pos.x+relativePos.x-5,button.pos.y+relativePos.y,20,20],1)
        screen.blit(text,textRect)

    for bond in bonds:
        if bond.type==0:
            bonds.remove(bond)
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
        if bond.ste.id<100000000:
            st+=v
        ed=Element.vec2D(bond.ede.pos.x,bond.ede.pos.y)
        ed+=relativePos
        if bond.ede.id<100000000:
            ed-=v

        if bond.type>=1:
            pygame.draw.line(screen,(0,0,0),st.get_tuple(),ed.get_tuple())
        if bond.type>=2:
            st-=n; ed-=n
            pygame.draw.line(screen,(0,0,0),st.get_tuple(),ed.get_tuple())
        if bond.type==3:
            st+=n*2; ed+=n*2
            pygame.draw.line(screen,(0,0,0),st.get_tuple(),ed.get_tuple())
    
    ft=pygame.font.SysFont('cambriamath',14)
    text=ft.render("save",True,(100,100,100))
    textRect=text.get_rect()
    textRect.topleft=(5,0)
    screen.blit(text,textRect)
    pygame.draw.rect(screen,(100,100,100),[0,0,40,20],2)
    pygame.display.flip()
    selectedPos=Element.vec2D(t[0]-relativePos.x,t[1]-relativePos.y)
    
    # event in pygame
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            InGame=False
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
                    if bufferString=="C6H6":
                        benzenes.append(Element.Benzene(element.pos))
                        delete_element(element)
                    element.text=bufferString
    clock.tick(FPS)
pygame.quit()