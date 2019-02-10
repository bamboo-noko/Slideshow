import kivy

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, NumericProperty
import os
import random
import configparser
from glob import glob
from os.path import join, dirname

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class RotatedImage(Image):
    angle = NumericProperty(0)

class SlideshowController(FloatLayout):

    load_dir = ""
    files = []
    input_wid = ObjectProperty(None)
    input_interval_wid = ObjectProperty(None)
    input_repeat_wid = ObjectProperty(None)
    label_current_time_wid = ObjectProperty(None)
    label_current_num_wid = ObjectProperty(None)
    button_stop_wid = ObjectProperty(None)
    box_layout_wid = ObjectProperty(None)
    checkbox_flip_wid = ObjectProperty(None)
    rotated_image = ""
    clock_event = ""

    isStart = False
    isStop = False
    index = 0

    def __init__(self, **kwargs):
        super(SlideshowController, self).__init__(**kwargs)
        self.rotated_image = RotatedImage(source="./resources/imgs/black.png")
        self.box_layout_wid.add_widget(self.rotated_image)
        # inifile = configparser.ConfigParser()
        # inifile.read("./config.ini", "UTF-8")
        # # self.input_wid.text = inifile.get("settings", "dir")
        # # self.input_interval_wid.text = inifile.get("settings", "interval")
        # # self.input_repeat_wid.text = inifile.get("settings", "repeat")

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.input_wid.text = path
        self.dismiss_popup()

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
        self.clock_event = Clock.schedule_interval(self.callback, 1)
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
        self.rotated_image.source = "./resources/imgs/black.png"
        self.label_current_num_wid.text = "0"
        self.label_current_time_wid.text = "0"
        self.clock_event.cancel()
        self.rotated_image.angle = 0

        self.isStart = False
        self.isStop = False
        self.update_widget_state()

    def change_image(self):
        if self.checkbox_flip_wid.active :
            self.rotated_image.angle = 0 if random.randint(0, 1) == 0 else 180

        self.rotated_image.source = self.files[self.index]
        self.rotated_image.reload()
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
        self.clock_event.cancel()
        self.clock_event()
        self.change_image()
        self.init_time()

    def stop(self):
        if not self.isStart:
            return

        if self.isStop:
            self.clock_event()
            self.isStop = False
            self.button_stop_wid.text = "Stop"
        else:
            self.clock_event.cancel()
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
            self.input_wid.disabled = True
            self.input_interval_wid.disabled = True
            self.input_repeat_wid.disabled = True
            self.checkbox_flip_wid.disabled = True

        else:
            self.button_stop_wid.text = "Stop"
            self.input_wid.disabled = False
            self.input_interval_wid.disabled = False
            self.input_repeat_wid.disabled = False
            self.checkbox_flip_wid.disabled = False


class SlideshowApp(App):

    def build(self):
        root = self.root
        return SlideshowController()

Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == '__main__':
    SlideshowApp().run()
