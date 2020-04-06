# -*- coding: utf-8 -*-
"""
@author: Michał Kołomański
"""
import random

a = 10               # Rectangle dimension in km
b = 15               # Rectangle dimension in km
N = 100              # Number of people
dx = random.random() # Movement speed (0-1)
MR = 0.7 * N         # Number of people moving in one timestamp
R_inf = 0.005        # How close people must be to get infection in km
T_inf = 0.5          # How much time people must spend <= R_inf to get infection in h
T_inc = 7            # Incubation time in days, person can infect people (no symptoms) - person moves
T_rec = 14           # Convalescence time, person can infect people (symptoms) - person stops
DR = 0.5             # Mortality rate. Recovery or death.
# People who have recovered regain the ability to move and are resistant to subsequent infections
# The deceased are removed from the simulation

