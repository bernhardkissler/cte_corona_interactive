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

import plotly
import datetime

today_date = datetime.datetime.today().strftime("%m/%d/%Y")

pio.templates.default = "plotly_white"
import pandas as pd
import numpy as np

from scipy.integrate import odeint

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
    [
        dbc.Row(
            children=[
                dbc.Col(width=1),
                dbc.Col(
                    children=[
                        dbc.Row(
                            dbc.Col(
                                html.H3(
                                    "A short Introduction to the Corona-crisis and its epidemiologic background"
                                ),
                            ),
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(html.H5("Figure ...")),
                                                dbc.CardBody(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        dbc.Label(
                                                                            "Choose the time of infectiousness"
                                                                        ),
                                                                        dbc.Input(
                                                                            id="input_sir_contact",
                                                                            type="number",
                                                                            placeholder="input contact rate",
                                                                            value=1.75,
                                                                            debounce=True,
                                                                        ),
                                                                        dbc.Label(
                                                                            "Choose a probability of infection"
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
                                                                            id="input_sir_prob_inf",
                                                                        ),
                                                                    ],
                                                                    width=3,
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dcc.Graph(
                                                                            id="SICRD_figure"
                                                                        ),
                                                                    ],
                                                                    width="auto",
                                                                ),
                                                            ]
                                                        )
                                                    ]
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
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(html.H5("Figure ...")),
                                                dbc.CardBody(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col([], width=3),
                                                                dbc.Col(
                                                                    [
                                                                        dcc.Graph(
                                                                            figure=ECDCfigure()
                                                                        ),
                                                                    ],
                                                                    width="auto",
                                                                ),
                                                            ]
                                                        )
                                                    ]
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
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(html.H5("Figure A1")),
                                                dbc.CardBody(
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                children=[
                                                                    dbc.Label(
                                                                        "Choose the minimum value"
                                                                    ),
                                                                    dbc.Input(
                                                                        id="input_exp_min",
                                                                        type="number",
                                                                        placeholder="input min value",
                                                                        value=2,
                                                                        debounce=True,
                                                                    ),
                                                                    dbc.Label(
                                                                        "Choose the maximum value"
                                                                    ),
                                                                    dbc.Input(
                                                                        id="input_exp_max",
                                                                        type="number",
                                                                        placeholder="input max value",
                                                                        value=2,
                                                                        debounce=True,
                                                                    ),
                                                                    dbc.Label(
                                                                        "Choose how many series should be displayed"
                                                                    ),
                                                                    dbc.Input(
                                                                        id="input_exp_incr",
                                                                        type="number",
                                                                        placeholder="input increments value",
                                                                        value=1,
                                                                        debounce=True,
                                                                    ),
                                                                    dbc.Label(
                                                                        "Choose how many periods the calculations should be made"
                                                                    ),
                                                                    dbc.Input(
                                                                        id="input_exp_per",
                                                                        type="number",
                                                                        placeholder="input per value",
                                                                        value=10,
                                                                        debounce=True,
                                                                    ),
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
                                                ),
                                            ]
                                        ),
                                    ]
                                )
                            ],
                        ),
                        # dbc.Row(
                        #     [
                        #         dbc.Col(
                        #             [
                        #                 dbc.Card(
                        #                     [
                        #                         dbc.CardHeader(html.H5("Figure ...")),
                        #                         dbc.CardBody(
                        #                             [
                        #                                 dbc.Row(
                        #                                     [
                        #                                         dbc.Col(
                        #                                             [
                        #                                                 dbc.Label(
                        #                                                     "Choose a contact rate"
                        #                                                 ),
                        #                                                 dbc.Input(
                        #                                                     id="input_sir_contact",
                        #                                                     type="number",
                        #                                                     placeholder="input contact rate",
                        #                                                     value=1.75,
                        #                                                     debounce=True,
                        #                                                 ),
                        #                                                 dbc.Label(
                        #                                                     "Choose a probability of infection"
                        #                                                 ),
                        #                                                 dcc.Slider(
                        #                                                     min=0,
                        #                                                     max=1,
                        #                                                     step=0.01,
                        #                                                     value=0.2,
                        #                                                     marks={
                        #                                                         i: "{}".format(
                        #                                                             i
                        #                                                         )
                        #                                                         for i in np.linspace(
                        #                                                             0,
                        #                                                             1,
                        #                                                             5,
                        #                                                         )
                        #                                                     },
                        #                                                     id="input_sir_prob_inf",
                        #                                                 ),
                        #                                                 dbc.Label(
                        #                                                     "Choose the duration of infection"
                        #                                                 ),
                        #                                                 dbc.Input(
                        #                                                     id="input_sir_removed",
                        #                                                     type="number",
                        #                                                     placeholder="input duration of infection",
                        #                                                     value=1
                        #                                                     / 14,
                        #                                                     debounce=True,
                        #                                                 ),
                        #                                                 dbc.Label(
                        #                                                     "Choose the test rate"
                        #                                                 ),
                        #                                                 dcc.Slider(
                        #                                                     min=0,
                        #                                                     max=1,
                        #                                                     step=0.01,
                        #                                                     value=0.2,
                        #                                                     marks={
                        #                                                         i: "{}".format(
                        #                                                             i
                        #                                                         )
                        #                                                         for i in np.linspace(
                        #                                                             0,
                        #                                                             1,
                        #                                                             5,
                        #                                                         )
                        #                                                     },
                        #                                                     id="input_sir_tests",
                        #                                                 ),
                        #                                                 dbc.Label(
                        #                                                     "Choose number of periods"
                        #                                                 ),
                        #                                                 dbc.Input(
                        #                                                     id="input_sir_t_max",
                        #                                                     type="number",
                        #                                                     placeholder="input number of periods",
                        #                                                     value=365
                        #                                                     / 2,
                        #                                                     debounce=True,
                        #                                                 ),
                        #                                                 dbc.Label(
                        #                                                     "Show tests?"
                        #                                                 ),
                        #                                                 dbc.RadioItems(
                        #                                                     options=[
                        #                                                         {
                        #                                                             "label": "yes",
                        #                                                             "value": True,
                        #                                                         },
                        #                                                         {
                        #                                                             "label": "no",
                        #                                                             "value": False,
                        #                                                         },
                        #                                                     ],
                        #                                                     value=True,
                        #                                                     id="input_sir_show_tests",
                        #                                                 ),
                        #                                             ],
                        #                                             width=3,
                        #                                         ),
                        #                                         dbc.Col(
                        #                                             [
                        #                                                 dcc.Graph(
                        #                                                     id="sir_test_fig"
                        #                                                 )
                        #                                             ],
                        #                                             width="auto",
                        #                                         ),
                        #                                     ]
                        #                                 )
                        #                             ]
                        #                         ),
                        #                     ]
                        #                 )
                        #             ]
                        #         ),
                        #     ]
                        # ),
                    ],
                    width=10,
                ),
                dbc.Col(width=1),
            ]
        )
    ]
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
    dash.dependencies.Output("SICRD_figure", "figure"),
    [
        dash.dependencies.Input("input_sir_contact", "value"),
        dash.dependencies.Input("input_sir_prob_inf", "value"),
    ],
)
def SICRD_figure_container(input_sir_contact, input_sir_inf):
    gamma = 1.0 / 4.0  # time normal case till recovery
    rho = 1 / 9.0  # time normal case till death
    alpha = 0.02  # death rate normal case
    epsilon = 0.05  # critical rate
    zeta = 1.0 / 5.0  # time critical case till recovery
    eta = 1.0 / 7.0  # time critical case till death
    teta = 0.1  # death rate critical case
    return SICRD_model(
        gamma,
        rho,
        alpha,
        epsilon,
        zeta,
        eta,
        teta,
        input_sir_inf,
        input_sir_contact,
        5,
        15,
        30,
        0,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
