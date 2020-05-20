import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = html.Div(
    [
        html.Div(
            [
                html.H6(
                    "A short Introduction to the Corona-crisis and its epidemiologic background"
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Input(
                            id="input_exp_min",
                            type="number",
                            placeholder="input min value",
                            value=2,
                            debounce=True,
                        ),
                        dcc.Input(
                            id="input_exp_max",
                            type="number",
                            placeholder="input max value",
                            value=2,
                            debounce=True,
                        ),
                        dcc.Input(
                            id="input_exp_incr",
                            type="number",
                            placeholder="input increments value",
                            value=1,
                            debounce=True,
                        ),
                        dcc.Input(
                            id="input_exp_per",
                            type="number",
                            placeholder="input per value",
                            value=10,
                            debounce=True,
                        ),
                        dcc.Graph(id="exp_fig"),
                    ],
                    id="exp_growth_content",
                    className="col-md-12 px-0",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label(
                            [
                                html.Span("social distancing"),
                                dcc.Input(
                                    id="inp_mod_rho",
                                    type="number",
                                    min=0,
                                    max=1,
                                    step=0.01,
                                    value=1,
                                    debounce=True,
                                ),
                            ],
                        ),
                        html.Label(
                            [
                                html.Span("contact rate"),
                                dcc.Input(
                                    id="inp_mod_beta",
                                    type="number",
                                    min=0,
                                    max=5,
                                    step=0.01,
                                    value=1.75,
                                    debounce=True,
                                ),
                            ],
                        ),
                        html.Label(
                            [
                                html.Span("prob of infection"),
                                dcc.Input(
                                    id="inp_mod_teta",
                                    type="number",
                                    min=0,
                                    max=1,
                                    step=0.1,
                                    value=1,
                                    debounce=True,
                                ),
                            ],
                        ),
                        html.Label(
                            [
                                html.Span("inv of incubation time"),
                                dcc.Input(
                                    id="inp_mod_alpha",
                                    type="number",
                                    min=0,
                                    max=1,
                                    step=0.01,
                                    value=0.2,
                                    debounce=True,
                                ),
                            ],
                        ),
                        html.Label(
                            [
                                html.Span("inv of infectious period after symptoms"),
                                dcc.Input(
                                    id="inp_mod_gamma",
                                    type="number",
                                    min=0,
                                    max=1,
                                    step=0.01,
                                    value=0.5,
                                    debounce=True,
                                ),
                            ],
                        ),
                        html.Label(
                            [
                                html.Span("inv of infectious period before symptoms"),
                                dcc.Input(
                                    id="inp_mod_zeta",
                                    type="number",
                                    min=0,
                                    max=1,
                                    step=0.01,
                                    value=0.17,
                                    debounce=True,
                                ),
                            ],
                        ),
                        html.Label(
                            [
                                html.Span("death rate"),
                                dcc.Input(
                                    id="inp_mod_epsilon",
                                    type="number",
                                    min=0,
                                    max=1,
                                    step=0.01,
                                    value=0.02,
                                    debounce=True,
                                ),
                            ],
                        ),
                        html.Label(
                            [
                                html.Span("rate of symptomatic disease"),
                                dcc.Input(
                                    id="inp_mod_eta",
                                    type="number",
                                    min=0,
                                    max=1,
                                    step=0.01,
                                    value=0.7,
                                    debounce=True,
                                ),
                            ],
                        ),
                        html.Label(
                            [
                                html.Span("immunity constant"),
                                dcc.Input(
                                    id="inp_mod_delta",
                                    type="number",
                                    min=0,
                                    max=1,
                                    step=0.01,
                                    value=0.01,
                                    debounce=True,
                                ),
                            ],
                        ),
                        html.Label(
                            [
                                html.Span("length of observation"),
                                dcc.Input(
                                    id="inp_mod_t_max",
                                    type="number",
                                    min=0,
                                    max=500,
                                    step=1,
                                    value=100,
                                    debounce=True,
                                ),
                            ],
                        ),
                        html.Label(
                            [
                                html.Span("time steps"),
                                dcc.Input(
                                    id="inp_mod_dt",
                                    type="number",
                                    min=0,
                                    max=10,
                                    step=0.1,
                                    value=0.1,
                                    debounce=True,
                                ),
                            ],
                        ),
                        html.Label(
                            [
                                html.Span("total pop"),
                                dcc.Input(
                                    id="inp_mod_N",
                                    type="number",
                                    value=1000,
                                    debounce=True,
                                ),
                            ],
                        ),
                        html.Label(
                            [
                                html.Span("No of initially infected"),
                                dcc.Input(
                                    id="inp_mod_I",
                                    type="number",
                                    value=1,
                                    debounce=True,
                                ),
                            ],
                        ),
                    ],
                    # className="col md-6 px-0",
                ),
                html.Div(
                    [dcc.Graph(id="mod_fig"),],
                    # className="col md-6 px-0",
                ),
            ],
            className="row",
        ),
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
    exp_fig = go.Figure()
    for i in vals_cont:
        exp_fig.add_trace(
            go.Scatter(
                x=df["index"],
                y=df["cum_{}".format(i)],
                mode="lines",
                name="cum. value with growth-factor of {}".format(i),
                line_shape="spline",
            )
        )
        exp_fig.add_trace(
            go.Scatter(
                x=df["index"],
                y=df["ind_{}".format(i)],
                mode="lines",
                name="ind. value with growth-factor of {}".format(i),
                line_shape="spline",
                line=dict(dash="dash"),
            )
        )
    return exp_fig


