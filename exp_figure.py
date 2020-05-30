import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import datetime

# from app import colors

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


def expfigure(exp_min, exp_max, exp_incr, input_exp_per):
    vals_cont = np.linspace(exp_min, exp_max, exp_incr)
    df = get_frame(input_exp_per, vals_cont)
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
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(showgrid=False, zeroline=True)
    fig.update_yaxes(showgrid=False, zeroline=True)
    fig.update_yaxes(type="log", row=1, col=2)
    return fig
