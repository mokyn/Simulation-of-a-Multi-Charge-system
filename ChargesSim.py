GlowScript 2.7 VPython

#Setting up the canvas
key = 0
scene.width = 1000
scene.height = 500
click=False
dragging = False
#Clicking the Mouse
def down():
    global click
    global showfield
    global running
    click = True
    if mag(scene.mouse.pos-runB.pos) < 3:
        running = not running
        if running:
            t=attach_trail(tc, radius=0.1, color=color.red )
        else:
            t.stop()
    if mag(scene.mouse.pos-addP.pos) < 3:
        rand = vec(-5+10*random(),-5+10*random(),0)
        charges.append(compound([sphere(color=color.red, pos=rand),box(color=color.white,pos=rand+vec(0,0,1),size=vec(1,0.2,0.2)),box(color=color.white,pos=rand+vec(0,0,1),size=vec(0.2,1,0.2))]))
        charges[-1].charge=qe
        charges[-1].v=vec(0,0,0)
        charges[-1].mass=me
        vvs.append(arrow(color=color.green, pos=vec(0,0,0), opacity=0))
        avs.append(arrow(color=color.red, pos=vec(0,0,0), opacity=0))
    if mag(scene.mouse.pos-addE.pos) < 3:
        rand = vec(-5+10*random(),-5+10*random(),0)
        charges.append(compound([sphere(color=color.blue, pos=rand),box(color=color.white,pos=rand+vec(0,0,1),size=vec(1,0.2,0.2))]))
        charges[-1].charge=-qe
        charges[-1].v=vec(0,0,0)
        charges[-1].mass=me
        vvs.append(arrow(color=color.green, pos=vec(0,0,0), opacity=0))
        avs.append(arrow(color=color.red, pos=vec(0,0,0), opacity=0))
def setvel():
    global pressv
    pressv=True
def vup():
    global pressv
    pressv=False
fieldlines=[]
pressv = False
charges=[]
vvs = []
avs = []
bounds=compound([box(color=color.white, pos=vec(-25,0,0), size=vec(1,51,1)),box(color=color.white, pos=vec(25,0,0), size=vec(1,51,1)),box(color=color.white, pos=vec(0,25,0), size=vec(51,1,1)),box(color=color.white, pos=vec(0,-25,0), size=vec(51,1,1))])
#Releasing the mouse
def mouseup():
    global click
    global dragging
    click = False
    dragging = False
scene.bind("mousedown", down)
scene.bind('mouseup', mouseup)
scene.bind("v keydown",setvel)
scene.bind("v keyup",vup)
running = False
runB= label(pos=vec(15,11,0), text='Run')
addP= label(pos=vec(15,7,0), text='Add Positive Charge')
addE= label(pos=vec(15,3,0), text='Add Negative Charge')
k=9.0*10**9
qe=1.6*10**(-19)
#Setting up 20x20 array of electric field lines
for x in range (10):
    for y in range (10):
        fieldlines.append(arrow(ipos=vec(-22.5+5*x,-22.5+5*y,0)))
v=vec(0,0,0)
me=9.109*10**-31
#Main game loop
frate = 40
while True:
    rate(frate)
    addP.pos=scene.center+vec(330*scene.pixel_to_world,120*scene.pixel_to_world,0)
    addE.pos=scene.center+vec(330*scene.pixel_to_world,70*scene.pixel_to_world,0)
    runB.pos=scene.center+vec(330*scene.pixel_to_world,20*scene.pixel_to_world,0)
    if running:
        runB.text='Stop'
    else:
        runB.text='Run'
    for i in range (len(charges)):
        if ((mag(charges[i].pos-scene.mouse.pos)<(20*scene.pixel_to_world) and not dragging) or dragging==i) and click:
            if dragging==False:
                offset=scene.mouse.pos-charges[i].pos
                dragging = i
            charges[i].pos = scene.mouse.pos-offset
    for line in fieldlines:
        fnet = vec(0,0,0)
        for particle in charges:
            fnet+= particle.charge*(line.ipos-particle.pos) / (mag(line.ipos-particle.pos)**3)
        line.pos=line.ipos-norm(fnet)*1.5
        line.axis=norm(fnet)*3
        line.opacity=mag(fnet)*5*10**20
    if running:
        for particle in charges:
            fnet=vec(0,0,0)
            particle.pos.z=0
            for p2 in charges:
                if particle != p2:
                    fnet+=k*particle.charge*p2.charge*(particle.pos-p2.pos) / (mag(particle.pos-p2.pos)**3)
                    if mag(particle.pos-p2.pos)<2:
                        particle.pos += norm(particle.pos-p2.pos)*(1- mag(particle.pos-p2.pos)/2)
                        p2.pos += norm(p2.pos-particle.pos)*(-mag(p2.pos-particle.pos)/2+1)
                        fnet=vec(0,0,0)
                        temp=vec(particle.v)
                        particle.v=p2.v
                        p2.v=temp
            particle.a=fnet/particle.mass
            particle.v += particle.a/frate
            if particle.pos.x>23:
                particle.v.x=-particle.v.x
                particle.pos.x=23
            if particle.pos.x<-23:
                particle.v.x=-particle.v.x
                particle.pos.x=-23
            if particle.pos.y>23:
                particle.v.y=-particle.v.y
                particle.pos.y=23
            if particle.pos.y<-23:
                particle.v.y=-particle.v.y
                particle.pos.y=-23
            if mag(particle.v)>10:
                particle.v=10*norm(particle.v)
            particle.pos+= particle.v/frate
        for i in range (len(charges)):
            vvs[i].pos = charges[i].pos
            avs[i].pos = charges[i].pos
            vvs[i].opacity = 1
            avs[i].opacity = 1
            if mag(charges[i].v)>5:
                vvs[i].axis = 5*norm(charges[i].v)
            else:
                vvs[i].axis = charges[i].v
            if mag(charges[i].a)>5:
                avs[i].axis = 5*norm(charges[i].a)
            else:
                avs[i].axis = charges[i].a
    else:
        for i in range (len(charges)):
            if mag(charges[i].pos-scene.mouse.pos)<5:
                vvs[i].pos=charges[i].pos
                if pressv:
                    vvs[i].axis=scene.mouse.pos-charges[i].pos
                    charges[i].v=scene.mouse.pos-charges[i].pos
                    vvs[i].opacity=1
            
            
            
            