def SECIRD_model(init_vals, params, t):
    S_0, E_0, C_0, I_a_0, I_s_0, R_0, D_0 = init_vals
    test_sum = [S_0 + E_0 + C_0 + I_a_0 + I_s_0 + R_0 + D_0]
    S, E, C, I_a, I_s, R, D = [S_0], [E_0], [C_0], [I_a_0], [I_s_0], [R_0], [D_0]
    alpha, beta, gamma, delta, epsilon, eta, zeta, rho, teta = params
    beta = rho * beta
    dt = t[1] - t[0]
    for _ in t[1:]:
        #         print(R[-1])
        next_S = (
            S[-1]
            - beta * teta * S[-1] * (I_a[-1] + I_s[-1] + C[-1]) * dt
            + delta * R[-1] * dt
        )
        next_E = (
            E[-1]
            + (beta * teta * S[-1] * (I_a[-1] + I_s[-1] + C[-1]) - alpha * E[-1]) * dt
        )
        next_C = C[-1] + (alpha * E[-1] - zeta * C[-1]) * dt
        next_I_a = I_a[-1] + (zeta * C[-1] * (1 - eta) - (gamma * I_a[-1])) * dt
        next_I_s = I_s[-1] + (zeta * C[-1] * (eta) - (gamma * I_s[-1])) * dt
        next_R = (
            R[-1] + (gamma * (1 - epsilon) * (I_a[-1] + I_s[-1]) - delta * R[-1]) * dt
        )
        next_D = D[-1] + (gamma * (epsilon) * (I_a[-1] + I_s[-1])) * dt
        next_test_sum = next_S + next_E + next_C + next_I_a + next_I_s + next_R + next_D

        S.append(next_S)
        E.append(next_E)
        C.append(next_C)
        I_a.append(next_I_a)
        I_s.append(next_I_s)
        R.append(next_R)
        D.append(next_D)
        test_sum.append(next_test_sum)

    return (
        pd.DataFrame(np.stack([S, E, C, I_a, I_s, R, D, test_sum]).T)
        .rename(
            columns={
                0: "Susceptibles",
                1: "Exposed",
                2: "Carrier",
                3: "Infective_asymptomatic",
                4: "Infective_symptomatic",
                5: "Recovered",
                6: "Dead",
                7: "test_sum",
            }
        )
        .reset_index()
    )


@app.callback(
    dash.dependencies.Output("mod_fig", "figure"),
    [
        dash.dependencies.Input("inp_mod_rho", "value"),
        dash.dependencies.Input("inp_mod_beta", "value"),
        dash.dependencies.Input("inp_mod_teta", "value"),
        dash.dependencies.Input("inp_mod_alpha", "value"),
        dash.dependencies.Input("inp_mod_gamma", "value"),
        dash.dependencies.Input("inp_mod_zeta", "value"),
        dash.dependencies.Input("inp_mod_epsilon", "value"),
        dash.dependencies.Input("inp_mod_eta", "value"),
        dash.dependencies.Input("inp_mod_delta", "value"),
        dash.dependencies.Input("inp_mod_t_max", "value"),
        dash.dependencies.Input("inp_mod_dt", "value"),
        dash.dependencies.Input("inp_mod_N", "value"),
        dash.dependencies.Input("inp_mod_I", "value"),
    ],
)
def update_mod_fig(
    inp_mod_rho,
    inp_mod_beta,
    inp_mod_teta,
    inp_mod_alpha,
    inp_mod_gamma,
    inp_mod_zeta,
    inp_mod_epsilon,
    inp_mod_eta,
    inp_mod_delta,
    inp_mod_t_max,
    inp_mod_dt,
    inp_mod_N,
    inp_mod_I,
):
    SECIRD_vals = [
        1 - inp_mod_I / inp_mod_N,
        inp_mod_I / inp_mod_N,
        0,
        0,
        0,
        0,
        0,
    ]  # normalized inputs
    SECIRD_params = [
        inp_mod_alpha,
        inp_mod_beta,
        inp_mod_gamma,
        inp_mod_delta,
        inp_mod_epsilon,
        inp_mod_eta,
        inp_mod_zeta,
        inp_mod_rho,
        inp_mod_teta,
    ]
    SECIRD_t = np.linspace(0, inp_mod_t_max, int(inp_mod_t_max / inp_mod_dt) + 1)
    SECIRD_results = SECIRD_model(SECIRD_vals, SECIRD_params, SECIRD_t)

    mod_fig = go.Figure()
    for col in SECIRD_results.columns:
        if (
            col
            != "index"
            #                     and
            #                     (col != "test_sum")
        ):
            mod_fig.add_trace(
                go.Scatter(
                    x=SECIRD_results["index"],
                    y=SECIRD_results[col],
                    mode="lines",
                    name=col,
                    line_shape="spline",
                )
            )
    return mod_fig


if __name__ == "__main__":
    app.run_server(debug=True)
