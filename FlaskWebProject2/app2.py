

from bokeh.plotting import figure
from bokeh.models import Plot, ColumnDataSource
from bokeh.properties import Instance
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
from bokeh.models.widgets import HBox, VBox, Slider

from flask import Flask, render_template, request, redirect, url_for
from bokeh.embed import components

app = Flask(__name__)


class EventHandler:
    def input_change(self):
        a = 8
        print "test"

eventHandler = EventHandler()



def input_change1():
    test = True;

@app.route('/')
def index():  
    slider_freq = Slider(orientation="horizontal", start=1, end=5, value=1, step=1, name="freq1", title = "Frequency")
    slider_freq.on_change('value', eventHandler, 'input_change')

    layout = HBox(
        children = [slider_freq]
    )
    script, div = components(layout)

    return render_template('index.html', script = script, div = div)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)