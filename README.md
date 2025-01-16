# Streamlit Global State Example - Both State and Calculation

* [Home on NIDAP](https://nidap.nih.gov/workspace/compass/view/ri.compass.main.folder.4ecdda7e-e977-4dd0-b5d5-5bb8bb14a730)
* [Secondary home on GitHub](https://github.com/andrew-weisman/persisting-streamlit-state-and-calculation)

This app shows that while a job is running, you can:

1. Refresh the browser.
1. Switch pages.
1. Close the browser and go back to the same URL.

Once you return to the app, it will be like you never left, as long as the original "streamlit run ..." process hasn't been stopped.

Thus, this shows how we've used purely native Streamlit functionality to solve the problem of both (1) loss of static values in the session state and (2) loss of long-running calculation results.
