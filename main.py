import kivy

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.factory import Factory

import os
from random import randint
from glob import glob
from os.path import join, dirname


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SlideshowController(FloatLayout):
    load_dir = ""
    files = []
    image_wid = ObjectProperty(None)
    loadfile = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load directory", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def change_image(self, dt):
        self.image_wid.source = self.files[randint(0, len(self.files)-1)]
        self.image_wid.reload()

    def start(self):
        self.open_dir()
        self.image_wid.source = self.files[randint(0, len(self.files)-1)]
        self.image_wid.reload()
        Clock.schedule_interval(self.change_image, 5)

    def open_dir(self):
        log = "load_dir:" + self.load_dir
        Logger.info(log)
        self.files = glob(join(self.load_dir, '*'))

    def load(self, path, filename):
        self.load_dir = path
        self.dismiss_popup()


class SlideshowApp(App):

    def build(self):
        return SlideshowController()


Factory.register('SlideshowController', cls=SlideshowController)
Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    SlideshowApp().run()