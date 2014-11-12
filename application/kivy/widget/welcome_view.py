# -*- coding: utf-8 -*-

from widget.basescreen import BaseScreen

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, DictProperty, ListProperty, NumericProperty, StringProperty 
#from kivy.logger import Logger



class WelcomeLayout(FloatLayout):
    app = ObjectProperty(None)
    view = ObjectProperty(None)



class WelcomeLayoutView(BaseScreen):

    def create_content(self):

        self.main_layout = WelcomeLayout(app = self.app,
                                    view = self,
                                    size_hint = (None, None),
                                    size = self.size
                                    )
        return self.main_layout



