import streamlit as st

import numpy as np
import pandas as pd

from utils import *
from KeywordExtractor import DATA_TYPES
   
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

def extract_keywords(data_format : str):
    
    st.session_state[KEYWORD_EXTRACTOR_KEY].set_data_type(data_format)
    
    results = st.session_state[KEYWORD_EXTRACTOR_KEY].analyze_text(st.session_state[QUERY_TEXT_KEY])
    
    st.session_state[ANALYSIS_RESULTS_KEY] = pd.DataFrame(  results, 
                                                            columns=RESULTS_COLUMNS)
    
    # st.session_state[USER_PAGE_SELECTION_KEY] = RESULTS_NAV_OPTION
    
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

def setup_page():
    st.title('Setup Run')
    st.write('On this page you can upload files, or copy text to be analyized...')
    
    st.session_state[QUERY_TEXT_KEY] = st.text_area('Enter text to be analyzed')
    
    st.file_uploader('Upload a file to be analyzed')
    
    st.sidebar.divider()
        
    data_format = st.sidebar.selectbox(  'Data Format',
                                        options=DATA_TYPES)
    
    st.sidebar.checkbox('Batch Mode')
    st.sidebar.checkbox('+\'ve Keywords Only')
    st.sidebar.checkbox('Case sensitive')
    
    st.sidebar.checkbox(    'Explore Reference Text',
                            disabled=True)    
        
    st.sidebar.text_input('Confidence Level (%)', value='95')
    
    st.sidebar.divider()
    
    st.sidebar.button('Extract Keywords', 
                      on_click=extract_keywords,
                      args=[data_format])