#!/usr/bin/env python
# coding: utf-8

# In[1]:


# %load_ext nb_black


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


# In[3]:


# print(px.colors.qualitative.Vivid * 2)
print(px.colors.qualitative.Plotly * 2)


# In[4]:


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
# colors = [
#     "rgb(255, 111, 97)",
#     "rgb(93, 105, 177)",
#     "rgb(82, 188, 163)",
#     "rgb(165, 170, 153)",
#     "rgb(229, 134, 6)",
#     "rgb(204, 97, 176)",
#     "rgb(36, 121, 108)",
#     "rgb(218, 165, 27)",
#     "rgb(47, 138, 196)",
#     "rgb(118, 78, 159)",
#     "rgb(153, 201, 69)",
#     #
#     "rgb(255, 111, 97)",
#     "rgb(93, 105, 177)",
#     "rgb(82, 188, 163)",
#     "rgb(165, 170, 153)",
#     "rgb(229, 134, 6)",
#     "rgb(204, 97, 176)",
#     "rgb(36, 121, 108)",
#     "rgb(218, 165, 27)",
#     "rgb(47, 138, 196)",
#     "rgb(118, 78, 159)",
#     "rgb(153, 201, 69)",
# ]

fig = go.Figure(
    data=[
        go.Bar(
            x=[x for x in range(1, len(colors) + 1)],
            y=[1 for x in range(1, len(colors) + 1)],
            marker=dict(color=colors),
        )
    ]
)
fig.show()


# ### exponential growth figure

# In[5]:


def get_series(t, i):
    """
    takes in a base population of infected <i>
    and the duration of spreading and returns an array of cumulative infected <c> (recovery period assumed as 14 days)
    and of newly infected <x> per day.
    """
    p = 0  # newly infected per day
    x = []  # array of cumulative infected per day
    c = []  # array of newly infected per day
    for z in range(t + 1):
        if z <= 14:
            p += i ** z
            x.append(p)
            c.append(i ** z)
        else:
            p += i ** z
            x.append(p)
            c.append(i ** z - c[z - 14])

    return (x, c)


