import kivy

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty

import os
from random import randint
from glob import glob
from os.path import join, dirname


class SlideshowController(FloatLayout):
    load_dir = ""
    files = []
    image_wid = ObjectProperty(None)
    input_wid = ObjectProperty(None)
    input_interval_wid = ObjectProperty(None)
    input_repeat_wid = ObjectProperty(None)
    label_current_time_wid = ObjectProperty(None)
    label_current_num_wid = ObjectProperty(None)
    event = ""

    isStart = False

    def callback(self, dt):
        self.count_down()
        if (int(self.label_current_time_wid.text) is not 0):
            return

        self.label_current_num_wid.text = str(int(self.label_current_num_wid.text) + 1)
        if(int(self.label_current_num_wid.text) > int(self.input_repeat_wid.text)):
            self.end()
            return

        self.change_image()
        self.init_time()

    def count_down(self):
        self.label_current_time_wid.text = str(int(self.label_current_time_wid.text) - 1)
    
    def init_time(self):
        self.label_current_time_wid.text = self.input_interval_wid.text

    def change_image(self):
        self.image_wid.source = self.files[randint(0, len(self.files)-1)]
        self.image_wid.reload()

    def start(self):
        if not self.validation_check():
            return

        isStart = True
        self.files = glob(join(self.input_wid.text, '*'))
        self.change_image()
        self.init_time()
        self.label_current_num_wid.text = "1"
        self.event = Clock.schedule_interval(self.callback, 1)

        self.update_widget_state()
        Logger.info("State:start")

    def end(self):
        self.image_wid.source = "./resources/imgs/black.png"
        self.label_current_num_wid.text = "0"
        self.event.cancel()
        Logger.info("State:end")

    def validation_check(self):
        if not (os.path.exists(self.input_wid.text)):
            return False

        if not (os.path.isdir(self.input_wid.text)):
            return False

        if not (self.input_interval_wid.text.isdecimal()):
            return False

        if not (self.input_repeat_wid.text.isdecimal()):
            return False

        return True

    def update_widget_state(self):
        pass


class SlideshowApp(App):

    def build(self):
        return SlideshowController()


if __name__ == '__main__':
    SlideshowApp().run()