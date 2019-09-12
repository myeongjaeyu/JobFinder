import collections
import os

import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.offline import plot
from wordcloud import WordCloud


def counting_frequency(data):
    counted_words = collections.Counter(data).most_common()
    return counted_words


def draw_var_chart(data):
    x = list()
    y = list()
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
        width=800,
        height=1000,
        margin=dict(
            l=60,
            r=10,
            b=10,
            t=10,
            pad=4
        ),
        font=dict(size=14),
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
        width=1600,
        height=2000,
        colormap=matplotlib.cm.tab20b
    )
    wordcloud = wordcloud.generate(' '.join(data))
    plt.figure(figsize=(20, 16))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(os.getcwd() + save, bbox_inches='tight')
    plt.clf()
