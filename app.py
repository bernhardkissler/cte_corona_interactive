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
                                            [
                                                dbc.CardHeader(html.H5("Figure ...")),
                                                dbc.CardBody(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col([], width=3),
                                                                dbc.Col(
                                                                    [], width="auto"
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
                                                                dcc.Graph(id="exp_fig"),
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
                                                                            "Choose a contact rate"
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
                                                                        dbc.Input(
                                                                            id="input_sir_prob_inf",
                                                                            type="number",
                                                                            placeholder="input probability of infection",
                                                                            value=0.2,
                                                                            debounce=True,
                                                                        ),
                                                                        dbc.Label(
                                                                            "Choose the duration of infection"
                                                                        ),
                                                                        dbc.Input(
                                                                            id="input_sir_removed",
                                                                            type="number",
                                                                            placeholder="input duration of infection",
                                                                            value=1
                                                                            / 14,
                                                                            debounce=True,
                                                                        ),
                                                                        dbc.Label(
                                                                            "Choose the test rate"
                                                                        ),
                                                                        dbc.Input(
                                                                            id="input_sir_tests",
                                                                            type="number",
                                                                            placeholder="input test rate",
                                                                            value=0.1,
                                                                            debounce=True,
                                                                        ),
                                                                        dbc.Label(
                                                                            "Choose number of periods"
                                                                        ),
                                                                        dbc.Input(
                                                                            id="input_sir_t_max",
                                                                            type="number",
                                                                            placeholder="input number of periods",
                                                                            value=365
                                                                            / 2,
                                                                            debounce=True,
                                                                        ),
                                                                        dbc.Label(
                                                                            "Show tests?"
                                                                        ),
                                                                        dbc.RadioItems(
                                                                            options=[
                                                                                {
                                                                                    "label": "yes",
                                                                                    "value": True,
                                                                                },
                                                                                {
                                                                                    "label": "no",
                                                                                    "value": False,
                                                                                },
                                                                            ],
                                                                            value=True,
                                                                            id="input_sir_show_tests",
                                                                        ),
                                                                    ],
                                                                    width=3,
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dcc.Graph(
                                                                            id="sir_test_fig"
                                                                        )
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


############################################################################################### Second graphs beginning here
def testing_errors_model(init_values, change_rates, periods):
    """
    inputs:
    initial values for outputs, rates    
    outputs:
    tot_population, inf_population, test_pos_population, test_neg_population, rem_population, implied_inf_population, period
    """
    (
        sus_pop_0,
        inf_pop_0,
        rem_pop_0,
        test_pos_pop_0,
        test_neg_pop_0,
        implied_inf_pop_0,
    ) = init_values
    (sus_pop, inf_pop, rem_pop, test_pos_pop, test_neg_pop, implied_inf_pop,) = (
        [sus_pop_0],
        [inf_pop_0],
        [rem_pop_0],
        [test_pos_pop_0],
        [test_neg_pop_0],
        [implied_inf_pop_0],
    )
    tot_pop = [(sus_pop_0 + inf_pop_0 + rem_pop_0)]
    r_contact, r_prob_inf, r_removed, r_tests = change_rates
    dt = periods[1] - periods[0]
    for _ in periods[1:]:
        n_tot_pop = sus_pop[-1] + inf_pop[-1] + rem_pop[-1]
        n_sus_pop = (
            sus_pop[-1] - (r_contact * r_prob_inf * sus_pop[-1] * inf_pop[-1]) * dt
        )
        n_inf_pop = (
            inf_pop[-1]
            + (r_contact * r_prob_inf * sus_pop[-1] * inf_pop[-1]) * dt
            - (inf_pop[-1] * r_removed) * dt
        )
        n_rem_pop = rem_pop[-1] + (inf_pop[-1] * r_removed) * dt
        #### end of ode_1
        if False:
            #         _ < 21:
            n_test_pos_pop = 0
            n_test_neg_pop = 0
            n_implied_inf_pop = 0
        else:
            n_test_pos_pop = (
                #             test_pos_pop[-1]
                +n_inf_pop
                * r_tests
                * dt
            )
            n_test_neg_pop = (
                #                 test_neg_pop[-1]
                +n_sus_pop * r_tests * dt
                + n_rem_pop * r_tests * dt
            )
            n_implied_inf_pop = +n_test_pos_pop / (n_test_neg_pop + n_test_pos_pop)
        ### update of lists
        tot_pop.append(n_tot_pop)
        sus_pop.append(n_sus_pop)
        inf_pop.append(n_inf_pop)
        test_pos_pop.append(n_test_pos_pop)
        test_neg_pop.append(n_test_neg_pop)
        rem_pop.append(n_rem_pop)
        implied_inf_pop.append(n_implied_inf_pop)
    return (
        pd.DataFrame(
            np.stack(
                [
                    tot_pop,
                    sus_pop,
                    inf_pop,
                    rem_pop,
                    test_pos_pop,
                    test_neg_pop,
                    implied_inf_pop,
                ]
            ).T
        ).rename(
            columns={
                0: "Total Population",
                1: "Susceptible",
                2: "Infected",
                3: "Removed",
                4: "Tested positive",
                5: "Tested negative",
                6: "Implied infected",
            }
        )
        #         .reset_index()
    )


@app.callback(
    dash.dependencies.Output("sir_test_fig", "figure"),
    [
        dash.dependencies.Input("input_sir_contact", "value"),
        dash.dependencies.Input("input_sir_prob_inf", "value"),
        dash.dependencies.Input("input_sir_removed", "value"),
        dash.dependencies.Input("input_sir_tests", "value"),
        dash.dependencies.Input("input_sir_t_max", "value"),
        dash.dependencies.Input("input_sir_show_tests", "value"),
    ],
)
def SIR_model_graph(r_contact, r_prob_inf, r_removed, r_tests, t_max, show_tests):
    #     define number of periods
    dt = 1
    periods = np.linspace(0, t_max, int(t_max / dt) + 1)
    #     unpack initial population values
    tot_pop = 1000
    inf_pop = 1
    init_values = [1 - inf_pop / tot_pop, inf_pop / tot_pop, 0, 0, 0, 0]
    #     pack change rates
    change_rates = [r_contact, r_prob_inf, r_removed, r_tests]
    #     generate df
    testing_errors_model_results = testing_errors_model(
        init_values, change_rates, periods
    )

    fig = go.Figure()
    for col in testing_errors_model_results.reset_index().columns:
        if show_tests == True:
            if col in ["Tested positive", "Tested negative", "Implied infected"]:
                fig.add_trace(
                    go.Scatter(
                        x=testing_errors_model_results.reset_index()["index"],
                        y=testing_errors_model_results[col],
                        mode="lines",
                        name=col,
                        legendgroup="secondary testing",
                        line=dict(dash="dash")
                        #                 line_shape="spline",
                    )
                )
            elif (col != "index") & (col != "Total Population"):
                fig.add_trace(
                    go.Scatter(
                        x=testing_errors_model_results.reset_index()["index"],
                        y=testing_errors_model_results[col],
                        mode="lines",
                        name=col,
                        legendgroup="primary ode",
                    )
                )
            fig.update_layout(
                title="Random, representative testing in the SIR model",
                xaxis_title="Days",
                yaxis_title="Percentage of total population",
            )
        else:
            if col in ["Tested positive", "Tested negative", "Implied infected"]:
                pass
            elif (col != "index") & (col != "Total Population"):
                fig.add_trace(
                    go.Scatter(
                        x=testing_errors_model_results.reset_index()["index"],
                        y=testing_errors_model_results[col],
                        mode="lines",
                        name=col,
                        legendgroup="primary ode",
                    )
                )
            fig.update_layout(
                title="SIR model",
                xaxis_title="Days",
                yaxis_title="Percentage of total population",
            )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
