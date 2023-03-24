'''
Welcome to sus clicker V3 {remastered}

in this update:
- All bugs have been fixed
- Completely rewrote the code
- Added physics to the suses
- Added better saved data {can modify if you want}
- Removed cheats as you can just change the data
- Better music
- Rebirth animation
- Better data loading
- Secret eggs?

And much more to come!
'''
from ursina import *
import json
import threading

with open("data.json", 'r') as data:
    data=json.load(data)

#Classes
class FallingSus(Entity):
    def __init__(self, position):
        super().__init__(
            model='quad',
            texture='assets/Red.png',
            scale=0.35,
            position=position,
        )
        self.speed = Vec3(0, 6, 0)
        self.gravity = Vec3(0, -9.81, 0)
        self.max_swerve_speed = 4.0
        self.swerve_speed = random.uniform(-self.max_swerve_speed, self.max_swerve_speed)
        
    def update(self):
        self.speed += self.gravity * time.dt
        self.position += self.speed * time.dt
        self.position += Vec3(self.swerve_speed * time.dt, 0, 0)
        if self.y <= -9:
            destroy(self)

class Gen(Button):
    def __init__(self,susmaker,default_cost, cost, icon, position,bought=0, scale=.1,**kwargs):
        super().__init__(self,position=position,scale=scale, **kwargs)
        self.cost=cost
        self.bought=bought
        self.susmaker=susmaker
        self.can_buy=icon
        self.cant_buy='assets/Need_more.png'
        self.cost=cost
        self.default_cost=default_cost
        self.color=color.clear
        self.highlight_color=color.clear
        self.pressed_color=color.clear
        self.on_click=self.bought_gen
        self.tooltip=Tooltip(f'Buy for <green>{self.cost} suses')
        self.save_data()
    def update(self):
        if suses>=self.cost:
            self.icon=self.can_buy
            self.tooltip.text=f'Buy for <green>{self.cost} suses'
        else:
            self.icon=self.cant_buy
            self.tooltip.text=f'Buy for <red>{self.cost} suses'
        

    def bought_gen(self):
        global suses
        if suses>=self.cost:
            suses-=self.cost
            self.bought+=1
            self.cost+=round(self.default_cost+25)
            self.generate_sus()
        else:
            print_on_screen("Not enough sus!")
    def generate_sus(self):
        global suses
        if not Prestiging:
            suses+=round(self.susmaker+multiplier)
            invoke(self.generate_sus,delay=1)
        else:
            pass

    def save_data(self):
        if self.bought>=1:
            for i in range(self.bought):
                self.generate_sus()



#Funcions 
async def LoadAudio(path, name=None,autoplay=False,loop=False):
    global audioname
    audioname = loader.loadSfx(path)
    
    audioname=Audio(audioname,autoplay=autoplay,loop=loop)
    if name!=None:
        globals()[name] = audioname
    else:
        pass

def load_animation(path,name):
    animation = Animation(path,visible=False)
    globals()[name] = animation

def start_loading_animation(path,name=None):
    loading_thread = threading.Thread(target=load_animation, args=(path, name))
    loading_thread.start()

def sus_click():
    global multiplier,suses
    suses+=1*multiplier
    susClicker.scale = [e*1.25 for e in [.1,.1]]
    susClicker.animate('scale_x', .15, duration=.1)
    susClicker.animate('scale_y', .15, duration=.1)
    falling_picture = FallingSus(susClicker.position - (2.1,1.1,0))
    falling_picture.position += Vec3(0, 1.5, 0)


def shop():
    global inMenu
    MenuClick.play()
    if not inMenu:
        shopIcon.animate_rotation([0, 0, 180], duration=1.3)
        shopIcon.animate_position([4,0], duration=1.3)
        Gen1.animate_position([.8,.2], duration=1.3)
        Gen2.animate_position([.8,0], duration=1.3)
        Gen3.animate_position([.8,-0.2], duration=1.3)
        shop_background.animate_position([7.5,0], duration=1.3)
        prestige.animate_position([.8,.4], duration=1.3)
        NextPageButton.visible=True
        PreviousPageButton.visible=True
        shopButton.x=.49
        inMenu=True
    else:
        shopIcon.animate_rotation([0,0,0], duration=1.3)
        shopIcon.animate_position([6,0], duration=1.3)
        Gen1.animate_position([1,.2], duration=1.3)
        Gen2.animate_position([1,0], duration=1.3)
        Gen3.animate_position([1,-.2], duration=1.3)
        shop_background.animate_position([9,0], duration=1.3)
        prestige.animate_position([1,.4], duration=1.3)
        PreviousPageButton.visible=False
        NextPageButton.visible=True
        shopButton.x=.73
        inMenu=False

def NextPage():
    global currentPage
    if currentPage<2:
        currentPage+=1
        print("Next pressed")

def PreviousPage():
    global currentPage
    if currentPage>1:
        currentPage-=1
        print("Previous pressed")

def Prestige():
    global suses,multiplier,PresCost,Prestiging
    if suses>=PresCost:
        if inMenu:
            shop()
        Prestiging=True
        suses=0
        PrestigeSong.play()
        BgMusic.stop()
        Gen1.cost=100
        Gen1.bought=0
        Gen2.cost=450
        Gen2.bought=0
        Gen3.cost=1000
        Gen3.bought=0
        data['suses'] = 0
        data['susGen1Cost']=100
        data['susGen1Bought']=0
        data['susGen2Cost']=450
        data['susGen2Bought']=0
        data['susGen3Cost']=1000
        data['susGen3Bought']=0
        PresCost+=round(5000*1.1)
        multiplier+=1
        shopIcon.visible=False
        animation.visible=True
        black.visible=True
        suses_text.visible=False
        susClicker.visible=False
        susClicker.disabled=True
        black.animate_scale((100,100,100),duration=10)
        animation.animate_scale((1000,1000,1000),duration=6)
        animation.animate_position([-40,0],duration=5)
        invoke(after_pres,delay=10)

