# encoding: utf-8

import npyscreen
import requests
import json

import matplotlib
matplotlib.use('module://drawilleplot')
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib._pylab_helpers import Gcf

API_URL = 'http://studiatozlo.pythonanywhere.com/api/'



class PlotForm(npyscreen.Form):
    def __init__(self, *args, **kwargs):
        self.currencies = kwargs.pop('currencies')
        super(PlotForm, self).__init__(*args, **kwargs)

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
       y, x = self.useable_space ()
       self.start_at        = self.add(npyscreen.TitleDateCombo, name='Start date')
       self.end_at          = self.add(npyscreen.TitleDateCombo, name='End date')
       self.base            = self.add(npyscreen.TitleSelectOne,max_height=5, name="Base",values = self.currencies, scroll_exit=True)
       self.symbol          = self.add(npyscreen.TitleSelectOne, max_height=5, name="Symbol",values = self.currencies, scroll_exit=True)
       self.build           = self.add(npyscreen.ButtonPress, name='Confirm', when_pressed_function=self.display_plot)
       self.plot            = self.add(npyscreen.MultiLineEdit, editable=False)
    

    def get_rates(self, base, target, start_at, end_at):
        try:
            response = requests.get(API_URL+'rates/?base={}&target={}&start_at={}&end_at={}'.format(base, target, start_at, end_at))
            return response.text
        except:
            self.spawn_notify_popup("Sorry, it shouldn't happen", "Server error")



    def build_plot(self, rates, dates):  
            data = ""
            self.plot.value = ""
            figure(num=None, figsize=(6, 4), dpi=200, facecolor='w', edgecolor='k')
            plt.plot(rates, dates)
            for manager in Gcf.get_all_fig_managers():
                canvas = manager.canvas
                canvas.draw()
                string = canvas.to_txt()
                data+=string
            plt.close()
            self.plot.value = data
            self.plot.display()

    def display_plot(self):
        if self.validate():
            _base = self.base.get_selected_objects()[0]
            _symbol = self.symbol.get_selected_objects()[0]

            resp = self.get_rates(_base, _symbol, self.start_at.value, self.end_at.value)
            hist_data = json.loads(resp)
        
            rates = []
            dates = []
            
            for value in hist_data:    
                rates.append(value['date'])
                dates.append(value['exchange_rate'])
            self.build_plot(rates, dates)



    def validate(self):
        if self.base.value and self.symbol.value and self.start_at.value and self.end_at.value:
            return True
        else:
            self.spawn_notify_popup("Don't leave empty fields", "Form error")
            return False

    def spawn_notify_popup(self, msg, title):
        npyscreen.notify_confirm(msg, title= title)

class App(npyscreen.NPSAppManaged):

    def onStart(self):
       self.addForm('MAIN', PlotForm, name='Exchange Rate Viewer', currencies = self.get_currencies(), height=50)

    @staticmethod
    def get_currencies():
        try:
            reaponse = requests.get(API_URL+'currencies/')
            return reaponse.json()
        except:
            self.spawn_notify_popup("Sorry, can't get required data", "Server error")

def run():
    app = App()
    app.run()

if __name__ == "__main__":
    run()

