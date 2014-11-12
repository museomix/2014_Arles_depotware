# -*- coding: utf-8 -*-

from widget.basescreen import BaseScreen

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.properties import ObjectProperty, DictProperty, ListProperty, NumericProperty, StringProperty, BooleanProperty 
from kivy.logger import Logger
from kivy.clock import Clock

import os

class CarouselBaseItem(FloatLayout):
    app = ObjectProperty(None)
    view = ObjectProperty(None)
    index = NumericProperty(0)

    def on_validated(self, *largs):
        carousel = self.view.carousel 
        carousel.current_is_released()  

class CarouselItem(CarouselBaseItem): #Single Image
    source = StringProperty('')

class CarouselImagesItem(CarouselBaseItem): #Several Images
    source = StringProperty('') 
    sources = ListProperty('')
    locked = BooleanProperty(False)
    
    def change_pic(self):
        if self.locked: return
        images = self.sources
        if len(images) <= 1:
            return
        # get current index
        index = images.index([self.source])
        # increase index
        index += 1
        if index >= len(images):
            index = 0 
        self.source = images[index][0]
    
    def on_touch_down(self, touch):
        super(CarouselImagesItem, self).on_touch_down(touch)
        if self.collide_point(touch.x, touch.y) == True:
            return True

    def validate(self):
        self.locked = True
        print 'validate'
        self.on_validated()
		
class CarouselImagesItem2(CarouselImagesItem):
    pass
              

class CarouselDoubleImagesItem(CarouselBaseItem): #Double Several Images
    source1 = StringProperty('') # source at init
    source2 = StringProperty('') 
    sources1 = ListProperty('') # all sources
    sources2 = ListProperty('')
    item1 = ObjectProperty(None) # subwidget
    item2 = ObjectProperty(None)
    game_over = BooleanProperty(None)

    def validate(self):
        if self.game_over is True: 
            return
        #print self.item1.source, self.item2.source
        source1 = self.item1.source.split(".")[0][-1]
        source2 = self.item2.source.split(".")[0][-1] 

        print source1, source2  
        if (source1 == source2) and (source1 =='9'):
            print 'you win'
            self.item1.locked = True
            self.item2.locked = True
            self.game_over = True 
            Clock.schedule_once(self.trig_validated, 3)
            return True
        else:
            return False

    def on_touch_up(self, touch):
        super(CarouselBaseItem, self).on_touch_up(touch)   
        x,y = touch.pos
        if self.collide_point(x,y):
            self.validate() 
    
    def trig_validated(self, dt):
        self.parent.parent.current_is_released() 
 

class CarouselVideoItem(CarouselBaseItem): #Single Video
    source = StringProperty('')
    video = ObjectProperty(None)

    def replay(self, instance):
        Logger.info('Video: replay/loop %s' % self.source)
        self.video.play = True

    def do_on_eos(self):
        self.parent.parent.current_is_released()

    """
    def on_touch_down(self, touch):
        return True 
    """
"""
class CarouselDoubleSeveralItem(FloatLayout): #Screen with 2 times Several Images
    app = ObjectProperty(None)
    view = ObjectProperty(None)
    index = NumericProperty(0)
    source = StringProperty('')
"""
class ProductCarousel(Carousel):
    app = ObjectProperty(None)
    view = ObjectProperty(None)
    items = DictProperty(None)

    def on_touch_move(self, touch):
        return

    def current_is_released(self):
        self.load_next()
        Logger.info("Carousel: next, view: %s" % self.view.name)
        Clock.schedule_once(self.play_video,2)

    def play_video(self, dt):
        current = self.current_slide
        # check if current slide is a video player
        # if yes, start video  
        if isinstance(current, CarouselVideoItem):
            current.video.play = True     
    


class ProductLayoutView(BaseScreen):
    path = StringProperty('')
    name = StringProperty('')
    sources = ListProperty([])

    def reset_sources(self):
        files = [ f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path,f)) ]
        #self.sources = files 
        sources = []
        for i in files : 
            e = ['.DS_Store', '.mp6']
            if e[0] in i: continue
            if e[1] in i: continue      
            i = os.path.join(self.path, i)
            sources.append(i)
        self.sources = sources
        Logger.info('Carousel: sources = %s' % sources)
      
    def get_sources_from_path(self, path):
        files = [ f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) ]
        sources = []
        for i in files : 
            e = ['.DS_Store', '.mp6']
            if e[0] in i: continue
            if e[1] in i: continue  
            i = os.path.join(path, i)
            sources.append([i])
        return sources
    """
    def get_sources_from_path2(self, root):
        sources = {}
        subdir = {}  
        for path, subdirs, files in os.walk(root):
            for subdir in subdirs:
                if path not in sources.keys():
                    sources[path] = []
                    print 'subdir=%s' % str(path)
            for name in files:
                index = path#.split('/')[1]
                print index
                parent = sources[index]
                parent.append(name) 
                #print os.path.join(path, name)
                print name
        print sources
    """
    def get_dirlist_from_path(self, path):
        list_dir = os.listdir(path) 
        # remove crap from list_dir
        crap = '.DS_Store'
        try:
            list_dir.remove(crap)
        except:
            pass
        return list_dir    


    def get_video_slide(self, path, sources, slide_index):
                current_file = sources[0]
                j = current_file[0]
                print sources, j  
                # has to be .mp4 
                if not '.mp4' in j:
                    Logger.info('ProductLayoutView: File %s %s %s, NOT A .mp4 file' % (path, sources, j))  
                item = CarouselVideoItem(
                           app = self.app,
                           size_hint = (None, None),
                           size = self.size,
                           view = self,
                           #index = sources.index(j), 
                           source = j,
                           options = {'allow_stretch': True, 'eos': 'loop'}
                           )
                return item
 
    def get_image_slide(self, path, sources, slide_index):
                current_file = sources[0]
                j = current_file[0]
                # single image
                for extension in ['.jpg', '.png']:
                    if not extension in j:
                        Logger.info('ProductLayoutView: File %s %s %s, NOT A jpg, png file' % (path, sources, j))  
                item = CarouselItem(
                           app = self.app,
                           size_hint = (None, None),
                           size = self.size,
                           view = self,
                           #index = sources.index(j), 
                           source = j
                           ) 
                return item

    def get_images_slide(self, path, sources, slide_index):
                current_file = sources[0]
                j = current_file[0]
                # single image
                for extension in ['.jpg', '.png']:
                    if not extension in j:
                        Logger.info('ProductLayoutView: File %s %s %s, NOT A jpg, png file' % (path, sources, j))  
                item = CarouselImagesItem2(
                           app = self.app,
                           size_hint = (None, None),
                           size = self.size,
                           view = self,
                           #index = sources.index(j), 
                           source = j,
                           sources = sources 
                           ) 
                return item

    def get_double_images_slide(self, path, sources1, sources2, slide_index):
                #sources2 = sources2.reverse() #reverse list
                current_file1 = sources1[0]
                current_file2 = sources2[0]
                j1 = current_file1[0]
                j2 = current_file2[0] 
                # single image
                for extension in ['.jpg', '.png']:
                    if (not extension in j1) or (not extension in j2):
                        Logger.info('ProductLayoutView: File %s %s %s %s %s, NOT A jpg, png file' % (path, sources1, sources2, j1, j2))
                  
                item = CarouselDoubleImagesItem(
                           app = self.app,
                           size_hint = (None, None),
                           size = self.size,
                           view = self,
                           #index = sources.index(j), 
                           source1 = j1,
                           source2 = j2,
                           sources1 = sources1,
                           sources2 = sources2   
                           ) 
                return item

    def get_image_lot_slide(self, path, sources, slide_index):
        pass


    def create_content(self):
        dir_list = self.get_dirlist_from_path(self.path)
        #print dir_list 
        #self.reset_sources()
        #print self.sources

        self.carousel = carousel = ProductCarousel(direction='right',
                                                           loop=False,
                                                           app = self.app,
                                                           view = self,
                                                           size_hint = (None, None),
                                                           size = self.size,
                                                           anim_move_duration = 1.5,
                                                           anim_type = 'out_circ',
                                                           min_move = .1    
                                                           )

        for i in dir_list:
            path = os.path.join(self.path, i)
            print path 
            sources = self.get_sources_from_path(path)
            print sources

            slide_index = 0 
			
			# Scénario 
            if i == '01':
              #carousel.items[id] = item = self.get_video_slide(path, sources, slide_index)
				# Accueil médiation
				carousel.items[id] = item = self.get_image_slide(path, sources, slide_index)
            elif i == '02':
				# Video Archéologue
				carousel.items[id] = item = self.get_video_slide(path, sources, slide_index)
				#print 'sources: %s' % sources 
                #sources1 = [k for k in sources if '1_' in k[0]]
                #sources2 = [k for k in sources if '2_' in k[0]]
                #print 'sources1: %s' % sources1, 'sources2: %s' % sources2
                #carousel.items[id] = item = self.get_double_images_slide(path, sources1, sources2, slide_index)
            
            elif i == '03':
				# Choix d'appariement de 2 images : Formes / Matière
 				print 'sources: %s' % sources 
				sources1 = [k for k in sources if '1_' in k[0]]
				sources2 = [k for k in sources if '2_' in k[0]]
				print 'sources1: %s' % sources1, 'sources2: %s' % sources2
				carousel.items[id] = item = self.get_double_images_slide(path, sources1, sources2, slide_index)
            
            elif i == '04':
			    # Vidéo Bingo !
				carousel.items[id] = item = self.get_video_slide(path, sources, slide_index)

            elif i == '05':
				#  Video 
				carousel.items[id] = item = self.get_video_slide(path, sources, slide_index)
             
            elif i == '06':
			    # Choix de l'image de contexte
				carousel.items[id] = item = self.get_images_slide(path, sources, slide_index)
            
            elif i == '07':
			    # Vidéo Bingo !
				carousel.items[id] = item = self.get_video_slide(path, sources, slide_index)

            elif i == '08':
				#  Video 
				carousel.items[id] = item = self.get_video_slide(path, sources, slide_index)
            """
            elif i == '09':
				#  Choix de l'image de cartel 
				carousel.items[id] = item = self.get_images_slide(path, sources, slide_index)

            elif i == '10':
				# Image Crédits
				carousel.items[id] = item = self.get_image_slide(path, sources, slide_index)
            """
            slide_index += 1
            carousel.add_widget(item)
            
        return carousel

    


