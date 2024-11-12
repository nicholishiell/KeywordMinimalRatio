import streamlit as st

from  KeywordExtractor import KeywordExtractor

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HOME_NAV_OPTION='Home'
SETUP_OPTION='Setup Analysis'
RESULTS_NAV_OPTION='View Results'

NAV_OPTIONS = [HOME_NAV_OPTION, SETUP_OPTION, RESULTS_NAV_OPTION]

TYPE_COLUMN = 'Type'
MINIMAL_RATIO_COLUMN = 'MR (Minimal Ratio)'
FREQ_IN_TEXT_COLUMN = 'Freq in Query Text'
FREQ_IN_REF_COLUMN = 'Freq in Reference Text'
LOWER_BOUND_COLUMN = 'Lower Confidence Bound'
UPPER_BOUND_COLUMN = 'Upper Confidence Bound'

RESULTS_COLUMNS = [TYPE_COLUMN, MINIMAL_RATIO_COLUMN, FREQ_IN_TEXT_COLUMN, 
                   FREQ_IN_REF_COLUMN, LOWER_BOUND_COLUMN, UPPER_BOUND_COLUMN]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Session State Keys
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

KEYWORD_EXTRACTOR_KEY = 'keyword_extractor'
QUERY_TEXT_KEY = 'query_text'
ANALYSIS_RESULTS_KEY = 'analysis_results'

USER_PAGE_SELECTION_KEY = 'user_page_selection'
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
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_page_index():
        
    return NAV_OPTIONS.index(st.session_state[USER_PAGE_SELECTION_KEY])


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~