import streamlit as st
import random

# Ensure session state is initialized
if "responses" not in st.session_state:
    st.session_state.responses = {}

questions_2 = [
    "Acts like a leader", "Has leadership abilities", "Strong personality",
    "Dominant", "Makes decisions easily", "Defends own beliefs",
]

questions_3 = [
    "Objective", "Error-free", "Neutral",
    "Accurate", "Cooperative", "Sociable", "Friendly",
    "Warm", "Knowledgeable", "Conscious", "Capable", "Reliable"
]

def cache_response(response):
    page_name = st.session_state.pages_name[st.session_state.page]
    st.session_state.responses[page_name] = response

def survey_page_1():
    questions = {
        "1": "What is your current age?",
        "2": "What is your gender?",
        "3": "What is your racial/ethnic category? (You can choose the closest one)",
        "4": "What is the highest degree or level of school you have completed?",
        "5": "Currently, what is your total annual household income before taxes?",
        "6": "Are you a native English speaker?",
        "7": "How will you rate your English proficiency on a 5-point scale?"
    }

    select_responses = {
        "2": ["Male", "Female", "Non-binary", "Prefer not to answer"],
        "3": ["American Indian or Alaskan Native", "Asian", "Black or African American", "Hispanic or Latinx", "White or Caucasian", "Other", "Prefer not to answer"],
        "4": ["No schooling completed", "High school graduate", "Bachelor's degree", "Master's degree", "Doctorate degree", "Other", "Prefer not to answer"],
        "5": ['$0 ~ $15,000', "$15,001 ~ $25,000", "$25,001 ~ $35,000", "$35,001 ~ $50,000", "$50,001 ~ $75,000", "$75,001 ~ $100,000", "$100,001 ~ $200,000", "More than $200,000", "Prefer not to answer"],
        "6": ["Yes", "No"],
        "7": ["1 (Elementary proficiency)", "2", "3", "4", "5 (Full bilingual proficiency)"]
    }

    response = {}
    
    for i, (qkey, question) in enumerate(questions.items()):
        st.write(f"> **{qkey}. {question}**")
        if qkey in select_responses:
            response[question] = st.radio(f"**{question}**", select_responses[qkey], key=f"select_{i}", label_visibility="collapsed")
        else:
            response[question] = st.text_input(f"**{question}**", key=f"text_{i}", label_visibility="collapsed")
    
    cache_response(response)

def survey_page_2():
    response = {val: None for val in questions_2}
    slider_labels = [1, 2, 3, 4, 5, 6, 7]

    if "shuffled_questions_survey_page_2" not in st.session_state:
        st.session_state.shuffled_questions_survey_page_2 = random.sample(questions_2, len(questions_2))

    questions = st.session_state.shuffled_questions_survey_page_2
    st.write("**8. How well does each of the following words describe you?**")
    
    for question in questions:
        st.write(f"> **{question}**")
        selected_value = st.slider(question, min_value=1, max_value=7, step=1, key=f"slider_{question}")
        response[question] = selected_value
    
    cache_response(response)

def survey_page_3():
    response = {val: None for val in questions_3}
    slider_labels = [1, 2, 3, 4, 5, 6, 7]

    if "shuffled_questions_survey_page_3" not in st.session_state:
        st.session_state.shuffled_questions_survey_page_3 = random.sample(questions_3, len(questions_3))

    questions = st.session_state.shuffled_questions_survey_page_3
    st.write("**9. How well does each of the following words describe artificial intelligence (AI)?**")

    for question in questions:
        st.write(f"> **{question}**")
        selected_value = st.slider(question, min_value=1, max_value=7, step=1, key=f"slider_{question}")
        response[question] = selected_value
    
    cache_response(response)

def survey_page_4():
    st.write("""
    There are AI chatbots that can produce text and images in response to the things people ask them for. 
    Sometimes called generative AI, these chatbots review large amounts of information to come up with their responses.
    """)

    questions = [
        "How well-informed do you consider yourself about generative AI chatbots (like ChatGPT, Claude, Gemini, Perplexity AI, etc.)?",
        "How often do you use generative AI chatbots?",
        "What do you use these AI chatbots for? (Choose all that apply)"
    ]
    
    response = {}

    st.write(f"> **10. {questions[0]}**")
    response[questions[0]] = st.slider(questions[0], min_value=1, max_value=7, step=1, key=f"slider_{questions[0]}")
    
    options_11 = ["Never", "Used once or twice", "Use sometimes", "Use regularly"]
    st.write(f"> **11. {questions[1]}**")
    response[questions[1]] = st.radio(f"11. {questions[1]}", options_11, key="select_11", label_visibility="collapsed")

    if response[questions[1]] != "Never":
        st.write(f"> **12. {questions[2]}**")
        response[questions[2]] = st.multiselect(
            questions[2],
            ["For entertainment", "To find new information related to my hobbies or interests", "For work", "For education and self-development", "Other"],
            key="multiselect_12"
        )
    else:
        response[questions[2]] = "N/A"
    
    cache_response(response)
