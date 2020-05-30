import numpy as np
import pandas as pd


# prob_infection = 0.25
# init_contact_rate = 5
# end_contact_rate = 5
# inflection_point = 15
# beds_per_thousand = 30
# beds_scaling_factor = 0.0


def contact_rate(t, init_contact_rate, end_contact_rate, inflection_point):
    speed_of_change = 0.8
    return (init_contact_rate - end_contact_rate) / (
        1 + np.exp(-speed_of_change * (-t + inflection_point))
    ) + end_contact_rate


def beta(t, prob_infection, init_contact_rate, end_contact_rate, inflection_point):
    #     prob_infection = 0.25
    return (
        contact_rate(t, init_contact_rate, end_contact_rate, inflection_point)
        * prob_infection
    )


def beds(t, N, beds_per_thousand, scaling_factor):
    base_number = (beds_per_thousand / 1000) * N  # correct for Germany
    s = scaling_factor  # scaling constant meaning 1 bed per 1000 persons added every 5 days
    return base_number + s * t * base_number


def test_rate(t, N, tests_per_thousand, scaling_factor):
    base_number = (tests_per_thousand / 1000) * N  # correct for Germany
    s = scaling_factor  # scaling constant meaning 1 bed per 1000 persons added every 5 days
    return base_number + s * t * base_number
