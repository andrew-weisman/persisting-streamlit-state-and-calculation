# Import relevant libraries
import streamlit as st
import time
import global_state_lib as gsl
from datetime import datetime
import pytz


# Define a function to convert a datetime difference to HH:MM:SS format
def datetime_diff_to_HHMMSS(diff):
    hours, remainder = divmod(diff.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}'


# Main function
def main():

    # Create a global state object, potentially reading it from cache.
    gs = gsl.get_global_state()

    # Constant
    format_string = '%Y-%m-%d %I:%M:%S %p %Z'
    
    # Initialize session state variables.
    if 'running' not in st.session_state:
        st.session_state['running'] = False

    # Create columns for the start and stop buttons.
    col1, col2 = st.columns(2)

    # Create the start and stop buttons.
    with col1:
        if st.button('Start monitoring', use_container_width=True):
            st.session_state['running'] = True
    with col2:
        if st.button('Stop monitoring', use_container_width=True):
            st.session_state['running'] = False

    # Create a placeholder for the display beneath the buttons
    placeholder = st.container()

    # Run a loop to update the output every second if running
    while st.session_state['running']:
        start_time = gs.session_state['long_running_function_start_time']
        if gs.session_state['long_running_function_end_time'] is not None:
            return_value = gs.session_state['return_value']
            end_time = gs.session_state['long_running_function_end_time']
            placeholder.write('Done.')
            placeholder.write(f'Return value: {return_value}')
            placeholder.write(f'Start time: {start_time.strftime(format_string)}')
            placeholder.write(f'End time: {end_time.strftime(format_string)}')
            placeholder.write(f'Elapsed time: {datetime_diff_to_HHMMSS(end_time - start_time)}')
        else:
            current_time = datetime.now(pytz.timezone('US/Eastern'))
            placeholder.write(f'Running...')
            placeholder.write(f'Start time: {start_time.strftime(format_string)}')
            placeholder.write(f'Elapsed time: {datetime_diff_to_HHMMSS(current_time - start_time)}')
        time.sleep(1)
        st.rerun()


# Run the main function
if __name__ == "__main__":
    main()
