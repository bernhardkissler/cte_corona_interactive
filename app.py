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
                dbc.Col(width=1),
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
                                                    children=[html.H5("Figure A2")],
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
                                                    children=[html.H5("Figure A3")],
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
                                                    children=[html.H5("Figure A5")],
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
                                                    children=[html.H5("Figure A6")],
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
                                                                                    "Number of tests per 1000 inhabitants:"
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
                                                    children=[html.H5("Figure A10")],
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
                                                                                dbc.Label(
                                                                                    "Number of ICUs per 1000 inhabitants:"
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
