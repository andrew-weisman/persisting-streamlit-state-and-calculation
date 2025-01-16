# Import relevant libraries
import streamlit as st
from datetime import datetime
import pytz


# Run a long-running function and then save the result to the global state.
def wrapper_for_long_running_function(gs, long_running_function, *args, **kwargs):
    timezone = pytz.timezone('US/Eastern')
    gs.session_state['long_running_function_start_time'] = datetime.now(timezone)
    gs.session_state['long_running_function_end_time'] = None
    gs.session_state['return_value'] = long_running_function(*args, **kwargs)
    gs.session_state['long_running_function_end_time'] = datetime.now(timezone)


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


# Use the session state to save the same-named key to the global state, optionally calling a callback function.
def save_to_global_state(global_state_arguments, callback_arguments=(None, None, None)):
    gs, key = global_state_arguments
    callback_func, callback_args, callback_kwargs = callback_arguments
    if callback_func is not None:
        if callback_args is None:
            callback_args = ()
        if callback_kwargs is None:
            callback_kwargs = {}
        callback_func(*callback_args, **callback_kwargs)
    gs.session_state[key] = st.session_state[key]


# Obtain a global state object, creating it if it doesn't exist.
@st.cache_resource
def get_global_state():
    return GlobalState()


# Define a class to hold the global state, which is simply a dictionary called session_state.
class GlobalState:

    # Initialize the object.
    def __init__(self):
        self.session_state = {}

    # Global state version of the st.text_input().
    def text_input(self, label, key=None, on_change=None, args=None, kwargs=None, initial_value=None, *args2, **kwargs2):
        initialize_state(self, key, initial_value)
        return st.text_input(label, on_change=save_to_global_state, kwargs={'global_state_arguments': (self, key), 'callback_arguments': (on_change, args, kwargs)}, key=key, *args2, **kwargs2)

    # Global state version of the st.number_input().
    def number_input(self, label, key=None, on_change=None, args=None, kwargs=None, initial_value=None, *args2, **kwargs2):
        initialize_state(self, key, initial_value)
        return st.number_input(label, on_change=save_to_global_state, kwargs={'global_state_arguments': (self, key), 'callback_arguments': (on_change, args, kwargs)}, key=key, *args2, **kwargs2)
