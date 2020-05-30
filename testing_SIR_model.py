from SIR_helper_functions import contact_rate, beta, test_rate
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
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


def deriv(
    y,
    t,
    N,
    prob_infection,
    init_contact_rate,
    end_contact_rate,
    inflection_point,
    gamma,
):
    S, I, R = y
    dSdt = (
        -beta(t, prob_infection, init_contact_rate, end_contact_rate, inflection_point)
        * S
        * (I)
        / N
    )
    dIdt = beta(
        t, prob_infection, init_contact_rate, end_contact_rate, inflection_point
    ) * S * (I) / N - (gamma * I)
    dRdt = gamma * I
    return (dSdt, dIdt, dRdt)


def SIRTestingmModel(
    gamma,
    tests_per_thousand,
    scaling_factor,
    prob_infection,
    init_contact_rate,
    end_contact_rate,
    inflection_point,
):
    N = 1
    init_infected = 0.000001
    S0, I0, R0 = (
        N - init_infected,
        init_infected,
        0,
    )  # initial conditions: one infected, rest susceptible
    t = np.linspace(0, 100, 1000)  # Grid of time points (in days)

    y0 = S0, I0, R0  # Initial conditions vector
    S, I, R = odeint(
        deriv,
        y0,
        t,
        args=(
            N,
            prob_infection,
            init_contact_rate,
            end_contact_rate,
            inflection_point,
            gamma,
        ),
    ).T
    SIRD_odeint = pd.DataFrame({"Susceptible": S, "Infected": I, "Recovered": R,})
    SIRD_odeint["total"] = SIRD_odeint.sum(axis=1)
    SIRD_odeint["days"] = SIRD_odeint.reset_index()["index"].div(10)

    #     Add test statistics for random testing
    SIRD_odeint_random = pd.DataFrame()
    #     SIRD_odeint_random["Infected"] = SIRD_odeint["Infected"]
    SIRD_odeint_random["Tested overall - random"] = (
        test_rate(SIRD_odeint["days"], N, tests_per_thousand, scaling_factor)
        * SIRD_odeint["total"]
    )
    SIRD_odeint_random["Tested positive - random"] = SIRD_odeint[
        "Infected"
    ] * test_rate(SIRD_odeint["days"], N, tests_per_thousand, scaling_factor)
    SIRD_odeint_random["Tested negative - random"] = SIRD_odeint[
        "Susceptible"
    ] * test_rate(
        SIRD_odeint["days"], N, tests_per_thousand, scaling_factor
    ) + SIRD_odeint[
        "Recovered"
    ] * test_rate(
        SIRD_odeint["days"], N, tests_per_thousand, scaling_factor
    )
    SIRD_odeint_random["Implied prevalence - random"] = SIRD_odeint_random[
        "Tested positive - random"
    ] / (
        SIRD_odeint_random["Tested positive - random"]
        + SIRD_odeint_random["Tested negative - random"]
    )
    # Add test statistics for biased testing
    SIRD_odeint_biased = pd.DataFrame()
    #     SIRD_odeint_biased["Infected"] = SIRD_odeint["Infected"]
    SIRD_odeint_biased["Tested overall - biased"] = (
        test_rate(SIRD_odeint["days"], N, tests_per_thousand, scaling_factor)
        * SIRD_odeint["total"]
    )
    SIRD_odeint_biased["Tested positive - biased"] = SIRD_odeint.apply(
        lambda row: min(
            test_rate(row["days"], N, tests_per_thousand, scaling_factor),
            row["Infected"],
        )
        * 0.6,
        axis=1,
    )
    SIRD_odeint_biased["Tested negative - biased"] = SIRD_odeint.apply(
        lambda row: test_rate(row["days"], N, tests_per_thousand, scaling_factor)
        * row["total"]
        - min(
            test_rate(row["days"], N, tests_per_thousand, scaling_factor),
            row["Infected"],
        )
        * 0.6,
        axis=1,
    )
    SIRD_odeint_biased["Implied prevalence - biased"] = SIRD_odeint_biased[
        "Tested positive - biased"
    ] / (
        SIRD_odeint_biased["Tested positive - biased"]
        + SIRD_odeint_biased["Tested negative - biased"]
    )
    #       create figure
    fig = make_subplots(
        rows=3,
        cols=1,
        x_title="Days",
        y_title="Relative probability",
        subplot_titles=("Basic Model", "Random testing", "Cluster testing"),
    )
    #     Subfig 1
    graph_colors = [colors[0], colors[1], colors[4]]
    test_graph_colors = [colors[6], colors[7], colors[8], colors[9]]
    for i, col in enumerate(SIRD_odeint):
        if col in ["Susceptible", "Infected", "Recovered"]:
            fig.add_trace(
                go.Scatter(
                    x=SIRD_odeint["days"],
                    y=SIRD_odeint[col],
                    mode="lines",
                    name=col,
                    line=dict(color=graph_colors[i]),
                    legendgroup="Basic SIR model",
                ),
                row=1,
                col=1,
            )
    # SUbfig 2
    fig.add_trace(
        go.Scatter(
            x=SIRD_odeint["days"],
            y=SIRD_odeint["Infected"],
            mode="lines",
            name="Infected",
            legendgroup="Random testing",
            line=dict(color=graph_colors[1]),
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=SIRD_odeint["days"],
            y=SIRD_odeint["total"],
            mode="none",
            name="total",
            showlegend=False,
        ),
        row=2,
        col=1,
    )
    for i, col in enumerate(SIRD_odeint_random):
        fig.add_trace(
            go.Scatter(
                x=SIRD_odeint["days"],
                y=SIRD_odeint_random[col],
                mode="lines",
                name=col,
                line=dict(color=test_graph_colors[i], dash="dot"),
                legendgroup="Random testing",
            ),
            row=2,
            col=1,
        )
    # SUbfig 3
    fig.add_trace(
        go.Scatter(
            x=SIRD_odeint["days"],
            y=SIRD_odeint["Infected"],
            mode="lines",
            name="Infected",
            legendgroup="Biased testing",
            line=dict(color=graph_colors[1]),
        ),
        row=3,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=SIRD_odeint["days"],
            y=SIRD_odeint["total"],
            mode="none",
            name="total",
            showlegend=False,
        ),
        row=3,
        col=1,
    )
    for i, col in enumerate(SIRD_odeint_biased):
        fig.add_trace(
            go.Scatter(
                x=SIRD_odeint["days"],
                y=SIRD_odeint_biased[col],
                mode="lines",
                name=col,
                line=dict(color=test_graph_colors[i], dash="dot"),
                legendgroup="Biased testing",
            ),
            row=3,
            col=1,
        )
    #     axes update
    fig.update_layout(
        title="Testing in the SIR model",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    return fig
