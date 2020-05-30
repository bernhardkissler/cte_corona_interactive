import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# from plotly.subplots import make_subplots
import datetime

today_date = datetime.datetime.today().strftime("%m/%d/%Y")


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


def ECDCfigure():
    df_ECDC_pv, df_ECDC_pv_group_2 = ECDCdata()
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
    fig.update_layout(
        legend_title_text="",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
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
