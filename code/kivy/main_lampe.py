# -*- coding: utf-8 -*-

import kivy
kivy.require('1.0.8')
from kivy.app import App

from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty, \
        NumericProperty, ObjectProperty, BooleanProperty, DictProperty
from kivy.uix.screenmanager import ScreenManager, SlideTransition, FadeTransition, WipeTransition, ShaderTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.logger import Logger

from os.path import join, dirname
from glob import glob
from functools import partial

# Threading
import time
from threading import Thread
import serial





################################## M I S C #########################################

# Create your own transition. This shader implements a "fading"
# transition.
fs = """$HEADER
    uniform float t;
    uniform sampler2D tex_in;
    uniform sampler2D tex_out;

    void main(void) {
        vec4 cin = texture2D(tex_in, tex_coord0);
        vec4 cout = texture2D(tex_out, tex_coord0);
        gl_FragColor = mix(cout, cin, t);
    }
"""



class MainLayout(FloatLayout):
    app = ObjectProperty(None)
                     
  


######################################## A P P ######################################################

class RetailApp(App):

    def serial_input(self, dt):
        ard = serial.Serial(port='COM3',timeout=5)
        a = 1
        if a == 1:
            msg = ard.readline()
            print msg
            msg = str(msg)
    	    if  '00011' in msg: 
		        self.object_down('01')
 
            elif '10111' in msg: 
		        self.object_down('02')
 
            elif '11011' in msg : 
		        self.object_down('03')
 
            elif '11101' in msg: 
		        self.object_down('04')
 
            elif msg in '11110': 
		        self.object_down('05')
 
            
    def object_down(self, id, *largs):
        print id
        self.show_screenview_by_name(id)

    def object_up(self, id, *largs):
        self.show_screenview_by_name('welcome')


    # APP ############################### SCREEN MANAGER ####################################################

    def show_screenview_by_name(self, name):
        sm = self.screen_manager 
        cur = sm.current
        #sm.transition.direction = direction
        #sm.transition.duration = .5 

        if cur != name:            
            # show product view 
            sm.current = name

            if name == 'welcome': 
                return

            # reinit carousel, go to first slide
            product_view = self.product_layout_views[name]
            carousel = product_view.carousel
            slides = carousel.slides
            carousel.load_slide(slides[0])

    def show_screenview(self, screenview, direction):
        sc = screenview
        sm = self.screen_manager 
        cur = sm.current
        #sm.transition.direction = direction
        #sm.transition.duration = .5 

        if cur != sc.name:
            sm.current = sc.name

    def on_pause(self):
        return True

    def test(self):
        # TEMPORARY TEST 
        self.object_down('03')
        #Clock.schedule_once(partial(self.object_down, '03'), 10)
        #Clock.schedule_once(partial(self.object_up, '01'), 16)    
        #Clock.schedule_once(partial(self.object_down, '02'), 20)
        #Clock.schedule_once(partial(self.object_up, '02'), 30)
        #Clock.schedule_once(partial(self.object_down, '01'), 36)

    def build(self):

        # data
        data = ['03'] 

        # main 
        self.main_layout = main_layout = MainLayout(app = self)
        
        # basedir
        self.base_dir = dirname(__file__)

        # get screen size and resize ratio compare to full HD size
        self.screen_size = screen_size = Window.size #(1280, 800) #(1280, 800) #NEXUS7
        #self.screen_ratio = screen_ratio = min(screen_size[0]/1920., screen_size[1]/1080.)
        self.screen_ratio = screen_ratio = min(screen_size[0]/1600., screen_size[1]/1200.)
        print screen_size, screen_ratio
        
        # screen manager
        self.screen_manager = sm = ScreenManager( 
                                                 #transition = ShaderTransition(fs = fs, duration = 1.5)
                                                 #transition = SlideTransition(duration = 1.5)
                                                 transition = FadeTransition(duration = 1.5)
                                                 )
        main_layout.add_widget(sm) 

        # welcome layout
        from widget.welcome_view import WelcomeLayoutView      
        self.welcome_layout_view = wlv = WelcomeLayoutView(
                           app = self,
                           #size_hint= (1, 1),
                           size_hint= (None, None),
                           size = self.screen_size,
                           name = 'welcome'  
                           )  
        sm.add_widget(wlv)      
 
        # screen views
        from widget.product_view import ProductLayoutView        
        self.product_layout_views = {}          

        # Create product layout view
        for i in data:
            path = join(self.base_dir, i)
            Logger.info('Main: Create %s layout' % i)

            self.product_layout_views[i] = plv = ProductLayoutView(
                           app = self,
                           #size_hint= (1, 1),
                           size_hint= (None, None),
                           size = self.screen_size,
                           name = i,
                           path = path  
                           )
            sm.add_widget(plv)
            #Logger.info('Main: Add %s layout' % i)
        """
        # Create THread to analyse Serial Port data input
        print 'Start serial input thread'
        serial_input_thread = t = Thread(target=self.serial_input)
        t.start() 
        t.join()
        """
        # read serial input
        #Clock.schedule_interval(self.serial_input, 1)
		
        sm.current = 'welcome'

        
        self.test()
        return main_layout 
        

if __name__ in ('__main__','__android__'):
    RetailApp().run()
