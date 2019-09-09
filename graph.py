import plotly.graph_objects as go
from plotly.offline import plot
import urllib.request
import matplotlib
import matplotlib.pyplot as plt
import squarify
from wordcloud import WordCloud
import collections
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime

import requests
import os

def counting_frequency(data):
    counted_words = collections.Counter(data).most_common(100)
    return counted_words


def draw_var_chart(data):
    x = list()
    y = list()
    width = list()
    for key, value in data:
        x.insert(0, value)
        y.insert(0, key)
    trace1 = go.Bar(
        x=x,
        y=y,
        text=x,
        textposition='outside',
        orientation='h',
        marker_color='#696969',
    )
    layout = go.Layout(
        autosize=False,
        width=800,
        height=1000,
        font=dict(
            size=14
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    plot_data = [trace1]
    figure = go.Figure(data=plot_data, layout=layout)
    plot_div = plot(figure, output_type='div', include_plotlyjs=False)
    return plot_div

def word_cloud(data, save):
    wordcloud = WordCloud(
        max_font_size=500,
        background_color="white",
        width=2000,
        height=2400,
        colormap=matplotlib.cm.RdGy
    )
    wordcloud = wordcloud.generate(' '.join(data))
    plt.figure(figsize=(24, 20))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(os.getcwd() + save)

def draw_treemap(data):
    fig = go.Figure()
    keys = list()
    values = list()
    for key, value in data:
        values.insert(0, value)
        keys.insert(0, key)

    x = 0.
    y = 0.
    width = 100.
    height = 100.

    normed = squarify.normalize_sizes(values, width, height)
    rects = squarify.squarify(normed, x, y, width, height)

    # Choose colors from http://colorbrewer2.org/ under "Export"
    color_brewer = ['#42926b', '#394b41', '#9cb0a4', ' #1d1d35',
                    '#0e8dbe', '#005b88', '#3784e1', '#cf634d'] * 10
    shapes = []
    annotations = []
    counter = 0

    for r, key, val, color in zip(rects, keys, values, color_brewer):
        shapes.append(
            dict(
                type='rect',
                x0=r['x'],
                y0=r['y'],
                x1=r['x'] + r['dx'],
                y1=r['y'] + r['dy'],
                line=dict(width=2),
                fillcolor=color
            )
        )
        annotations.append(
            dict(
                x=r['x'] + (r['dx'] / 2),
                y=r['y'] + (r['dy'] / 2),
                text=key,
                showarrow=False
            )
        )

    # For hover text
    fig.add_trace(go.Scatter(
        x=[r['x'] + (r['dx'] / 2) for r in rects],
        y=[r['y'] + (r['dy'] / 2) for r in rects],
        text=[str(v) for v in keys],
        mode='lines+markers+text',
    ))

    fig.update_layout(
        height=700,
        width=700,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        shapes=shapes,
        annotations=annotations,
        hovermode='closest'
    )

    fig.show()