def get_frame(t, vals):
    """
    takes in the duration of spreading <t> and an array of initially infected <vals> and calls get_series for every element of 
    vals. A pandas Dataframe with the concatenated results is returned.
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


# In[6]:


def expfigure(t, vals_cont):
    df = get_frame(t, vals_cont)
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Linear scale", "Log scale"),
        x_title="Days",
        y_title="Number of infected",
    )
    for i, val in enumerate(vals_cont):
        fig.add_trace(
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
        fig.add_trace(
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
    fig.update_layout(
        title="Exponential growth of infected population (cumulative sum)",
    )
    fig.update_xaxes(showgrid=False, zeroline=True)
    fig.update_yaxes(showgrid=False, zeroline=True)
    fig.update_yaxes(type="log", row=1, col=2)
    return fig


t = 10
vals_cont = list(np.linspace(1.5, 3, 3))

fig = expfigure(t, vals_cont)
fig.show()
# fig.write_image("EXPmodel.svg", width=700, height=400)


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


# ### ECDC Data graphs

# In[8]:


def ECDCdata():
    df_ECDC = pd.read_csv(
        "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    )

    df_ECDC["dateRep"] = pd.to_datetime(df_ECDC["dateRep"], infer_datetime_format=True)
    df_ECDC["cases_cum"] = (
        df_ECDC.sort_values("dateRep")
        .groupby("countriesAndTerritories")["cases"]
        .cumsum()
    )
    df_ECDC["deaths_cum"] = (
        df_ECDC.sort_values("dateRep")
        .groupby("countriesAndTerritories")["deaths"]
        .cumsum()
    )

    df_ECDC_pv = df_ECDC.pivot_table(
        df_ECDC, columns="countriesAndTerritories", aggfunc="max"
    ).transpose()

    countries_group2 = [
        "China",
        "South_Korea",
        "Sweden",
        "Italy",
        "Germany",
        "United_States_of_America",
    ]
    df_ECDC_pv_group_2 = df_ECDC_pv.reset_index()[
        (df_ECDC_pv.reset_index()["countriesAndTerritories"] == "China")
        | (df_ECDC_pv.reset_index()["countriesAndTerritories"] == "South_Korea")
        | (df_ECDC_pv.reset_index()["countriesAndTerritories"] == "Sweden")
        | (df_ECDC_pv.reset_index()["countriesAndTerritories"] == "Italy")
        | (df_ECDC_pv.reset_index()["countriesAndTerritories"] == "Germany")
        #     | (
        #         df_ECDC_pv.reset_index()["countriesAndTerritories"]
        #         == "United_States_of_America"
        #     )
    ][["countriesAndTerritories", "cases_cum", "deaths_cum"]].values.tolist()
    return df_ECDC_pv, df_ECDC_pv_group_2


# Graph based on https://ourworldindata.org/covid-mortality-risk

# In[9]:


def ECDCfigure():
    df_ECDC_pv, df_ECDC_pv_group_2 = ECDCdata()
    fig = px.scatter(
        df_ECDC_pv[df_ECDC_pv["continentExp"] != "Other"].reset_index(),
        x="cases_cum",
        y="deaths_cum",
        color="continentExp",
        log_x=True,
        log_y=True,
        hover_data=["countriesAndTerritories"],
        title="Cumulative cases and deaths in different countries until {}".format(
            today_date
        ),
        symbol="continentExp",
        color_discrete_sequence=colors,
    )
    v = [0.1, 0.025, 0.00625, 0.0015625]
    diags = []
    for i in v:
        diags.append(1 / i)
    for diag in diags:
        fig.add_trace(
            go.Scatter(
                x=[1 * diag, df_ECDC_pv["cases_cum"].max()],
                y=[1, df_ECDC_pv["cases_cum"].max() / diag],
                mode="lines+text",
                name="CFR of {}%".format(round((1 / diag * 100), 3)),
                line_shape="spline",
                line=dict(width=1, dash="dot", color="grey"),
                #             text=["", "{}% CFR".format(round((1 / diag * 100), 3))],
                textposition="middle right",
                showlegend=False,
            )
        )
        fig.add_annotation(
            text="{}% CFR".format(round((1 / diag * 100), 3)),
            x=np.log10(df_ECDC_pv["cases_cum"].max()),
            y=np.log10(df_ECDC_pv["cases_cum"].max() / diag),
            xref="x",
            yref="y",
            ax=42,
            ay=0,
            width=80,
            align="left",
            font=dict(size=8,),
        )
    fig.update_layout(legend_title_text="")
    fig.update_traces(textfont_size=7,)
    fig.update_xaxes(
        nticks=6, title_text="Log of cumulative confirmed cases",
    )
    fig.update_yaxes(
        nticks=6, title_text="Log of cumulative confirmed deaths",
    )
    for line in range(len(df_ECDC_pv_group_2)):
        fig.add_annotation(
            text=df_ECDC_pv_group_2[line][0].replace("_", " "),
            x=np.log10(df_ECDC_pv_group_2[line][1]),
            y=np.log10(df_ECDC_pv_group_2[line][2]),
            xref="x",
            yref="y",
            ax=-40,
            ay=-40,
            font=dict(size=8,),
        )
    return fig


fig = ECDCfigure()
fig.show()
# fig.write_image("ECDCdata.svg", width=700, height=400)


# ###  Testing fallacies
# 
# https://de.statista.com/statistik/daten/studie/1107749/umfrage/labortest-fuer-das-coronavirus-covid-19-in-deutschland/

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


# #### SIRD includign critical cases


# In[13]:


t = np.linspace(0, 100, 1000)  # Grid of time points (in days)

contact_rates = pd.DataFrame(
    {
        "cr": map(
            contact_rate,
            t,
            [init_contact_rate for x in range(len(t))],
            [end_contact_rate for x in range(len(t))],
            [inflection_point for x in range(len(t))],
        )
    }
)
contact_rates["days"] = contact_rates.reset_index()["index"].div(10)
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=contact_rates["days"],
        y=contact_rates["cr"],
        mode="lines",
        name="contact rate",
        line=(dict(color=colors[0])),
    )
)
fig.show()


# ### Testing in the SIR model

# In[14]:


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
    fig.update_layout(title="Basic SIR model",)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    return fig


fig = SIRmodel(
    gamma, prob_infection, init_contact_rate, end_contact_rate, inflection_point,
)
fig.show()
# fig.write_image("SIRmodel.svg", width=700, height=400)


# In[15]:


0.25 * 5 * 4


# In[16]:


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
    fig.update_layout(title="Testing in the SIR model",)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    return fig


tests_per_thousand = 100
tests_scaling_factor = 0.00

fig = SIRTestingmModel(
    gamma,
    tests_per_thousand,
    tests_scaling_factor,
    prob_infection,
    init_contact_rate,
    end_contact_rate,
    inflection_point,
)
fig.show()
# fig.write_image("SIRTestingmModel.svg", width=700, height=500)


# In[ ]:




