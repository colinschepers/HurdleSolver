from typing import List, Tuple

import pandas as pd
import streamlit as st

from hurdle_solver.solver import Solver
from hurdle_solver.utils import get_all_words

TABLE_ROW_LIMIT = 1000
STYLING_JS = """
    <style>
        footer {visibility: hidden;}
        .block-container {padding: 1rem;}
        tbody th {display:none}
        .blank {display:none}
        div[data-stale*="false"] button { width: 100%; }
        div[data-testid*="stMarkdownContainer"] table { width: 100%; }
    </style>
"""


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def get_vocab():
    return set(get_all_words())


def get_solver() -> Solver:
    solver = Solver(get_vocab())
    for guess, num_green, num_yellow in get_game_state():
        solver.add_information(guess, num_green, num_yellow)
    return solver


def get_game_state() -> List[Tuple[str, int, int]]:
    if 'game_state' not in st.session_state:
        st.session_state['game_state'] = []
    return st.session_state.game_state


def highlight_cols(df: pd.DataFrame):
    df = df.copy()
    df.loc[:, :] = 'background-color: #b7b5b5'
    df[['# Green']] = 'background-color: #66bb6a'
    df[['# Yellow']] = 'background-color: #ffa726'
    return df


def get_guess_options():
    return get_solver().get_suggestions()


def get_scored_suggestions():
    return get_solver().get_scored_suggestions()[:TABLE_ROW_LIMIT]


def get_dataframe():
    game_state = get_game_state()
    data = [(*guess, num_green, num_yellow) for guess, num_green, num_yellow in game_state]
    df = pd.DataFrame(data, columns=list(range(5)) + ["# Green", "# Yellow"])
    df = df.style.apply(highlight_cols, axis=None).hide(axis='columns')
    return df


def run_dashboard():
    st.set_page_config(page_title="Hurdle Solver")
    st.markdown(STYLING_JS, unsafe_allow_html=True)

    st.title("Hurdle Solver")
    game_state = get_game_state()

    col1, col2, col3 = st.columns(3)
    guess_placeholder = col1.empty()
    guess = guess_placeholder.selectbox('Guess', options=get_guess_options(), key="guess")
    num_green = col2.number_input('# Green', 0, 5, 0)
    num_yellow = col3.number_input('# Yellow', 0, 5, 0)

    if st.button("Add"):
        if num_green == 5:
            st.balloons()
        game_state.append((guess, num_green, num_yellow))
        guess_placeholder.selectbox('Guess', options=get_guess_options(), key="guess_updated")

    dataframe_placeholder = st.empty()
    dataframe_placeholder.write(get_dataframe().to_html(), unsafe_allow_html=True, key="dataframe")

    if st.button("Remove") and game_state:
        game_state.pop()
        guess_placeholder.selectbox('Guess', options=get_guess_options(), key="guess_updated")
        dataframe_placeholder.write(get_dataframe().to_html(), unsafe_allow_html=True, key="dataframe_updated")

    df = pd.DataFrame(get_scored_suggestions(), columns=["Suggestion", "Score"])
    st.table(df)


if __name__ == '__main__':
    run_dashboard()
