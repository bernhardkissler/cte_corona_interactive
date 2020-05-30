from SIR_helper_functions import contact_rate, beta, beds
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

# gamma = 1.0 / 4.0  # time normal case till recovery
# rho = 1 / 9.0  # time normal case till death
# alpha = 0.02  # death rate normal case
# epsilon = 0.05  # critical rate
# zeta = 1.0 / 5.0  # time critical case till recovery
# eta = 1.0 / 7.0  # time critical case till death
# teta = 0.1  # death rate critical case


def deriv(
    y,
    t,
    N,
    prob_infection,
    init_contact_rate,
    end_contact_rate,
    inflection_point,
    beds_per_thousand,
    scaling_factor,
    gamma,
    rho,
    alpha,
    epsilon,
    zeta,
    eta,
    teta,
):
    S, I, C, R, D = y
    dSdt = (
        -beta(t, prob_infection, init_contact_rate, end_contact_rate, inflection_point)
        * S
        * (I + 0.5 * C)
        / N
    )
    dIdt = (
        beta(t, prob_infection, init_contact_rate, end_contact_rate, inflection_point)
        * S
        * (I + 0.5 * C)
        / N
        - ((1 - epsilon) * (((1 - alpha) * gamma * I) + (alpha * rho * I)))
        - (epsilon * I)
    )
    dCdt = (epsilon * I) - (
        ((1 - teta) * zeta * min(beds(t, N, beds_per_thousand, scaling_factor), C))
        + (teta * eta * min(beds(t, N, beds_per_thousand, scaling_factor), C))
        + max(0, C - beds(t, N, beds_per_thousand, scaling_factor))
    )
    dRdt = ((1 - epsilon) * (1 - alpha) * gamma * I) + (
        (1 - teta) * zeta * min(beds(t, N, beds_per_thousand, scaling_factor), C)
    )
    dDdt = (
        ((1 - epsilon) * alpha * rho * I)
        + (teta * eta * min(beds(t, N, beds_per_thousand, scaling_factor), C))
        + max(0, C - beds(t, N, beds_per_thousand, scaling_factor))
    )

    return (dSdt, dIdt, dCdt, dRdt, dDdt)


def SICRD_model(
    gamma,
    rho,
    alpha,
    epsilon,
    zeta,
    eta,
    teta,
    prob_infection,
    init_contact_rate,
    end_contact_rate,
    inflection_point,
    beds_per_thousand,
    scaling_factor,
):

    N = 1
    init_infected = 0.000001
    S0, I0, C0, R0, D0 = (
        N - init_infected,
        init_infected,
        0,
        0,
        0,
    )  # initial conditions: one infected, rest susceptible
    t = np.linspace(0, 100, 1000)  # Grid of time points (in days)

    y0 = S0, I0, C0, R0, D0  # Initial conditions vector
    S, I, C, R, D = odeint(
        deriv,
        y0,
        t,
        args=(
            N,
            prob_infection,
            init_contact_rate,
            end_contact_rate,
            inflection_point,
            #
            beds_per_thousand,
            scaling_factor,
            gamma,
            rho,
            alpha,
            epsilon,
            zeta,
            eta,
            teta,
        ),
    ).T
    SIRD_odeint = pd.DataFrame(
        {
            "Susceptible": S,
            "Infected": I,
            "Critically ill": C,
            "Recovered": R,
            "Dead": D,
        }
    )
    SIRD_odeint["total"] = SIRD_odeint.sum(axis=1)
    SIRD_odeint["days"] = SIRD_odeint.reset_index()["index"].div(10)
    triage_df = pd.DataFrame(
        {
            "beds": map(
                beds,
                t,
                [1 for x in range(len(t))],
                [beds_per_thousand for x in range(len(t))],
                [scaling_factor for x in range(len(t))],
            )
        }
    )
    triage_df["days"] = triage_df.reset_index()["index"].div(10)

    fig = make_subplots(
        rows=2,
        cols=1,
        x_title="Days",
        y_title="Relative probability",
        subplot_titles=("Compartmental model", "Triage conditions"),
    )
    #     Subfig 1
    for i, col in enumerate(SIRD_odeint.columns):
        if col != "days" and col != "total":
            fig.add_trace(
                go.Scatter(
                    x=SIRD_odeint["days"],
                    y=SIRD_odeint[col],
                    mode="lines",
                    name=col,
                    line=dict(color=colors[i]),
                    legendgroup="base model",
                ),
                row=1,
                col=1,
            )
    # Subfig 2
    fig.add_trace(
        go.Scatter(
            x=SIRD_odeint["days"],
            y=SIRD_odeint["Critically ill"],
            mode="lines",
            name="Critically ill",
            line=(dict(color=colors[2])),
            legendgroup="beds",
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=SIRD_odeint["days"],
            y=SIRD_odeint["Dead"],
            mode="lines",
            name="Dead",
            line=(dict(color=colors[4], dash="dot")),
            legendgroup="beds",
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=triage_df["days"],
            y=triage_df["beds"],
            mode="lines",
            name="Beds",
            line=(dict(color=colors[5], dash="dot")),
            legendgroup="beds",
        ),
        row=2,
        col=1,
    )

    #     axes update
    fig.update_layout(
        title="Triage in the expanded SIR model",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        #         xaxis_title="Days",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    return fig
