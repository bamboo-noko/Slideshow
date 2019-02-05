import kivy

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window

import os
import random
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
    button_stop_wid = ObjectProperty(None)
    event = ""

    isStart = False
    isStop = False
    index = 0

    def callback(self, dt):
        self.count_down()
        if (int(self.label_current_time_wid.text) is not 0):
            return

        self.calc_num()
        if not self.is_next():
            self.end()
            return

        self.change_image()
        self.init_time()

    def start(self):
        if not self.validation_check():
            return

        files = glob(join(self.input_wid.text, '*'))
        self.files = list(filter(self.check_ext, files))
        if len(self.files) <= 0:
            return

        random.shuffle(self.files)
        self.isStart = True
        self.change_image()
        self.init_time()
        self.label_current_num_wid.text = "1"
        self.event = Clock.schedule_interval(self.callback, 1)
        self.update_widget_state()

    def check_ext(self, x: str) -> bool:
        if os.path.splitext(x)[1] == ".png":
            return True
        if os.path.splitext(x)[1] == ".jpg":
            return True
        if os.path.splitext(x)[1] == ".gif":
            return True
        if os.path.splitext(x)[1] == ".bmp":
            return True

        return False

    def count_down(self):
        self.label_current_time_wid.text = \
            str(int(self.label_current_time_wid.text) - 1)

    def calc_num(self):
        self.label_current_num_wid.text = \
            str(int(self.label_current_num_wid.text) + 1)

    def is_next(self):
        return int(self.label_current_num_wid.text) <= \
            int(self.input_repeat_wid.text)

    def end(self):
        self.image_wid.source = "./resources/imgs/black.png"
        self.label_current_num_wid.text = "0"
        self.label_current_time_wid.text = "0"
        self.event.cancel()

        self.isStart = False
        self.isStop = False
        self.update_widget_state()

    def change_image(self):
        self.image_wid.source = self.files[self.index]
        self.image_wid.reload()
        self.index += 1
        if self.index > len(self.files) - 1:
            self.index = 0

    def init_time(self):
        self.label_current_time_wid.text = self.input_interval_wid.text

    def next(self):
        if not self.isStart:
            return

        self.calc_num()
        if not self.is_next():
            self.end()
            return

        self.isStop = False
        self.button_stop_wid.text = "Stop"
        self.event.cancel()
        self.event()
        self.change_image()
        self.init_time()

    def stop(self):
        if not self.isStart:
            return

        if self.isStop:
            self.event()
            self.isStop = False
            self.button_stop_wid.text = "Stop"
        else:
            self.event.cancel()
            self.isStop = True
            self.button_stop_wid.text = "Resume"

    def validation_check(self):
        if not (os.path.exists(self.input_wid.text)):
            return False

        if not (os.path.isdir(self.input_wid.text)):
            return False

        if not (self.input_interval_wid.text.isdecimal()):
            return False

        if not (self.input_repeat_wid.text.isdecimal()):
            return False

        if (int(self.input_interval_wid.text) <= 0):
            return False

        if (int(self.input_repeat_wid.text) <= 0):
            return False

        if self.isStart:
            return False

        return True

    def update_widget_state(self):
        if self.isStart:
            self.input_wid.readonly = True
            self.input_interval_wid.readonly = True
            self.input_repeat_wid.readonly = True

        else:
            self.button_stop_wid.text = "Stop"
            self.input_wid.readonly = False
            self.input_interval_wid.readonly = False
            self.input_repeat_wid.readonly = False


class SlideshowApp(App):

    def build(self):
        return SlideshowController()


if __name__ == '__main__':
    SlideshowApp().run()
