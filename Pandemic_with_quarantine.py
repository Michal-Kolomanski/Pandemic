# -*- coding: utf-8 -*-
"""
@author: Michał Kołomański
"""

# Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def point(xlimit, ylimit):
    """
    :param xlimit:
    :param ylimit:
    :return random point:
    """
    import random
    x = random.uniform(0, xlimit)
    y = random.uniform(0, ylimit)
    return x, y

def Generate_N_people_1_infected(Number_of_people, xlimit, ylimit):
    """
    :param Number_of_people:
    :param xlimit:
    :param ylimit:
    :return dataframe of N people, one of them is infected:
    """
    import pandas as pd
    df = pd.DataFrame(columns='X,Y'.split(','))

    for i in range(Number_of_people):
        df.loc[i, 'X'], df.loc[i, 'Y'] = point(xlimit, ylimit)
        df.loc[i, 'Infected'] = False
        df.loc[i, 'Hour'] = 0

    df.loc[df.sample().index.values, 'Infected'] = True # 1 random infection

    return df

def who_moves(df, MR):
    """
    :param df:
    :return List of people that can move,
    Status (in numbers) of a day:
    """
    import math
    import pandas as pd
    samplesize = math.floor(len(df) * MR)
    Movers = df.sample(n=samplesize).index.values.tolist()
    hourStatus = pd.DataFrame(columns='Healthy,Infected,Ill,Recovered,Death,Quarantined'.split(','))

    return hourStatus, Movers

def point_color(df):
    """
    A function which colours points on the graph (the parameter 'Infected' in df)
    100 - Death
    50 - Ill
    10 - Rcovered
    True - Infected
    False - Healthy
    :param df_of_poeple:
    :return colored points:
    """
    cols = []
    for i in df.index:
        if df.loc[i, 'Infected'] == True:  # Infected
            cols.append('red')
        elif df.loc[i, 'Infected'] == 100:  # Death
            cols.append('white')
        elif df.loc[i, 'Infected'] == 50:  # Ill
            cols.append('yellow')
        elif df.loc[i, 'Infected'] == 10:  # Recovered
            cols.append('green')
        elif df.loc[i, 'Infected'] == False: # Healthy
            cols.append('blue')
        elif df.loc[i, 'Infected'] == 200: # Quarantined
            cols.append('magenta')
    return cols

def legend_color(Status):
    """
    Colors for a legend (graph)
    :param Status:
    :return colors:
    """
    cols = []

    for i in Status.columns:
        if i == 'Infected':         # Infected
            cols.append('red')
        elif i == 'Death':          # Death
            cols.append('black')
        elif i == 'Ill':            # Ill
            cols.append('yellow')
        elif i == 'Recovered':      # Recovered
            cols.append('green')
        elif i == 'Healthy':        # Healthy
            cols.append('blue')
        elif i == 'Quarantined':    # Quarantined
            cols.append('magenta')

    return cols


def Plot():
    """
    Main function to plot pandemic progress
    :return:
    """
    import matplotlib.pyplot as plt
    global df, fig, hourStatus, hour, Movers

    # ploting dots
    cols = point_color(df)
    Labels = ['Healthy', 'Infected', 'Ill', 'Recovered', 'Death', 'Quarantined']
    axs[0].cla()
    axs[0].scatter(df['X'], df['Y'], s=5, c=cols)
    cols = legend_color(hourStatus)
    shour = str(hour)
    title = 'Hour ' + shour
    axs[0].set_title(title, loc='left')
    axs[0].set_yticklabels([])
    axs[0].set_xticklabels([])
    axs[0].tick_params(
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        right=False,  # ticks along the right edge are off
        left=False,  # ticks along the left edge are off
        labelbottom=False)  # labels along the bottom edge are off
    axs[1].cla()
    axs[1].plot(hourStatus['Healthy'], label=Labels[0], color=cols[0])
    axs[1].plot(hourStatus['Infected'], label=Labels[1], color=cols[1])
    axs[1].plot(hourStatus['Ill'], label=Labels[2], color=cols[2])
    axs[1].plot(hourStatus['Recovered'], label=Labels[3], color=cols[3])
    axs[1].plot(hourStatus['Death'], label=Labels[4], color=cols[4])
    axs[1].plot(hourStatus['Quarantined'], label=Labels[5], color=cols[5])
    axs[1].legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=0.)
    plt.xlabel('Hours')
    plt.ylabel('Population')
    if hour < 10: shour = '0' + shour
    title = 'Hour' + shour + '.png'
    plt.savefig(title)
    plt.show()

def Move(xlimit, ylimit, dx):
    """
    Move Movers Randomly
    :param xlimit:
    :param ylimit:
    :return:
    """
    global df, Movers
    for i in Movers:
        if (df.loc[i, 'Infected'] == 100 or df.loc[i, 'Infected'] == 50 or df.loc[i, 'Infected'] == 10 or df.loc[i, 'Infected'] == 200): Movers.remove(i)
        df.loc[i, 'X'], df.loc[i, 'Y'] = (df.loc[i, 'X'] + dx) % xlimit, \
        (df.loc[i, 'Y'] + dx) % ylimit


