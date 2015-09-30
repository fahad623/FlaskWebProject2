"""
This file demonstrates a bokeh applet, which can be viewed directly
on a bokeh-server. See the README.md file in this directory for
instructions on running.
"""
from flask import Flask, render_template, request, redirect, url_for
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import HoverTool, BoxSelectTool
from bokeh.models.widgets import DataTable
from bokeh.models import Plot, ColumnDataSource
from bokeh.models import CustomJS
from bokeh.models.widgets import HBox, Paragraph, Slider, VBox, Dropdown
import math
from bokeh.properties import Instance


class SlidersApp():



    def input_change(self):
        self.plot.title = "somne plot"

    @classmethod
    def create(cls):
        

        obj = cls()

        x = [1, 2, 3, 4, 5]
        y = [6, 7, 8, 7, 3]

        data = dict(
            x = x,
            y = y,
        )

        obj.source = ColumnDataSource(data=data)
        obj.plot = figure(plot_width=600, plot_height=600)
        obj.plot.circle('x', 'y', source = obj.source, fill_color="white", size=8)
        obj.slider_freq = Slider(orientation="horizontal", start=1, end=5, value=1, step=1, name="freq1", title = "Frequency")
        obj.slider_freq.on_change('value', obj, 'input_change')

        obj.layout = HBox()
        obj.layout.children.append(obj.plot)
        obj.layout.children.append(obj.slider_freq)

        return obj.layout


def make_sliders():
    app = SlidersApp.create()
    return app


from flask import Flask, render_template, request, redirect, url_for
from bokeh.embed import components

flask_app = Flask(__name__)


@flask_app.route('/')
def index():  
    slider_app = make_sliders()
    script, div = components(slider_app)

    return render_template('index.html', script = script, div = div)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    flask_app.run(HOST, PORT, debug = True)