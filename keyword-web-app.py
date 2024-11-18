import streamlit as st

from utils import *

from  KeywordExtractor import KeywordExtractor

from child_pages.HomePage import home_page
from child_pages.SetupPage import setup_page
from child_pages.ResultsPage import results_page

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def initialize_session_state():
        
    if KEYWORD_EXTRACTOR_KEY not in st.session_state:
        ke = KeywordExtractor() 
        ke.add_reference('ententen', 'resources/ententen12_lc_freq.txt')
        ke.select_reference('ententen')
    
        st.session_state[KEYWORD_EXTRACTOR_KEY] = ke
    
    if QUERY_TEXT_KEY not in st.session_state:
        st.session_state[QUERY_TEXT_KEY] = None
        
    if ANALYSIS_RESULTS_KEY not in st.session_state:
        st.session_state[ANALYSIS_RESULTS_KEY] = None
        
    if USER_PAGE_SELECTION_KEY not in st.session_state:
        st.session_state[USER_PAGE_SELECTION_KEY] = HOME_NAV_OPTION

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

def main():

    st.set_page_config( page_title="Minimal Ratio Keyword Extractor",
                        layout="wide")

    initialize_session_state()
    
    st.sidebar.title('Navigation')  

    st.session_state[USER_PAGE_SELECTION_KEY] = st.sidebar.radio(   'Pages', 
                                                                    options=NAV_OPTIONS)                                        
    
    if st.session_state[USER_PAGE_SELECTION_KEY] == HOME_NAV_OPTION:
        home_page()
    elif st.session_state[USER_PAGE_SELECTION_KEY] == SETUP_OPTION:
        setup_page()
    elif st.session_state[USER_PAGE_SELECTION_KEY] == RESULTS_NAV_OPTION:
        results_page()     
    else:
        home_page()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

if __name__=='__main__': 
    main()