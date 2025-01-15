# Potential TODO:
# * See my original cursory implementation of a global state to ensure I'm not missing anything. E.g., I may have done some things more elegantly there.


# Import relevant libraries
import streamlit as st
import time
import fibonacci
import global_state_lib as gsl


# Every seconds_to_wait seconds, add seconds_to_wait to starting_number and append the new number to a running list. After iterations_to_run iterations, return the resulting sequence.
def generate_sequence(starting_number, seconds_to_wait=1, iterations_to_run=5):
    sequence = []
    for _ in range(iterations_to_run):
        sequence.append(starting_number)
        starting_number += seconds_to_wait
        time.sleep(seconds_to_wait)
    return sequence


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
    gs = gsl.get_global_state()

    # Demonstrate persistence of the "name" key in the global state.
    # key = 'name'
    # gsl.initialize_state(gs, key, 'Andrew')
    # name = st.text_input('Enter your name:', on_change=gsl.save_to_global_state, args=(gs, key), key=key)
    name = gs.text_input('Enter your name:', on_change=None, args=None, kwargs=None, key='name', initial_value='Andrew')  # on_change, args, kwargs correspond to the callback as st.text_input() used to
    st.write(f'name: {name}')

    # Demonstrate persistence of the "number" key in the global state.
    # key = 'number'
    # gsl.initialize_state(gs, key, 0)
    # number = st.number_input('Enter a number:', on_change=gsl.save_to_global_state, args=(gs, key), key=key, min_value=0)
    number = gs.number_input('Enter a number:', on_change=None, args=None, kwargs=None, key='number', initial_value=0, min_value=0)
    st.write(f'number: {number}')

    # Use the "number" key in the global state to demonstrate the persistence of not only the "return_value" key in the global state, but also the calculation of it.
    key = 'return_value'
    gsl.initialize_state(gs, key, [])  # note saving to session state is unnecessary unlike above, so probably make that optional in initialize_state()
    button_text = 'Generate sequence'; args = (generate_sequence, number); kwargs = {'seconds_to_wait': 1, 'iterations_to_run': 10}  # swap this line out for a different one to run a different long-running function with different arguments
    # button_text = 'Calculate Fibonacci'; args = (fibonacci.fibonacci, number); kwargs = {}
    st.button(button_text, on_click=gsl.callback_for_long_running_function, args=(gs,) + args, kwargs=kwargs)
    return_value = gs.session_state[key]

    # Display the return value of the long-running function.
    st.write(f'return_value: {return_value}')

    # Allow the user to clear the global and session states.
    st.button('Clear states', on_click=gsl.clear_states, args=(gs,))


# Run the main function.
if __name__ == '__main__':
    main()