def after_pres():
    global Prestiging
    destroy(black)
    destroy(animation)
    BgMusic.play()
    Prestiging=False
    shopIcon.visible=True
    suses_text.visible=True
    susClicker.visible=True
    susClicker.disabled=False

#Ursina
app=Ursina()

#window settings
window.fps_counter.enabled=False
window.icon='assets/Red.ico'
window.title="Sus clicker"
window.exit_button.enabled = False

#Variables
secret=data['EE']
suses=data['suses']
multiplier=data['multiplier']
PresCost=data['PrestiegeCost']
Gen1Cost=data['susGen1Cost']
Gen1Bought=data['susGen1Bought']
Gen2Bought=data['susGen2Bought']
Gen2Cost=data['susGen2Cost']
Gen3Bought=data['susGen3Bought']
Gen3Cost=data['susGen3Cost']

Prestiging=False
inMenu=False
currentPage=1

##Buttons and there stuff

#Sus clicker stuff
suses_text=Text(text=f"suses: {suses}",y=.4,x=-.05)
suses_text.create_background()
susClicker=Button(parent=camera.ui,icon='assets/Red.png',scale=.15,x=-.3,color=color.clear,highlight_color=color.clear,pressed_color=color.clear,on_click=sus_click)

#Shop stuff
shopIcon=Entity(model='quad',texture='assets/shop.png',scale=1,x=6)
shopButton=Button(icon=None,x=.73,z=-1,scale=.12,pressed_color=color.clear,color=color.clear,hightlight_color=color.clear,on_click=shop)
NextPageButton=Button(icon="assets/shop.png",x=.85,y=-.4,z=-1,rotation_z=180,visible=False,scale=.07,pressed_color=color.clear,color=color.clear,hightlight_color=color.clear,on_click=NextPage)
PreviousPageButton=Button(icon="assets/shop.png",x=.78,y=-.4,z=-1,scale=.07,visible=False,pressed_color=color.clear,color=color.clear,hightlight_color=color.clear,on_click=PreviousPage)

#Gen stuff
Gen1=Gen(default_cost=100,susmaker=1,cost=Gen1Cost,icon='assets/Green.png',position=(1,.2,0),bought=Gen1Bought)
Gen2=Gen(default_cost=450,susmaker=3,cost=Gen2Cost,icon='assets/Blue.png',position=(1,0,0),bought=Gen2Bought)
Gen3=Gen(default_cost=1000,susmaker=5,cost=Gen3Cost,icon='assets/pink.png',position=(1,-.2,0),bought=Gen3Bought)

#Prestige stuff
prestige=Button(text='Prestige',icon='assets/pres logo.png',scale=.15,position=(1,.4,0),color=color.clear,hightlight=color.clear,pressed_color=color.clear,on_click=Prestige)
prestige.text_entity.y=-.2
prestige.tooltip=Tooltip(f'buy for <green>{PresCost} suses')

##Audio
app.taskMgr.add(LoadAudio(path="assets/bg_music.ogg",name='BgMusic',autoplay=True,loop=True))
app.taskMgr.add(LoadAudio(path="assets/menupop.ogg",name='MenuClick',autoplay=False,loop=False))
app.taskMgr.add(LoadAudio(path="assets/PrestigeMusic.ogg",name='PrestigeSong',autoplay=False,loop=False))

##Background stuff
bg=Entity(model='quad',texture='assets/bg.mp4',scale_x=90,scale_y=49.5,z=100)

##Misc things
shop_background=Entity(model='quad',color=color.black66,x=9,scale_x=2,scale_y=12,z=2)
start_loading_animation('assets/will.gif',name="animation")
black=Entity(model='quad',color=color.black,scale=.000000001,z=-4)


##game functions
def input(key):

    if held_keys['control'] and held_keys['shift'] and key=='m':
        data['suses'] = 0
        data['multiplier']=1
        data['PrestiegeCost']=5000
        data['susGen1Cost']=100
        data['susGen1Bought']=0
        data['susGen2Cost']=450
        data['susGen2Bought']=0
        data['susGen3Cost']=1000
        data['susGen3Bought']=0
    if held_keys['k'] and held_keys['i'] and key=='d':
        #application.paused=True
        print_on_screen("Secret unlocked!")
        secret=True

def update():
    global prestige
    if suses>=PresCost:
        prestige.tooltip.text=f'buy for <green>{PresCost} suses'
    else:
        prestige.tooltip.text=f'buy for <red>{PresCost} suses'
    data['suses'] = suses
    data['multiplier']=multiplier
    data['PrestiegeCost']=PresCost
    data['susGen1Cost']=Gen1.cost
    data['susGen1Bought']=Gen1.bought
    data['susGen2Cost']=Gen2.cost
    data['susGen2Bought']=Gen2.bought
    data['susGen3Cost']=Gen3.cost
    data['susGen3Bought']=Gen3.bought
    with open("data.json", "w") as f:
        json.dump(data, f,indent=4)
    suses_text.text=f"suses: {suses}"
    suses_text.create_background()

#Ursina
app.run()