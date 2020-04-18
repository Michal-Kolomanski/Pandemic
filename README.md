# Pandemic

The goal of this program is to model a pandemic that:
- Takes place in a limited rectangular (**xlimit, ylimit**),
- In the defined area there is a population of **N** healthy people and one of them is infected,
- Simulate people movement with **dx** range in each timestamp,
- People need to be close enough **R_inf** and long enough **T_inf** for an infection to occur,
- The disease has two stages:
  - In the first stage **,,Infected”** for the incubation period **T_inc** a person can infect others and can move.
  - In the second stage **,,Ill”** for the convalescence time **T_rec** a person can infect others but cannot move.
- After the convalescence time, recovery or death of the person occurs. Morality rate is determined by the **DR** parameter.
