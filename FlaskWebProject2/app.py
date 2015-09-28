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
from bokeh.models.
from bokeh.models.widgets import HBox, Paragraph, Slider, VBox
import math


app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


def make_layout():
    # set up some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 8, 7, 3]

    data = dict(
        x = x,
        y = y,
    )

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
        var f = cb_obj.get('value')
        
        source.trigger('change');
    """)


    plot1 = VBox(
        children=[
            p,
            Slider(orientation="horizontal", start=1, end=5, value=1, step=1, name="freq", callback = callback)
        ]
    )


    layout = HBox(
        children = [plot1]
    )

    return layout

@app.route('/')
def index():  

    layout = make_layout()
    script, div = components(layout)

    return render_template('index.html', script = script, div = div)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug = True)
