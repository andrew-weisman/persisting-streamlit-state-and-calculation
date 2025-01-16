# Import relevant libraries
import streamlit as st
import time
import global_state_lib as gsl
from datetime import datetime
import pytz


# Define a function to convert a datetime difference to HH:MM:SS format. This may be a little off, displaying 60 seconds as 60 seconds instead of 1 minute.
def datetime_diff_to_HHMMSS(diff):
    hours, remainder = divmod(diff.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}'


# Main function
def main():

    # Create a global state object, potentially reading it from cache.
    gs = gsl.get_global_state()

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

    # Run a loop to update the output every second if running
    format_string = '%Y-%m-%d %I:%M:%S %p %Z'
    while st.session_state['running']:
        start_time = gs.session_state['long_running_function_start_time']

        # If the long-running function has completed, display the results.
        if gs.session_state['long_running_function_end_time'] is not None:
            return_value = gs.session_state['return_value']
            end_time = gs.session_state['long_running_function_end_time']
            st.write('Done.')
            st.write(f'Return value: {return_value}')
            st.write(f'Start time: {start_time.strftime(format_string)}')
            st.write(f'End time: {end_time.strftime(format_string)}')
            st.write(f'Elapsed time: {datetime_diff_to_HHMMSS(end_time - start_time)}')
        
        # Otherwise, display the current time and elapsed time.
        else:
            current_time = datetime.now(pytz.timezone('US/Eastern'))
            st.write(f'Running...')
            st.write(f'Start time: {start_time.strftime(format_string)}')
            st.write(f'Elapsed time: {datetime_diff_to_HHMMSS(current_time - start_time)}')
        
        # Wait one second and rerun the app.
        time.sleep(1)
        st.rerun()


# Run the main function
if __name__ == "__main__":
    main()
