import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

from exp_figure import get_series, get_frame, expfigure
from ecdc_figure import ECDCfigure
from SICRD_figure import SICRD_model
from basic_SIR_model import SIRmodel
from testing_SIR_model import SIRTestingmModel

import plotly
import datetime

today_date = datetime.datetime.today().strftime("%m/%d/%Y")

pio.templates.default = "plotly_white"
import pandas as pd
import numpy as np

from scipy.integrate import odeint

bg_color = "#f7f7f5"


colors = [
    "#636EFA",
    "#EF553B",
    "#00CC96",
    "#19D3F3",
    "#FFA15A",
    "#FF6692",
    "#AB63FA",
    "#B6E880",
    "#FF97FF",
    "#FECB52",
    #
    "#636EFA",
    "#EF553B",
    "#00CC96",
    "#19D3F3",
    "#FFA15A",
    "#FF6692",
    "#AB63FA",
    "#B6E880",
    "#FF97FF",
    "#FECB52",
]


import pandas as pd
import numpy as np

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = html.Div(
    style={"background-color": "#deddd9"},
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    html.Div(
                        className="text-center",
                        children=[
                            dbc.Button(
                                "INFO",
                                id="open-centered",
                                color="info",
                                className="btn btn-sm position-fixed mt-2",
                            ),
                            dbc.Modal(
                                [
                                    dbc.ModalBody(
                                        children=[
                                            html.Div(
                                                className="container mb-3",
                                                children=[
                                                    html.H5("What are these figures?"),
                                                    html.Div(
                                                        "These figures are part of a report on the Covid-19 epidemic by students at the Frankfurt School of Finance & Manangement. The complete report and additional information can be found at our Github Repositories:"
                                                    ),
                                                    html.A(
                                                        "Link to the repository with the report",
                                                        href="https://github.com/bernhardkissler/cte_corona_report_",
                                                        target="_blank",
                                                    ),
                                                    html.P(
                                                        "",
                                                        className="container m-0 p-0",
                                                    ),
                                                    html.A(
                                                        "Link to the code for this website",
                                                        href="https://github.com/bernhardkissler/cte_corona_interactive",
                                                        target="_blank",
                                                    ),
                                                ],
                                            ),
                                            html.Div(
                                                children=[
                                                    html.Div(
                                                        html.H5(
                                                            "What do they and their inputs mean?"
                                                        ),
                                                        className="container",
                                                    ),
                                                    html.Div(
                                                        className="container mb-3",
                                                        children=[
                                                            html.H6(
                                                                "Figure A.2 – Cases of Covid-19 and death rates around the world"
                                                            ),
                                                            html.Div(
                                                                "This figure shows cumulative cases and deaths from Covid-19 (both on log axes) in different countries. We added lines indicating special case fatality rates. The idea for the chart came from (Ritchie & Roser, 2020) and the data from the ECDC. An interactive version can be found in the companion website to this report.",
                                                            ),
                                                        ],
                                                    ),
                                                    html.Div(
                                                        className="container mb-3",
                                                        children=[
                                                            html.H6(
                                                                "Figure A.4 – Development of infected populations with exponential growth"
                                                            ),
                                                            html.Div(
                                                                "This figure depicts exponential growth processes of an infected population for similar growth factors. It shows them both on a linear and a logarithmic scale."
                                                            ),
                                                            html.Div(
                                                                className="container mt-1 p-0",
                                                                children=[
                                                                    html.P(
                                                                        children=[
                                                                            "Number of Series: Decide how many series for different growthfactors should be calculated and displayed"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                    html.P(
                                                                        children=[
                                                                            "Minimum value: The smallest growthfactor which should be displayed"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                    html.P(
                                                                        children=[
                                                                            "Maximum value: The highest growthfactor which should be displayed"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                    html.P(
                                                                        children=[
                                                                            "Number of periods: For how many days should the number of infected be calculated"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    html.Div(
                                                        className="container mb-3",
                                                        children=[
                                                            html.H6(
                                                                "Figure A.5 – SIR a basic compartmental model"
                                                            ),
                                                            html.Div(
                                                                "This figure shows a basic epidemiological, compartmental model made up of three compartments. These are Susceptible, infected and recovered people. It simulates a period of approximately a quarter of a year and pro-vides the relative probability of the different compartments."
                                                            ),
                                                            html.Div(
                                                                className="container mt-1 p-0",
                                                                children=[
                                                                    html.P(
                                                                        children=[
                                                                            "Contact rate: Decide how many people any infected person meets per day"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                    html.P(
                                                                        children=[
                                                                            "Probability of infection: Decide how many likely a susceptible person is to be infected when meeting an infected person"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    html.Div(
                                                        className="container mb-3",
                                                        children=[
                                                            html.H6(
                                                                "Figure A.6 – An illustration of different testing strategies in a compartmental model"
                                                            ),
                                                            html.Div(
                                                                "This model includes simple simulations of the insights different testing strategies might provide into the abso-lute number of infected and the prevalence of the disease in the overall population."
                                                            ),
                                                            html.Div(
                                                                className="container mt-1 p-0",
                                                                children=[
                                                                    html.P(
                                                                        children=[
                                                                            "Contact rate: Decide how many people any infected person meets per day"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                    html.P(
                                                                        children=[
                                                                            "Probability of infection: Decide how many likely a susceptible person is to be infected when meeting an infected person"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                    html.P(
                                                                        children=[
                                                                            "Tests per 1000 inhabitants: Decide how many people are tested per day"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                    html.P(
                                                                        children=[
                                                                            "Growth rate of tests: Decide how fast the number of available tests grows"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    html.Div(
                                                        className="container mb-3",
                                                        children=[
                                                            html.H6(
                                                                "Figure A.10 – Triage in the expanded SIR model"
                                                            ),
                                                            html.Div(
                                                                "This figure expands the SIR model from before by two compartments and provides a simplified simulation of the mechanisms behind triage. The most important factors for this are death rates for the critically ill which depend on the availability of ICUs (Beds) steeply."
                                                            ),
                                                            html.Div(
                                                                className="container mt-1 p-0",
                                                                children=[
                                                                    html.P(
                                                                        children=[
                                                                            "Contact rate: Decide how many people any infected person meets per day"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                    html.P(
                                                                        children=[
                                                                            "Probability of infection: Decide how many likely a susceptible person is to be infected when meeting an infected person"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                    html.P(
                                                                        children=[
                                                                            "ICUs per 1000 inhabitants: Decide how ICUs per 1000 inhabitants are available"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                    html.P(
                                                                        children=[
                                                                            "Growth rate of ICUs: Decide how fast the number of available ICUs grows"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                    html.P(
                                                                        children=[
                                                                            "Rate of critical cases: Decide which percentage of ill people get critically ill"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                    html.P(
                                                                        children=[
                                                                            "Death rate for normal cases: Decide which percentage of normal cases die"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                    html.P(
                                                                        children=[
                                                                            "Death rate for critical cases: Decide which percentage of critically ill people die regardless of their treatment in ICUs"
                                                                        ],
                                                                        className="containr m-0 p-0",
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ]
                                    ),
                                    dbc.ModalFooter(
                                        dbc.Button(
                                            "Close",
                                            id="close-centered",
                                            className="ml-auto",
                                        ),
                                    ),
                                ],
                                scrollable=True,
                                id="modal-centered",
                                centered=True,
                                size="lg",
                            ),
                        ],
                    ),
                    width=1,
                ),
                dbc.Col(
                    children=[
                        dbc.Row(
                            dbc.Col(
                                className="col text-center",
                                children=[
                                    html.H4(
                                        className="container pt-3 pb-3 mb-2",
                                        style={"background-color": bg_color},
                                        children=[
                                            "A short Introduction to the Corona-crisis and its epidemiologic background"
                                        ],
                                    ),
                                ],
                            ),
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    className="container pt-1 pb-1 mb-1",
                                                    style={
                                                        "background-color": bg_color
                                                    },
                                                    children=[html.H5("Figure A.2")],
                                                ),
                                                html.Div(
                                                    className="container pt-1 pb-1 mb-2",
                                                    style={
                                                        "background-color": bg_color
                                                    },
                                                    children=[
                                                        dbc.Row(
                                                            [
                                                                dbc.Col([], width=0),
                                                                dbc.Col(
                                                                    [
                                                                        dcc.Graph(
                                                                            figure=ECDCfigure()
                                                                        ),
                                                                    ],
                                                                    width=12,
                                                                ),
                                                            ]
                                                        )
                                                    ],
                                                ),
                                            ]
                                        )
                                    ]
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    className="container pt-1 pb-1 mb-1",
                                                    style={
                                                        "background-color": bg_color
                                                    },
                                                    children=[html.H5("Figure A.4")],
                                                ),
                                                html.Div(
                                                    className="container pt-1 pb-1 mb-2",
                                                    style={
                                                        "background-color": bg_color
                                                    },
                                                    children=[
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    children=[
                                                                        html.Div(
                                                                            className="container",
                                                                            children=[
                                                                                dbc.Label(
                                                                                    "Number of series:"
                                                                                ),
                                                                                dbc.Input(
                                                                                    id="input_exp_incr",
                                                                                    type="number",
                                                                                    placeholder="input increments value",
                                                                                    value=3,
                                                                                    debounce=True,
                                                                                ),
                                                                                dbc.Label(
                                                                                    "Minimum value:"
                                                                                ),
                                                                                dbc.Input(
                                                                                    id="input_exp_min",
                                                                                    type="number",
                                                                                    placeholder="input min value",
                                                                                    value=1.5,
                                                                                    debounce=True,
                                                                                ),
                                                                                dbc.Label(
                                                                                    "Maximum value:"
                                                                                ),
                                                                                dbc.Input(
                                                                                    id="input_exp_max",
                                                                                    type="number",
                                                                                    placeholder="input max value",
                                                                                    value=3,
                                                                                    debounce=True,
                                                                                ),
                                                                                dbc.Label(
                                                                                    "Number of periods:"
                                                                                ),
                                                                                dbc.Input(
                                                                                    id="input_exp_per",
                                                                                    type="number",
                                                                                    placeholder="input per value",
                                                                                    value=10,
                                                                                    debounce=True,
                                                                                ),
                                                                            ],
                                                                        )
                                                                    ],
                                                                    width=3,
                                                                ),
                                                                dbc.Col(
                                                                    dcc.Graph(
                                                                        id="exp_fig",
                                                                    ),
                                                                    width="auto",
                                                                ),
                                                            ]
                                                        )
                                                    ],
                                                ),
                                            ]
                                        ),
                                    ]
                                )
                            ],
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    children=[
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    className="container pt-1 pb-1 mb-1",
                                                    style={
                                                        "background-color": bg_color
                                                    },
                                                    children=[html.H5("Figure A.5")],
                                                ),
                                                html.Div(
                                                    className="container pt-1 pb-1 mb-2",
                                                    style={
                                                        "background-color": bg_color
                                                    },
                                                    children=[
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        html.Div(
                                                                            className="container",
                                                                            children=[
                                                                                dbc.Label(
                                                                                    "Contact rate:"
                                                                                ),
                                                                                dbc.Input(
                                                                                    id="input_A5_contact",
                                                                                    type="number",
                                                                                    placeholder="input contact rate",
                                                                                    value=1.75,
                                                                                    debounce=True,
                                                                                ),
                                                                                dbc.Label(
                                                                                    "Probability of infection:"
                                                                                ),
                                                                                dcc.Slider(
                                                                                    min=0,
                                                                                    max=1,
                                                                                    step=0.01,
                                                                                    value=0.25,
                                                                                    marks={
                                                                                        i: "{}".format(
                                                                                            i
                                                                                        )
                                                                                        for i in np.linspace(
                                                                                            0,
                                                                                            1,
                                                                                            5,
                                                                                        )
                                                                                    },
                                                                                    id="input_A5_prob_inf",
                                                                                ),
                                                                            ],
                                                                        )
                                                                    ],
                                                                    width=3,
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dcc.Graph(
                                                                            id="A5_figure"
                                                                        ),
                                                                    ],
                                                                    width="auto",
                                                                ),
                                                            ]
                                                        )
                                                    ],
                                                ),
                                            ],
                                        )
                                    ],
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    children=[
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    className="container pt-1 pb-1 mb-1",
                                                    style={
                                                        "background-color": bg_color
                                                    },
                                                    children=[html.H5("Figure A.6")],
                                                ),
                                                html.Div(
                                                    className="container pt-1 pb-1 mb-2",
                                                    style={
                                                        "background-color": bg_color
                                                    },
                                                    children=[
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        html.Div(
                                                                            className="container",
                                                                            children=[
                                                                                dbc.Label(
                                                                                    "Contact rate:"
                                                                                ),
                                                                                dbc.Input(
                                                                                    id="input_A6_contact",
                                                                                    type="number",
                                                                                    placeholder="input contact rate",
                                                                                    value=1.75,
                                                                                    debounce=True,
                                                                                ),
                                                                                dbc.Label(
                                                                                    "Probability of infection:"
                                                                                ),
                                                                                dcc.Slider(
                                                                                    min=0,
                                                                                    max=1,
                                                                                    step=0.01,
                                                                                    value=0.25,
                                                                                    marks={
                                                                                        i: "{}".format(
                                                                                            i
                                                                                        )
                                                                                        for i in np.linspace(
                                                                                            0,
                                                                                            1,
                                                                                            5,
                                                                                        )
                                                                                    },
                                                                                    id="input_A6_prob_inf",
                                                                                ),
                                                                                dbc.Label(
                                                                                    "Tests per 1000 inhabitants:"
                                                                                ),
                                                                                dcc.Slider(
                                                                                    min=0,
                                                                                    max=1000,
                                                                                    step=10,
                                                                                    value=100,
                                                                                    marks={
                                                                                        i: "{}".format(
                                                                                            i
                                                                                        )
                                                                                        for i in np.linspace(
                                                                                            0,
                                                                                            1000,
                                                                                            5,
                                                                                        )
                                                                                    },
                                                                                    id="input_A6_no_tests",
                                                                                ),
                                                                                dbc.Label(
                                                                                    "Growth rate of tests:"
                                                                                ),
                                                                                dcc.Slider(
                                                                                    min=0,
                                                                                    max=0.1,
                                                                                    step=0.001,
                                                                                    value=0,
                                                                                    marks={
                                                                                        i: "{}".format(
                                                                                            i.round(
                                                                                                2
                                                                                            )
                                                                                        )
                                                                                        for i in np.linspace(
                                                                                            0,
                                                                                            0.1,
                                                                                            5,
                                                                                        )
                                                                                    },
                                                                                    id="input_A6_growth_tests",
                                                                                ),
                                                                            ],
                                                                        )
                                                                    ],
                                                                    width=3,
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dcc.Graph(
                                                                            id="A6_figure"
                                                                        ),
                                                                    ],
                                                                    width="auto",
                                                                ),
                                                            ]
                                                        )
                                                    ],
                                                ),
                                            ],
                                        )
                                    ],
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    children=[
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    className="container pt-1 pb-1 mb-1",
                                                    style={
                                                        "background-color": bg_color
                                                    },
                                                    children=[html.H5("Figure A.10")],
                                                ),
                                                html.Div(
                                                    className="container pt-1 pb-1 mb-2",
                                                    style={
                                                        "background-color": bg_color
                                                    },
                                                    children=[
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        html.Div(
                                                                            className="container",
                                                                            children=[
                                                                                dbc.Label(
                                                                                    "Contact rate:"
                                                                                ),
                                                                                dbc.Input(
                                                                                    id="input_A10_contact",
                                                                                    type="number",
                                                                                    placeholder="input contact rate",
                                                                                    value=1.75,
                                                                                    debounce=True,
                                                                                ),
                                                                                dbc.Label(
                                                                                    "Probability of infection:"
                                                                                ),
                                                                                dcc.Slider(
                                                                                    min=0,
                                                                                    max=1,
                                                                                    step=0.01,
                                                                                    value=0.25,
                                                                                    marks={
                                                                                        i: "{}".format(
                                                                                            i
                                                                                        )
                                                                                        for i in np.linspace(
                                                                                            0,
                                                                                            1,
                                                                                            5,
                                                                                        )
                                                                                    },
                                                                                    id="input_A10_prob_inf",
                                                                                ),
                                                                                dbc.Label(
                                                                                    "ICUs per 1000 inhabitants:"
                                                                                ),
                                                                                dcc.Slider(
                                                                                    min=0,
                                                                                    max=1000,
                                                                                    step=10,
                                                                                    value=100,
                                                                                    marks={
                                                                                        i: "{}".format(
                                                                                            i
                                                                                        )
                                                                                        for i in np.linspace(
                                                                                            0,
                                                                                            1000,
                                                                                            5,
                                                                                        )
                                                                                    },
                                                                                    id="input_A10_no_beds",
                                                                                ),
                                                                                dbc.Label(
                                                                                    "Growth rate of ICUs:"
                                                                                ),
                                                                                dcc.Slider(
                                                                                    min=0,
                                                                                    max=0.1,
                                                                                    step=0.001,
                                                                                    value=0,
                                                                                    marks={
                                                                                        i: "{}".format(
                                                                                            i.round(
                                                                                                2
                                                                                            )
                                                                                        )
                                                                                        for i in np.linspace(
                                                                                            0,
                                                                                            0.1,
                                                                                            5,
                                                                                        )
                                                                                    },
                                                                                    id="input_A10_growth_beds",
                                                                                ),
                                                                                dbc.Label(
                                                                                    "Rate of critical cases:"
                                                                                ),
                                                                                dcc.Slider(
                                                                                    min=0,
                                                                                    max=1,
                                                                                    step=0.01,
                                                                                    value=0.05,
                                                                                    marks={
                                                                                        i: "{}".format(
                                                                                            i
                                                                                        )
                                                                                        for i in np.linspace(
                                                                                            0,
                                                                                            1,
                                                                                            5,
                                                                                        )
                                                                                    },
                                                                                    id="input_A10_crit_rate",
                                                                                ),
                                                                                dbc.Label(
                                                                                    "Death rate for normal cases:"
                                                                                ),
                                                                                dcc.Slider(
                                                                                    min=0,
                                                                                    max=1,
                                                                                    step=0.01,
                                                                                    value=0.05,
                                                                                    marks={
                                                                                        i: "{}".format(
                                                                                            i
                                                                                        )
                                                                                        for i in np.linspace(
                                                                                            0,
                                                                                            1,
                                                                                            5,
                                                                                        )
                                                                                    },
                                                                                    id="input_A10_death_normal",
                                                                                ),
                                                                                dbc.Label(
                                                                                    "Death rate for critical cases:"
                                                                                ),
                                                                                dcc.Slider(
                                                                                    min=0,
                                                                                    max=1,
                                                                                    step=0.01,
                                                                                    value=0.1,
                                                                                    marks={
                                                                                        i: "{}".format(
                                                                                            i
                                                                                        )
                                                                                        for i in np.linspace(
                                                                                            0,
                                                                                            1,
                                                                                            5,
                                                                                        )
                                                                                    },
                                                                                    id="input_A10_death_crit",
                                                                                ),
                                                                            ],
                                                                        )
                                                                    ],
                                                                    width=3,
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dcc.Graph(
                                                                            id="A10_figure"
                                                                        ),
                                                                    ],
                                                                    width="auto",
                                                                ),
                                                            ]
                                                        )
                                                    ],
                                                ),
                                            ],
                                        )
                                    ],
                                ),
                            ]
                        ),
                    ],
                    width=10,
                ),
                dbc.Col(width=1),
            ]
        )
    ],
)


@app.callback(
    dash.dependencies.Output("modal-centered", "is_open"),
    [
        dash.dependencies.Input("open-centered", "n_clicks"),
        dash.dependencies.Input("close-centered", "n_clicks"),
    ],
    [dash.dependencies.State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output("exp_fig", "figure"),
    [
        dash.dependencies.Input("input_exp_min", "value"),
        dash.dependencies.Input("input_exp_max", "value"),
        dash.dependencies.Input("input_exp_incr", "value"),
        dash.dependencies.Input("input_exp_per", "value"),
    ],
)
def expfigure_containter(exp_min, exp_max, exp_incr, input_exp_per):
    return expfigure(exp_min, exp_max, exp_incr, input_exp_per)


@app.callback(
    dash.dependencies.Output("A5_figure", "figure"),
    [
        dash.dependencies.Input("input_A5_contact", "value"),
        dash.dependencies.Input("input_A5_prob_inf", "value"),
    ],
)
def A5_figure_container(input_A5_contact, input_A5_prob_inf):
    gamma = 1.0 / 4.0  # time normal case till recovery
    return SIRmodel(gamma, input_A5_prob_inf, input_A5_contact, input_A5_contact, 15)


@app.callback(
    dash.dependencies.Output("A6_figure", "figure"),
    [
        dash.dependencies.Input("input_A6_contact", "value"),
        dash.dependencies.Input("input_A6_prob_inf", "value"),
        dash.dependencies.Input("input_A6_no_tests", "value"),
        dash.dependencies.Input("input_A6_growth_tests", "value"),
    ],
)
def A6_figure_container(
    input_A6_contact, input_A6_prob_inf, input_A6_no_tests, input_A6_growth_tests
):
    gamma = 1.0 / 4.0  # time normal case till recovery
    return SIRTestingmModel(
        gamma,
        input_A6_no_tests,
        input_A6_growth_tests,
        input_A6_prob_inf,
        input_A6_contact,
        input_A6_contact,
        15,
    )


@app.callback(
    dash.dependencies.Output("A10_figure", "figure"),
    [
        dash.dependencies.Input("input_A10_contact", "value"),
        dash.dependencies.Input("input_A10_prob_inf", "value"),
        dash.dependencies.Input("input_A10_no_beds", "value"),
        dash.dependencies.Input("input_A10_growth_beds", "value"),
        dash.dependencies.Input("input_A10_crit_rate", "value"),
        dash.dependencies.Input("input_A10_death_normal", "value"),
        dash.dependencies.Input("input_A10_death_crit", "value"),
    ],
)
def A10_figure_container(
    input_A10_contact,
    input_A10_prob_inf,
    input_A10_no_beds,
    input_A10_growth_beds,
    input_A10_crit_rate,
    input_A10_death_normal,
    input_A10_death_crit,
):
    gamma = 1.0 / 4.0  # time normal case till recovery
    rho = 1 / 9.0  # time normal case till death
    # alpha = 0.02  # death rate normal case
    # epsilon = 0.05  # critical rate
    zeta = 1.0 / 5.0  # time critical case till recovery
    eta = 1.0 / 7.0  # time critical case till death
    # teta = 0.1  # death rate critical case
    return SICRD_model(
        gamma,
        rho,
        input_A10_death_normal,
        input_A10_crit_rate,
        zeta,
        eta,
        input_A10_death_crit,
        input_A10_prob_inf,
        input_A10_contact,
        input_A10_contact,
        0,
        input_A10_no_beds,
        input_A10_growth_beds,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