def Count(hour):
    """
    Count statistics
    :param hour:
    :return:
    """
    global df, hourStatus

    List = list(df['Infected'])
    hourStatus.loc[hour, 'Healthy'] = List.count(False)
    hourStatus.loc[hour, 'Infected'] = List.count(True)
    hourStatus.loc[hour, 'Ill'] = List.count(50)
    hourStatus.loc[hour, 'Recovered'] = List.count(10)
    hourStatus.loc[hour, 'Death'] = List.count(100)
    hourStatus.loc[hour, 'Quarantined'] = List.count(200)

    return

def infect(sample_index):
    """
    infect people
    :param sample_index:
    :return:
    """
    global df, hour
    if df.loc[sample_index, 'Infected'] == False:
        df.loc[sample_index, 'Infected'], df.loc[sample_index, 'Hour'] = True, hour

def check(i, j):
    """
    check if person i can be infected by person j and the other way
    :param person i:
    :param person j:
    :return:
    """
    import math
    global df, YesterdayPatients, R_inf
    Distance = math.sqrt((df.loc[i, 'X'] - df.loc[j, 'X']) ** 2 + (df.loc[i, 'Y'] - df.loc[j, 'Y']) ** 2)
    flag = ((YesterdayPatients[i] == True) ^ (YesterdayPatients[j] == True)) and Distance < R_inf and T_inf < timestamp
    return flag

def interact():
    """
    check everyone with everyone
    :return:
    """
    global hour, df
    for i in range(len(df)):
        for j in range(i):
            if check(i, j):
                if (df.loc[i, 'Infected'] == False):
                    infect(i)
                else:
                    infect(j)

def ill():
    """
    choose people who become ill (Hospitalized or home quarantine). Stops moving
    :return:
    """
    global df, hour

    for i in range(len(df['Hour'])):
        if df['Hour'][i] != 0.0 and df['Infected'][i] == True:
            if hour - df['Hour'][i] >= T_inc:
                df.loc[i, 'Infected'] = 50

    return

def kill(person_index):
    """
    Sad thing to do but \/('')\/
    :return:
    """
    global df

    df.loc[person_index, 'Infected'] = 100


def recover(person_index):
    """
    become recovered
    :return:
    """
    global df

    df.loc[person_index, 'Infected'] = 10


def Kill_or_recover():
    """
    kill or recover somebody (decision)
    :return:
    """
    import random
    global df, hour

    for i in range(len(df['Hour'])):
        if df.loc[i, 'Hour'] != 0.0 and df.loc[i, 'Infected'] == 50:
            if hour - df['Hour'][i] >= T_rec:
                decision = random.uniform(0, 1)
                if decision >= 1 - DR:
                    kill(i)
                else:
                    recover(i)

def quarantine():
    """
    quarantine mechanism
    :return:
    """
    import random
    global df

    for i in range(len(df['Hour'])):
        if df.loc[i, 'Infected'] == True:
            if (random.uniform(0, 10) >= 9.5): # 5% to be quarantined (in each ts)
                df.loc[i, 'Infected'] = 200


def Next_hour():
    """
    simulating the passage of time
    :return:
    """
    global df, hour
    hour += 1
    quarantine()
    ill()
    Kill_or_recover()
    print(hourStatus.loc[len(hourStatus) - 1])
    Move(xlimit, ylimit, dx)
    interact()

def gif():
    """
    creates gif from png
    :return:
    """
    from PIL import Image
    import glob

    # Create frames
    frames = []
    imgs = glob.glob("*.png")
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    # Save into GIF
    frames[0].save('pandemic.gif', format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=500, loop=0)


# Main ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib.pyplot as plt
""" 
Assumptions:
- N people in a rectangle (dim: xlimit, ylimit)
- Time is increased by a timestamp. In this project time was counted in hours and was increased by 1h
- People (represented as dots) can have 5 states: 
1) healthy - can't infect, can move
2) infected - can infect, can move
3) ill - can infect, can't move
4) recovered - can't infect, can move
5) death - can't infect, can't move - The deceased are removed from the simulation

The rest of the information below:
"""
# -------------------------------------------
#   I N P U T   V A R I A B L E S   H E R E  |
# -------------------------------------------
#                                            |
xlimit = 10          # Rectangle dimension in km
ylimit = 10          # Rectangle dimension in km
N = 500              # Number of people
timestamp = 1        # In hours
number_of_hours = 60  # Duration of the pandemic
dx = 0.5             # Range of single movement in one ts
MR = 0.6             # % of people moving in one timestamp
R_inf = 0.5          # How close people must be to get infection in km
T_inf = 0.5          # How much time people must spend <= R_inf to get infection in h
T_inc = 7            # Incubation time in hours, person can infect people (no symptoms) - person moves
T_rec = 20           # Convalescence time, person can infect people (symptoms) - person stops
DR = 0.1             # Mortality rate. Recovery or death.
#                                            |
# -------------------------------------------

# Pandemic is starting, hour = 0
hour = 0

df = Generate_N_people_1_infected(N, xlimit, ylimit)
hourStatus, Movers = who_moves(df, MR)
YesterdayPatients = list(df['Infected'])

while hour < number_of_hours:
    fig, axs = plt.subplots(2)
    fig.suptitle('Pandemic model', fontsize=16)
    Plot()
    Count(hour)
    Next_hour()
    YesterdayPatients = list(df['Infected'])

gif()


