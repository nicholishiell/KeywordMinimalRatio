import streamlit as st

import numpy as np
import pandas as pd

from utils import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
def get_guery_list():
    query_text = st.session_state[QUERY_TEXT_KEY]
    
    query_text = ''.join(filter(lambda x: x.isalpha() or x.isspace(), query_text))
    query_text = query_text.lower() 
       
    n_sample = len(query_text.split())
    
    word_counts = {}
    for word in query_text.split():
        word_counts[word] = word_counts.get(word, 0) + 1
    
    query_list = [[word, count] for word, count in word_counts.items()]
    
    return query_list, n_sample
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

def extract_keywords():
    
    query_list, n_sample = get_guery_list()
    ke = st.session_state[KEYWORD_EXTRACTOR_KEY]
    
    results = []
    for query in query_list:
        
        mr, ll, ul = ke.calculate_minimal_ratio(type=query[0],
                                                type_freq=query[1],
                                                sample_size=n_sample)
    
        results.append([query[0], mr, query[1], ke.get_type_freq(query[0]), ll, ul])
    
    
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
        
    st.sidebar.checkbox('Batch Mode')
    st.sidebar.checkbox('+\'ve Keywords Only')
    st.sidebar.checkbox('Case sensitive')
    
    st.sidebar.checkbox(    'Explore Reference Text',
                            disabled=True)    
        
    st.sidebar.text_input('Confidence Level (%)', value='95')
    
    st.sidebar.divider()
    
    st.sidebar.button('Extract Keywords', on_click=extract_keywords)