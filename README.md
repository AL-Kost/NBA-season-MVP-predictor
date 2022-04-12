[![tests](https://github.com/AL-Kost/NBA-season-MVP-predictor/actions/workflows/tests.yaml/badge.svg)](https://github.com/AL-Kost/NBA-season-MVP-predictor/actions/workflows/tests.yaml)
[![train](https://github.com/AL-Kost/NBA-season-MVP-predictor/actions/workflows/train.yaml/badge.svg)](https://github.com/AL-Kost/NBA-season-MVP-predictor/actions/workflows/train.yaml)
[![predict](https://github.com/AL-Kost/NBA-season-MVP-predictor/actions/workflows/predict.yaml/badge.svg)](https://github.com/AL-Kost/NBA-season-MVP-predictor/actions/workflows/predict.yaml)

# **NBA season MVP Predict🏀r** 

## Project goal & Results

This project aims at predicting the player who will win the NBA MVP award, by modelling the voting panel. The NBA MVP is given since the 1955–56 season to the best performing player of the regular season. Until the 1979–80 season, the MVP was selected by a vote of NBA players. Since the 1980–81 season, the award is decided by a panel of sportswriters and broadcasters - more info [here](https://en.wikipedia.org/wiki/NBA_Most_Valuable_Player_Award).

You can analyze the results of model by exploring the developed and deployed Streamlit application via this [link](https://share.streamlit.io/al-kost/nba-season-mvp-predictor/main).


## Main challenges


#### Imbalanced data 

There is only 1 MVP per year, among hundreds of players.

Current approach to solve this problem :

- Use MVP share instead of MVP award as the target variable (regression model). A dozen of players receive votes each season.
- Use generally accepted tresholds to filter non-MVP players and reduce the imbalance : 
  - More than 50% of the season games played
  - More than 24 minutes played per game
  - Team ranked in the conference top-10 (play-in qualifier)

#### Label consistency

A player winning MVP one year may not have won MVP the year before, event with the same stats. It all depends on the other players competition.

Current solution:

- Normalize stats per season
  - Min-max scaling
  - Standardization

## Data

All data was scraped from https://www.basketball-reference.com/.

Many thanks to the authors of the site for creating such a user-friendly repository of statistical data.

## Future work and model improvement

- Learn PyTorch and replace sklearn.MLPRegressor with LSTM or other neural network architecture model
- Write Telegram bot

