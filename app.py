import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

colors = [
    "rgb(31, 119, 180)",
    "rgb(255, 127, 14)",
    "rgb(44, 160, 44)",
    "rgb(214, 39, 40)",
    "rgb(148, 103, 189)",
    "rgb(140, 86, 75)",
    "rgb(227, 119, 194)",
    "rgb(127, 127, 127)",
    "rgb(188, 189, 34)",
    "rgb(23, 190, 207)",
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
                                                            dcc.Graph(id="exp_fig"),
                                                            width="auto",
                                                        ),
                                                    ]
                                                )
                                            )
                                        ),
                                    ]
                                )
                            ],
                        ),
                    ],
                    width=10,
                ),
                dbc.Col(width=1),
            ]
        )
    ]
)


def get_series(t, i):
    """
    takes in the initial number of infected (i); the number of periods (t) in and returns an exponential 
    daily growth and running sum of cases given that nobody dies.
    """
    p = 0
    x = []
    c = []
    for z in range(t + 1):
        p += i ** z
        x.append(p)
        c.append(i ** z)
    return (x, c)


def get_frame(t, vals):
    """
    takes in an array of initialy infected (vals) and numbe rof periods (t) and returns a df with all
    initial vals as columns and growth and running total per period as rows.
    """
    df = pd.DataFrame()
    for i in vals:
        data = (
            pd.DataFrame(get_series(t, i))
            .transpose()
            .rename(columns={0: "cum_{}".format(i), 1: "ind_{}".format(i)})
        )
        df = pd.concat([df, data], axis=1, join="outer", ignore_index=False)
    return df.reset_index()


@app.callback(
    dash.dependencies.Output("exp_fig", "figure"),
    [
        dash.dependencies.Input("input_exp_min", "value"),
        dash.dependencies.Input("input_exp_max", "value"),
        dash.dependencies.Input("input_exp_incr", "value"),
        dash.dependencies.Input("input_exp_per", "value"),
    ],
)
def update_exp_fig(exp_min, exp_max, exp_incr, input_exp_per):
    """
    takes in the inputs and returns an updated graph
    """
    vals_cont = np.linspace(exp_min, exp_max, exp_incr)
    df = get_frame(input_exp_per, vals_cont)
    exp_fig = make_subplots(
        rows=1, cols=2, subplot_titles=("Linear scale", "Log scale")
    )
    for i, val in enumerate(vals_cont):
        exp_fig.add_trace(
            go.Scatter(
                x=df["index"],
                y=df["cum_{}".format(val)],
                mode="lines",
                name="Growth factor of {}".format(val),
                line_shape="spline",
                legendgroup="lin",
                line=dict(color=colors[i]),
            ),
            row=1,
            col=1,
        )
    for i, val in enumerate(vals_cont):
        exp_fig.add_trace(
            go.Scatter(
                x=df["index"],
                y=df["cum_{}".format(val)],
                mode="lines",
                name="Growth factor of {}".format(val),
                line_shape="spline",
                legendgroup="log",
                showlegend=False,
                line=dict(color=colors[i]),
            ),
            row=1,
            col=2,
        )
    exp_fig.update_layout(
        title="Exponential growth of infected population (cumulative sum)",
        yaxis_title="Number of infected",
        showlegend=True,
    )
    exp_fig.update_yaxes(type="log", row=1, col=2)
    exp_fig.update_xaxes(title="Number of periods", row=1, col=1)
    exp_fig.update_xaxes(title="Number of periods", row=1, col=2)
    return exp_fig


if __name__ == "__main__":
    app.run_server(debug=True)
