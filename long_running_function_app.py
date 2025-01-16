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

    # Create a global state object, potentially reading it from cache.
    gs = gsl.get_global_state()

    # Demonstrate persistence of the "name" key in the global state.
    name = gs.text_input('Enter your name:', key='name', initial_value='Andrew')
    st.write(f'name: {name}')

    # Demonstrate persistence of the "number" key in the global state.
    number = gs.number_input('Enter a number:', key='number', initial_value=0, min_value=0)
    st.write(f'number: {number}')

    # Add two more numbers
    number2 = gs.number_input('Enter another number (such as seconds to wait):', key='number2', initial_value=1, min_value=1)
    number3 = gs.number_input('Enter a third number (such as iterations to run):', key='number3', initial_value=5, min_value=1)

    # Use the "number" key in the global state to demonstrate the persistence of not only the "return_value" key in the global state, but also the calculation of it.
    key = 'return_value'
    gsl.initialize_state(gs, key, [])  # note saving to session state is unnecessary unlike above, so probably make that optional in initialize_state()
    button_text = 'Generate sequence'; args = (generate_sequence, number); kwargs = {'seconds_to_wait': number2, 'iterations_to_run': number3}  # swap this line out for a different one to run a different long-running function with different arguments, such as the commented-out one below
    # button_text = 'Calculate Fibonacci'; args = (fibonacci.fibonacci, number); kwargs = {}
    st.button(button_text, on_click=gsl.wrapper_for_long_running_function, args=(gs,) + args, kwargs=kwargs)
    return_value = gs.session_state[key]

    # Display the return value of the long-running function.
    st.write(f'return_value: {return_value}')

    # Allow the user to clear the global and session states.
    st.button('Clear states', on_click=gsl.clear_states, args=(gs,))


# Run the main function.
if __name__ == '__main__':
    main()
