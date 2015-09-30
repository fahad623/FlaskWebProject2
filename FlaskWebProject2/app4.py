"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template, request, redirect, url_for
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import HoverTool, BoxSelectTool
from bokeh.models.widgets import DataTable
from bokeh.models import ColumnDataSource
from bokeh.models import CustomJS
from bokeh.models.widgets import HBox, Paragraph, Slider, VBox, Dropdown
from bokeh.io import vform
import math
import threading
import time

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

class EventHandler():
    def input_change(self):
        a = 8

eventHandler = EventHandler()

source = None

def make_layout():
    # set up some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 8, 7, 3]

    data = dict(
        x = x,
        y = y,
    )
    global source
    # create a column data source for the plots to share
    source = ColumnDataSource(data=data)

    # create a new plot with figure
    p = figure(plot_width=600, plot_height=600)

    # add both a line and circles on the same plot
    #p.line(x, y, line_width=2)
    p.circle('x', 'y', source = source, fill_color="white", size=8)

    p.outline_line_width = 7
    p.outline_line_alpha = 0.3
    p.outline_line_color = "navy"

    p.xaxis.axis_label = "Temperature"
    p.axis.major_label_text_color = "orange"
    p.xaxis.major_label_orientation = math.pi/4
    p.yaxis.major_label_orientation = "vertical"

    # change just some things about the x-axes
    p.xaxis.axis_label = "Temp"
    p.xaxis.axis_line_width = 3
    p.xaxis.axis_line_color = "red"

    # change just some things about the y-axes
    p.yaxis.axis_label = "Pressure"
    p.yaxis.major_label_text_color = "orange"
    p.yaxis.major_label_orientation = "vertical"

    p.add_tools(BoxSelectTool(), HoverTool())

    callback = CustomJS(args=dict(source=source), code="""
        var data = source.get('data');
        y = data['y']
        y[0] = 8        
        source.trigger('change');
        """)

    slider_freq = Slider(orientation="horizontal", start=1, end=5, value=1, step=1, name="freq1", title = "Frequency", callback = callback)
    
    plot1 = VBox(
        children=[
            p,
            slider_freq
        ]
    )

    layout = HBox(
        children = [plot1]
    )

    return layout


def worker():
    """thread worker function"""
    global source
    while True:
        time.sleep(2)
        source.data['y'][0] +=1

@app.route('/')
def index():  

    layout = make_layout()
    layout.setup_events
    script, div = components(layout)

    t = threading.Thread(target=worker)        
    t.start()

    return render_template('index.html', script = script, div = div)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
