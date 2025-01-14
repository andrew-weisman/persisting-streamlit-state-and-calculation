# Potential TODO:
# * Abstract out the Streamlit widgets into the global state class, e.g., make gs.number_input() and gs.text_input() methods. This way they can operate as usual, e.g., with their own callbacks using the same as the corresponding st APIs.
# * See my original implementation of a global state to ensure I'm not missing anything. E.g., I may have done it more elegantly there.


# Import required libraries
import streamlit as st
import time


# Every seconds_to_wait seconds, add 1 to starting_number and append the new number to a running list. After iterations_to_run iterations, return the resulting sequence.
def generate_sequence(starting_number, seconds_to_wait=1, iterations_to_run=5):
    sequence = []
    for _ in range(iterations_to_run):
        sequence.append(starting_number)
        starting_number += 1
        time.sleep(seconds_to_wait)
    return sequence


# Run a long-running function and then save the result to the global state.
def callback_for_long_running_function(gs, long_running_function, *args, **kwargs):
    return_value = long_running_function(*args, **kwargs)
    gs.session_state['return_value'] = return_value


# Potentially initialize a key to a default value in both the global and session states.
def initialize_state(gs, key, default_value):
    if key not in gs.session_state:
        gs.session_state[key] = default_value
    if key not in st.session_state:
        st.session_state[key] = gs.session_state[key]


# Clear both the global and session states.
def clear_states(gs):
    gs.session_state.clear()
    st.session_state.clear()


# Use the session state to save the same-named key to the global state.
def save_to_global_state(gs, key):
    gs.session_state[key] = st.session_state[key]


# Obtain a global state object, creating it if it doesn't exist.
@st.cache_resource
def get_global_state():
    return GlobalState()


# Define a class to hold the global state, which is simply a dictionary called session_state.
class GlobalState:
    def __init__(self):
        self.session_state = {}


# Define the  main function.
def main():

    # Display the app title.
    st.title('Streamlit Global State Example - Both State and Calculation')

    # Display the app instructions.
    st.markdown('''
This app demonstrates how to use a global state to persist both state and calculations across Streamlit sessions.
                
To demonstrate state persistence, enter your name and a number below. Then refresh the browser and see that your name and number are still there.
                
To demonstrate calculation persistence, for the sequence-generation example:
                
1. Press the "Generate sequence" button.
2. Immediately refresh the browser.
3. Keep pressing "r" to rerun the app.
4. After five seconds, the new sequence will be displayed.
                
To clear the state, press the "Clear states" button below.
                ''')                

    # Create a global state object, potentially reading it from cache.
    gs = get_global_state()

    # Demonstrate persistence of the "name" key in the global state.
    key = 'name'
    initialize_state(gs, key, 'Andrew')
    name = st.text_input('Enter your name:', on_change=save_to_global_state, args=(gs, key), key=key)
    st.write(f'name: {name}')

    # Demonstrate persistence of the "number" key in the global state.
    key = 'number'
    initialize_state(gs, key, 0)
    number = st.number_input('Enter a number:', on_change=save_to_global_state, args=(gs, key), key=key, min_value=0)
    st.write(f'number: {number}')

    # Use the "number" key in the global state to demonstrate the persistence of not only the "return_value" key in the global state, but also the calculation of it.
    key = 'return_value'
    initialize_state(gs, key, [])  # note saving to session state is unnecessary unlike above, so probably make that optional in initialize_state()
    button_text = 'Generate sequence'; args = (generate_sequence, number); kwargs = {'seconds_to_wait': 1, 'iterations_to_run': 5}  # swap this line out for a different one to run a different long-running function with different arguments
    st.button(button_text, on_click=callback_for_long_running_function, args=(gs,) + args, kwargs=kwargs)
    return_value = gs.session_state[key]

    # Display the return value of the long-running function.
    st.write(f'return_value: {return_value}')

    # Allow the user to clear the global and session states.
    st.button('Clear states', on_click=clear_states, args=(gs,))


# Run the main function.
if __name__ == '__main__':
    main()
