# Import relevant libraries
import streamlit as st
from datetime import datetime
import pandas as pd
import os
import pytz
from datetime import datetime

def get_timestamp(pretty=False):
    if pretty:
        return datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %I:%M:%S %p %Z')
    else:
        return datetime.now(pytz.timezone('US/Eastern')).strftime("%Y%m%d_%H%M%S_%Z")

def fibonacci(n):
    if n <= 1:
       return n
    else:
       return(fibonacci(n-1) + fibonacci(n-2))

# Define a function to manually restart the session state (only used for testing functionality)
def restart_session():
    st.toast('Restarting')
    for key in st.session_state.keys():
        del st.session_state[key]

# Define a function to determien whether we're in a published or unpublished Workspace
def get_dashboards_type():
    if os.path.exists('.git'):
        return 'unpublished'
    else:
        return 'published'

def main():

    # If the Streamlit session has just been initialized...
    if 'selection' not in st.session_state:
        
        # Initialize the widget value
        st.session_state['selection'] = 'start'
        
        # Get the current date+time
        # now = datetime.now()
        # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        dt_string = get_timestamp(pretty=True)
        
        # Append the current date+time to a logfile
        with open('startups.log', 'at') as f:
            f.write('{},{}\n'.format(dt_string, get_dashboards_type()))

    # Create a dropdown menu
    st.selectbox('Select an option:', ['start', 'a', 'b', 'c', 'd', 'e'], key='selection')

    # Output the log of the startup times to the screen
    if os.path.exists('startups.log'):
        st.dataframe(pd.read_csv('startups.log', header=None, names=['Start time', 'Workspace type']).tail(10))

    # Create a button to optionally manually restart the Streamlit session for testing functionality
    st.button('Restart session', on_click=restart_session)

    # Create a button to optionally run a long-taking process
    if 'number_in_fibonacci_sequence' not in st.session_state:
        st.session_state['number_in_fibonacci_sequence'] = 0
    st.number_input('Which number in the Fibonacci sequence to calculate:', min_value=0, max_value=500, key='number_in_fibonacci_sequence')
    if st.button('Start a long, computationally intensive process (try 500!)'):
        with st.spinner('Keep waiting...'):
            result = fibonacci(st.session_state['number_in_fibonacci_sequence'])
            st.write(result)
            with open('fibonacci.log', 'at') as f:
                f.write(f'The {st.session_state["number_in_fibonacci_sequence"]}th number in the Fibonacci sequence is {result}\n')
        st.success('Done!')    

    # Output the Fibonacci calculations
    if os.path.exists('fibonacci.log'):
        st.dataframe(pd.read_csv('fibonacci.log', header=None, names=['Calculation string']).tail(10))


if __name__ == '__main__':
    main()
