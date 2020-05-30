from SIR_helper_functions import contact_rate, beta
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


def SIRmodel(
    gamma, prob_infection, init_contact_rate, end_contact_rate, inflection_point,
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

    #       create figure
    fig = make_subplots(rows=1, cols=1, x_title="Days", y_title="Relative probability",)
    graph_colors = [colors[0], colors[1], colors[4]]
    #     Subfig 1
    for i, col in enumerate(SIRD_odeint.columns):
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

    #     axes update
    fig.update_layout(
        title="Basic SIR model",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    return fig
