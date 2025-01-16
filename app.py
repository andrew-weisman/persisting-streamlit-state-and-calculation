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

    # Set the page layout to wide.
    st.set_page_config(layout='wide')

    # If a new Streamlit session has been connected, display a warning message.
    if 'session_has_been_connected' not in st.session_state:
        st.warning(f'Connecting to a new Streamlit session on {datetime.now(pytz.timezone("US/Eastern")).strftime("%Y-%m-%d %I:%M:%S %p %Z")}.')
        st.session_state['session_has_been_connected'] = True
    
    # In the first of two main columns...
    main_columns = st.columns([1/3, 2/3])
    with main_columns[0]:

        st.write(os.listdir())

        # Display README.md as markdown in this app.
        with open(os.path.join(os.getcwd(), 'README.md'), 'r') as f:
            st.markdown(f.read())

    # In the second of two main columns...
    with main_columns[1]:

        # Display a header.
        st.subheader(pg.title)

        # Display the page.
        pg.run()


# Run the main function.
if __name__ == "__main__":
    main()
