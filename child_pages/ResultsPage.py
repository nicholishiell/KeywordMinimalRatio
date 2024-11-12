import streamlit as st
import pandas as pd
import numpy as np

from utils import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

def results_page():

    st.title('Extracted Keywords')
    st.write('This page displays the results from the analysis...')
    st.write(f'Number of types in queryText: {len(st.session_state[QUERY_TEXT_KEY].split())}')
    st.write(f'Number of types in referenceText: {st.session_state[KEYWORD_EXTRACTOR_KEY].get_n_types()}')
    st.write('The table below shows the extracted keywords along with their Minimal Ratio (MR) values...')  

    if st.session_state[ANALYSIS_RESULTS_KEY] is None:
        st.warning('No results to display')
    
    else:
        
        st.table(st.session_state[ANALYSIS_RESULTS_KEY].sort_values(by=MINIMAL_RATIO_COLUMN,ascending=False),)