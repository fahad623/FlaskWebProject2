
from flask import Flask, render_template, request, redirect, url_for
from bokeh.embed import components
from bokeh.resources import Resources
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import HBox, Slider, VBox
import math

app = Flask(__name__)

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
    p = figure(plot_width=600, plot_height=600)
    p.circle('x', 'y', source = source, fill_color="white", size=8)
    layout = HBox(
        children = [p]
    )

    return layout

@app.route('/')
def index():  

    layout = make_layout()
    script, div = components(layout)
    bokeh = Resources(mode="inline")

    return render_template('index1.html', bokeh = bokeh, script = script, div = div)

@app.route("/data")
def data():
    pass

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug = True)
