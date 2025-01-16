# Import relevant libraries
import streamlit as st
import long_running_function_app
import job_monitor
from datetime import datetime
import pytz
import os


# Define the main function.
def main():

    # Define the pages for the navigation bar.
    pg = st.navigation(
        {
            "Main": [
                st.Page(long_running_function_app.main, title="Global state example", icon=":material/dashboard:", default=True, url_path='global_state_example')
                ],
            "Tools": [
                st.Page(job_monitor.main, title="Job monitor", icon=":material/bug_report:", url_path='job_monitor')
                ],
        }
    )

    # If a new Streamlit session has been connected, display a warning message.
    if 'session_has_been_connected' not in st.session_state:
        st.warning(f'Connecting to a new Streamlit session on {datetime.now(pytz.timezone("US/Eastern")).strftime("%Y-%m-%d %I:%M:%S %p %Z")}.')
        st.session_state['session_has_been_connected'] = True
    
    # Display a header.
    st.title(pg.title)

    # Display the page.
    pg.run()


# Run the main function.
if __name__ == "__main__":
    main()
