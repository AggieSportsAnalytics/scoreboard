import streamlit as st
from functions import parse_live_matches
import time

st.title('Hello Streamlit!')

placeholder = st.empty() # create a placeholder to keep track of the live data

for seconds in range(60): # max one minute so that it doesn't accidentally run in the background
    placeholder.table(parse_live_matches())
    time.sleep(1) # update data every second
