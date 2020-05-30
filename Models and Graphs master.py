# In[2]:


import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import datetime

today_date = datetime.datetime.today().strftime("%m/%d/%Y")

pio.templates.default = "plotly_white"
import pandas as pd
import numpy as np

from scipy.integrate import odeint


# ### Intensive care units
#
# https://de.statista.com/statistik/daten/studie/1111057/umfrage/intensivbetten-je-einwohner-in-ausgewaehlten-laendern/#professional

# In[7]:


def icufigure():
    countries = [
        "Germany (2017)  ",
        "Austria (2018)  ",
        "US (2018)  ",
        "France (2018)  ",
        "Spain (2017)  ",
        "Italy (2020)  ",
        "Denmark (2014)  ",
        "Ireland (2016)  ",
    ]
    icu_number = [33.9, 28.9, 25.8, 16.3, 9.7, 8.9, 7.8, 5]
    fig = go.Figure(
        data=[
            go.Bar(
                y=countries,
                x=icu_number,
                text=icu_number,
                textposition="outside",
                orientation="h",
                marker=dict(color=colors[0],),
            )
        ]
    )
    fig.update_layout(
        title="Number of intensive care units per 100,000 inhabitants by country",
        yaxis=dict(showgrid=False),
        xaxis=dict(showgrid=False),
    )
    return fig


fig = icufigure()
fig.show()
# fig.write_image("ICUdata.svg", width=700, height=400)


# In[10]:


def RKIfigure():
    headers = [
        "Week",
        "Number of tests",
        "Number of positive tests",
        "positive tests as a percentage",
        "number of reporting laboratiories",
    ]
    data = [
        #     ["Bis einschließlich KW", "week 10", 124.716, 3.892, 3.1, 90],
        ["Week 11", 127_457, 7_582, 5.9, 114],
        ["Week 12", 348_619, 23_820, 6.8, 152],
        ["Week 13", 361_515, 31_414, 8.7, 151],
        ["Week 14", 408_348, 36_885, 9, 154],
        ["Week 15", 379_233, 30_728, 8.1, 163],
        ["Week 16", 330_027, 21_993, 6.7, 167],
        ["Week 17", 361_999, 18_052, 5, 177],
        ["Week 18", 325_259, 12_585, 3.9, 174],
        ["Week 19", 402_044, 10_746, 2.7, 181],
        ["Week 20", 425_842, 7_060, 1.7, 176],
    ]
    df = pd.DataFrame(data, columns=headers)
    df["Test growth"] = df["Number of tests"].pct_change() * 100

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df["Week"],
            y=df["Test growth"],
            mode="markers+lines+text",
            #             text=df["Test growth"].round(0),
            showlegend=False,
            line=dict(color=colors[1]),
            #             textposition="top center"
        ),
        secondary_y=True,
    )
    fig.add_trace(
        go.Bar(
            x=df["Week"],
            y=df["Number of tests"],
            #             text=df["Number of tests"],
            #             textposition="outside",
            #             textfont=dict(color=colors[0]),
            showlegend=False,
            marker=dict(color=colors[0],),
        ),
        secondary_y=False,
    )
    fig.update_layout(title="Number of tests performed in Germany per week",)
    fig.update_yaxes(
        title_text="Number of weekly tests",
        showgrid=False,
        secondary_y=False,
        color=colors[0],
    )
    fig.update_yaxes(
        title_text="Change in percent",
        showgrid=False,
        zeroline=False,
        secondary_y=True,
        color=colors[1],
    )

    return fig


fig = RKIfigure()
fig.show()
# fig.write_image("RKIdata.svg", width=700, height=400)
