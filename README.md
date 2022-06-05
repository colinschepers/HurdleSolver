# Hurdle Solver 
This application aims at helping to beat Hurdle (https://playhurdle.vercel.app), which is a Wordle meets Mastermind game.

## Installation
1. Make sure Python 3.8 is installed
2. Run the following command to install the requirements
```shell script
pip install -r requirements.txt
```

## Run Dashboard
Run the Streamlit Dashboard with the following command. 

```shell script
streamlit run streamlit_app.py
```

## Run via Console
To start a new solving session run the command below.
```shell script
python main.py
```
You can provide additional information when starting a solving session using arguments in triplets (guess, num_green, num_yellow):
```shell script
python main.py cones 1 2 nears 0 2
```
