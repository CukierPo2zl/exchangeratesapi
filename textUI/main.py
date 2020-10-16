from __future__ import division
from asciimatics.effects import BannerText, Print, Scroll
from asciimatics.renderers import ColourImageFile, FigletText, ImageFile
from asciimatics.scene import Scene
from asciimatics.screen import Screen
import sys
from asciimatics.widgets import Frame, DropdownList, Layout, Divider, Button, DatePicker, TextBox, Widget
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import requests

# from sympy import symbols
# from sympy.plotting.textplot import textplot_str
import matplotlib
matplotlib.use('module://drawilleplot')
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib._pylab_helpers import Gcf

API_URL = 'http://studiatozlo.pythonanywhere.com/api/currencies/'


form_data = {"plot": ""}

class ListView(Frame):
    def __init__(self, screen, currencies, form):
        super(ListView, self).__init__(screen,
                                       screen.height,
                                       screen.width,
                                       hover_focus=True,
                                       data = form_data,
                                       can_scroll=False,
                                       has_border=False,
                                       has_shadow = True,
                                       title="Exchange Rate Viewer")

        self._form = form

        self._currencies = currencies

        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())
        layout.add_widget(DatePicker("Start at:", "start_at"))
        layout.add_widget(DatePicker("End at:", "end_at"))
        layout.add_widget(DropdownList(
            name = "currency",
            label = "Select currency",
            options=  self._currencies,
            on_change=self._on_change
            ))

        controlls_layout = Layout([1,1,1,1])
        self.add_layout(controlls_layout)
        controlls_layout.add_widget(Button("Confirm", self._ok), 1)
        controlls_layout.add_widget(Button("Quit", self._quit), 2)

        end_header = Layout([100])
        self.add_layout(end_header)
        end_header.add_widget(Divider())

        # ploting = Layout([100], fill_frame=True)
        # self.add_layout(ploting)
        # ploting.add_widget(TextBox(
        #      Widget.FILL_FRAME, "", "plot", as_string=True, line_wrap=True))

        self.fix()


    def _ok(self):
        self.save()

        plot = ""
        figure(num=None, figsize=(6, 4), dpi=80, facecolor='w', edgecolor='k')

        plt.plot(['asd', 'dfsd', 'dfgdf', 'sdfsd'],[1, 2, 3, 4])

        for manager in Gcf.get_all_fig_managers():
            canvas = manager.canvas
            canvas.draw()
            string = canvas.to_txt()
            plot+=string

        plt.close()
        self._form["plot"] = str(plot)

        raise NextScene("Plot")



    def _on_change(self):
        self.save()



    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class PlotView(Frame):
    def __init__(self, screen, form):
        super(PlotView, self).__init__(screen,
                                      screen.height,
                                      screen.width,
                                      has_border = False,
                                      data = form_data,
                                      title="Exchange Rate Viewer")

        self._form = form

        controlls_layout = Layout([1,1,1,1])
        self.add_layout(controlls_layout)
        controlls_layout.add_widget(Button("X", self._quit), 3)
        layout = Layout([100])
        self.add_layout(layout)
        self._tb = TextBox(
             Widget.FILL_FRAME, "", "plot", as_string=True, line_wrap=True)
        layout.add_widget(self._tb)
        self.fix()


    def _quit(self):
        self._form["plot"] = " "
        super(PlotView, self).reset()
        raise NextScene("Main")



last_scene = None

def welcome_screen(screen):
    effects = [
        Print(screen, ImageFile("globe.gif", screen.height - 2, colours=screen.colours),
              0,
              stop_frame=10),
              Print(screen,
              FigletText("exchange rates",
                         font='banner3'),
              screen.height//2-3,
              colour=2, bg=7 if screen.unicode_aware else 0),
    ]
    return effects


def format_currencies(currencies):
    tmp = []
    i=0
    for currency in currencies:
        i+=1
        tmp.append((currency, i))
    return tmp




def ui(screen, scene):
    reaponse = requests.get(API_URL)
    supported_currencies = format_currencies(reaponse.json())

    scenes = [
        Scene(welcome_screen(screen)),
        Scene([ListView(screen, supported_currencies, form_data)], -1, name="Main"),
        Scene([PlotView(screen, form_data)], -1, name="Plot"),
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

if __name__ == "__main__":
    while True:
        try:
            Screen.wrapper(ui, catch_interrupt=True, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
