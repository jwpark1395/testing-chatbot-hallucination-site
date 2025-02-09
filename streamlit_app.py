import streamlit as st
import json
import random

def wide_space_default():
    st.set_page_config(layout="wide")
    # Add custom CSS to hide the menu
    hide_menu = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_menu, unsafe_allow_html=True)
    
wide_space_default()

import pandas as pd
from io import BytesIO

from contents.consent import consent_page, thanks_page, intro_page
from contents.survey import *
from contents.interaction import *
from contents.post_interaction import *



# Initialize the page state in session_state
if "page" not in st.session_state:
    st.session_state.page = 0
# Agree flag
if "agree" not in st.session_state:
    st.session_state.agree = False

# Initialize confidence conditions
if "confidence_conditions" not in st.session_state:
    # Create a list of 10 repetitions of each condition
    base_conditions = [0, 1, 2, 3, 4, 6, 7, 8] * 10
    random.shuffle(base_conditions)
    st.session_state.confidence_conditions = base_conditions
    st.session_state.assigned_conditions = {}  # Dictionary to store PID -> condition mappings
    st.session_state.total_assignments = 0

def load_assigned_conditions():
    """Load existing condition assignments"""
    try:
        with open('assigned_conditions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_assigned_conditions(assigned_conditions):
    """Save condition assignments"""
    with open('assigned_conditions.json', 'w') as f:
        json.dump(assigned_conditions, f)

def load_available_conditions():
    """Load or create available conditions"""
    try:
        with open('available_conditions.json', 'r') as f:
            state = json.load(f)
    except FileNotFoundError:
        base_conditions = [0, 1, 2, 3, 4, 5, 6, 7, 8] * 10  # Now includes 5
        random.shuffle(base_conditions)
        state = {
            'available_conditions': base_conditions,
            'total_assignments': 0
        }
        save_available_conditions(state)
    return state

def save_available_conditions(state):
    """Save available conditions state"""
    with open('available_conditions.json', 'w') as f:
        json.dump(state, f)

def get_confidence_condition(prolific_pid):
    if prolific_pid is None:
        return 0  # Default condition for testing/debugging
    
    # First check if this user already has an assigned condition
    assigned_conditions = load_assigned_conditions()
    if prolific_pid in assigned_conditions:
        return assigned_conditions[prolific_pid]
    
    # If not, get state of available conditions
    state = load_available_conditions()
    
    # Reset conditions list if we've assigned 90 conditions
    if state['total_assignments'] % 90 == 0 and state['total_assignments'] > 0:
        base_conditions = [0, 1, 2, 3, 4, 5, 6, 7, 8] * 10  # Now includes 5
        random.shuffle(base_conditions)
        state['available_conditions'] = base_conditions
    
    # Assign new condition
    try:
        condition = state['available_conditions'].pop()
        state['total_assignments'] += 1
        
        # Save the assignment both to assigned conditions and available conditions state
        assigned_conditions[prolific_pid] = condition
        save_assigned_conditions(assigned_conditions)
        save_available_conditions(state)
        
        return condition
    except IndexError:
        # If we somehow run out of conditions, reset the list
        base_conditions = [0, 1, 2, 3, 4, 5, 6, 7, 8] * 10  # Now includes 5
        random.shuffle(base_conditions)
        state['available_conditions'] = base_conditions
        condition = state['available_conditions'].pop()
        assigned_conditions[prolific_pid] = condition
        save_assigned_conditions(assigned_conditions)
        save_available_conditions(state)
        return condition

# Function to handle page changes
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

def check_response_is_not_none(check_page=["survey_page_1", "survey_page_2", "survey_page_3", "survey_page_4",
                                                  "post_page_1", "post_page_2", "post_page_3", "post_page_4"]):
    # Display collected responses
    page_name = st.session_state.pages_name[st.session_state.page]
    if page_name in check_page:
        cur_response = st.session_state.responses[page_name]
        # cur_response is a nested dictionary. check if all values are not None
        for key, value in cur_response.items():
            if value is None:
                return False
        return True
    else:
        return True

def display_debug_info():
    """Display debug information in the sidebar"""
    with st.sidebar:
        st.markdown("### Debug Information")
        
        # Current user info
        st.markdown("#### Current User")
        st.write(f"Prolific ID: {st.session_state.prolific_pid}")
        st.write(f"Confidence Condition: {st.session_state.confidence_condition}")
        st.write(f"Current Page: {st.session_state.pages_name[st.session_state.page]}")
        

        # Load and display all assignments
        st.markdown("#### All Assigned Conditions")
        try:
            with open('assigned_conditions.json', 'r') as f:
                assigned = json.load(f)
                st.json(assigned)
        except FileNotFoundError:
            st.write("No assigned conditions file found")
        
        # Available conditions info
        st.markdown("#### Available Conditions State")
        try:
            with open('available_conditions.json', 'r') as f:
                available = json.load(f)
                st.write(f"Total Assignments: {available['total_assignments']}")
                st.write(f"Remaining Conditions: {len(available['available_conditions'])}")
                st.write("Available Conditions:")
                st.json(available['available_conditions'])
        except FileNotFoundError:
            st.write("No available conditions file found")

# Main function to control the flow
def main():
    pages = [intro_page, consent_page, thanks_page, 
             survey_page_1, survey_page_2, survey_page_3_intro, survey_page_3, survey_page_4, 
             interaction_intro, interaction_page,
             post_intro, post_page_1, post_page_2, post_page_3, post_page_4, debrief, closing_page]

    st.session_state.pages_name = [f.__name__ for f in pages]
    if "interaction_done" not in st.session_state:
        st.session_state.interaction_done= False
    if "all_done" not in st.session_state:
        st.session_state.all_done = False

    # Set up responses state
    if "responses" not in st.session_state:
        st.session_state.responses = {}
        query_params = st.query_params
        if "PROLIFIC_PID" in query_params:
            prolific_pid = query_params["PROLIFIC_PID"]
            st.session_state.prolific_pid = prolific_pid
            # Assign confidence condition
            st.session_state.confidence_condition = get_confidence_condition(prolific_pid)
        else:
            st.session_state.prolific_pid = None
            st.session_state.confidence_condition = random.randint(0, 8)
    
    # Display debug information
    display_debug_info()
    
    # Display the current page
    pages[st.session_state.page]()
    col1, _, _, _, col2 = st.columns(5)
    # with col1:
    #     # if st.session_state.page > 0 and not st.session_state.all_done:
    #     if st.session_state.page > 0:
    #         st.button("Previous", on_click=prev_page)

    with col2:
        if st.session_state.page == 0 or st.session_state["agree"]:
            if not (st.session_state.page == st.session_state.pages_name.index("interaction_page") and not st.session_state.interaction_done):
                if st.session_state.page < (len(pages)-2):
                    if not check_response_is_not_none():
                        st.warning("You must answer all questions to proceed.")
                    else:
                        st.button("Next", on_click=next_page)

if __name__ == "__main__":
    main()