import streamlit as st
import time


def generate_sequence(gs, number):
    # Every 1 second, add 1 to number and append the new number to a running list. After 5 seconds, assign the sequence to the global state.
    sequence = []
    for _ in range(5):
        sequence.append(number)
        number += 1
        time.sleep(1)
    gs.session_state['sequence'] = sequence


def initialize_state(gs, key, default_value):
    if key not in gs.session_state:
        gs.session_state[key] = default_value
    if key not in st.session_state:
        st.session_state[key] = gs.session_state[key]


def clear_states(gs):
    gs.session_state.clear()
    st.session_state.clear()


def save_to_global_state(gs, key):
    gs.session_state[key] = st.session_state[key]


@st.cache_resource
def get_global_state():
    return GlobalState()


class GlobalState:
    def __init__(self):
        self.session_state = {}


def main():

    # Create a global state object
    gs = get_global_state()

    key = 'name'
    initialize_state(gs, key, 'Andrew')
    name = st.text_input('Enter your name:', on_change=save_to_global_state, args=(gs, key), key=key)

    st.write(f'name: {name}')

    key = 'number'
    initialize_state(gs, key, 0)
    number = st.number_input('Enter a number:', on_change=save_to_global_state, args=(gs, key), key=key, min_value=0)

    st.write(f'number: {number}')

    key = 'sequence'
    initialize_state(gs, key, [])  # note saving to session state is unnecessary, so probably make optional in initialize_state()
    st.button('Generate sequence', on_click=generate_sequence, args=(gs, number))
    sequence = gs.session_state[key]

    st.markdown('''
Steps:
                
1. Press the "Generate sequence" button above.
2. Immediately refresh the browser.
3. Keep pressing "r" to rerun the app.
4. After five seconds, the new sequence will be displayed.
                ''')

    st.write(f'sequence: {sequence}')

    st.button('Clear states', on_click=clear_states, args=(gs,))


if __name__ == '__main__':
    main()
