from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.uix.button import Button

class CloseButton(Button):
    pass

class CloseButtonLayout(Factory.AnchorLayout):
    basescreen = ObjectProperty(None)

class BaseScreen(Screen):
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.add_widget(self.create_content())
        #self.add_close_button()

    def close(self, *args):
        self.app.hide_screenview(self)

    def add_close_button(self):
        self.layout = layout = CloseButtonLayout(basescreen = self)
        btn = layout.ids.close_button
        btn.bind(on_release=self.close)
        self.add_widget(layout)

    def create_content(self):
        raise NotImplementedError('You need to create a method "create_content" in {!r}'.format(
            self.__class__))

