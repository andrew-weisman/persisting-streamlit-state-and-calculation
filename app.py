import streamlit as st
import long_running_function_app
import job_monitor


def main():

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

    pg.run()


if __name__ == "__main__":
    main()
