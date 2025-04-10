import streamlit as st
import time
import pandas as pd
import random

def read_hallucinations():
    df = pd.read_excel("contents/hallucinations.xlsx", sheet_name="Sheet1")
    questions = df[['Question', 'Hallucination']].values.tolist()
    random.shuffle(questions)
    return questions

def select_random_condition():
    conditions = {0: 13 * ["None"],
                  1: 4 * ["60%"] + 5 * ["80%"] + 4 * ["100%"],
                  2: 1 * ["60%"] + 11 * ["80%"] + 1 * ["100%"],
                  3: 4 * ["40%"] + 5 * ["60%"] + 4 * ["80%"],
                  4: 1 * ["40%"] + 11 * ["60%"] + 1 * ["80%"],
                  5: 4 * ["quite"] + 5 * ["highly"] + 4 * ["extremely"],
                  6: 1 * ["quite"] + 11 * ["highly"] + 1 * ["extremely"],
                  7: 4 * ["fairly"] + 5 * ["quite"] + 4 * ["highly"],
                  8: 1 * ["fairly"] + 11 * ["quite"] + 1 * ["highly"],
                  }
    idx = st.session_state.confidence_condition

    condition = conditions[idx]
    random.shuffle(condition)
    
    if idx > 0:
        return [f"Confidence: I am {c} confident" for c in condition], idx
    else:
        return condition, idx

def interaction_intro():
    st.write("""
    Now, you will interact with an AI chatbot. 
    You will ask the chatbot some questions and it will respond. 
    Please read the instructions below carefully.

    >
    > 1. On the next page, you will see a list of questions. **__Select__** one question to ask the chatbot.
    > 2. Carefully review the chatbot's answer and its confidence level.
    > 3. Rate the accuracy of the answer. 
    >

    You will ask the chatbot a total of 13 different questions. Click **__Next__** if you are ready to begin.

    """)
    st.markdown("""
        <style>
            strong strong {
                text-decoration: underline;
            }
        </style>
    """, unsafe_allow_html=True)

def type_effect(text, container, speed=0.03):
    """Helper function to create typing effect"""
    placeholder = container.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        placeholder.markdown(displayed_text)
        time.sleep(speed)
    return displayed_text

def interaction_page():
    # Initialize session state variables for interaction box, responses, and AI thinking state
    if "interaction_box" not in st.session_state:
        st.session_state.interaction_box = ""  # For input box
    if "h_responses" not in st.session_state:
        st.session_state.h_responses= []  # To store chat interactions
    if "ai_thinking" not in st.session_state:
        st.session_state.ai_thinking = 0  # To track AI thinking state
    if "last_response" not in st.session_state:
        st.session_state.last_response = None # To store last AI response
    if "questions" not in st.session_state and "answers" not in st.session_state:
        hallucinations = read_hallucinations()
        st.session_state.questions = [data[0] for data in hallucinations]
        st.session_state.original_questions= [data[0] for data in hallucinations]
        st.session_state.answers = {item[0]: item[1] for item in hallucinations}
    if "confidence" not in st.session_state:
        st.session_state.confidence, st.session_state.cfd_idx = select_random_condition()
    if "experiments" not in st.session_state:
        st.session_state.experiments = []
    if 'cfd' not in st.session_state:
        st.session_state.cfd = "None"

    # Instructions
    #st.markdown("""
       #<style>
        #    .stHorizontalBlock > div:first-child {
         #       height: fit-content;
          #      padding-right: 20px;
           #     border-right: 1px solid #ccc;
            #}
            #.st-emotion-cache-t1wise {
             #   height: 100vh;
              #  padding-top: 0rem;
               # padding-bottom: 0rem;
            #}
            #.st-emotion-cache-t1wise > div,
            #.st-emotion-cache-t1wise > div > div {
             #   height: 100vh;
            #}
            #div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > .st-key-intro) {
             #   height: 150px;
            #}
            #div:has(> .st-key-intro) {
             #   height: 100%;
            #}
       #     .st-key-intro {
        #        width: 40vw;
         #       min-width: 615px;
          #      background: #0068c9;
           #     padding: 5px 10px 5px;
            #    border-radius: 10px;
        #    }
        #    .st-key-intro h3 {
            #    padding: 0px 0 5px;
        #    }
         #   .st-key-intro h3,
         #   .st-key-intro p {
         #       color: #fff;
       #     }
        #    .st-key-intro p strong:last-child {
         #       display: block;
           #     margin: 0 0 0 0;
         #       font-size: 13px;
           #     padding: 0 0 0 8px;
          #      text-indent: 10px;
    #        }
   #     </style>
  #  """, unsafe_allow_html=True)
  #  Instructions = st.container(height=200, border=False, key="intro")
  #  Instructions.write("### Instructions")
  #  Instructions.markdown(f"""
   # **1. Choose a question from the list below, then click submit.**  
   # **2. The question will appear in the chat box.**  
    #**3. Click the arrow button to see the chatbot's response.**  
    #**<If you want to change your question, you can select a new one from the list and then click the arrow.>**  
    #""")

    # Layout with two columns
    col1, col2 = st.columns([1, 1.2])
    
    st.markdown("""
        <style>
            div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > .st-key-q_list) {
                height: calc(100vh - 310px);
                background: #f4f4f4;
                border-radius: 10px;
            }
            div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > .st-key-q_list)::-webkit-scrollbar {
                width: 15px;
                background-color: #f4f4f4;
            }
            
            div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > .st-key-q_list)::-webkit-scrollbar-thumb {
                # background: #e89a3e; /* 스크롤바 막대 색상 */
                border: 5px solid #f4f4f4; /* 스크롤바 막대 테두리 설정  */
                border-radius: 12px 12px 12px 12px;
            }
            
            .st-key-q_list {
                background: #f4f4f4;
                padding: 10px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Left column: Question list with auto-paste feature
    with col1:
        # Instructions
        st.markdown("""
           <style>
                .stHorizontalBlock > div:first-child {
                    height: fit-content;
                    padding-right: 20px;
                    border-right: 1px solid #ccc;
                }
                .st-emotion-cache-t1wise {
                    height: 100vh;
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                }
                .st-emotion-cache-t1wise > div,
                .st-emotion-cache-t1wise > div > div {
                    height: 100vh;
                }
                div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > .st-key-intro) {
                    height: 150px;
                }
                div:has(> .st-key-intro) {
                    height: 100%;
                }
                .st-key-intro {
                    width: 30vw;
                    min-width: 400px;
                    max-width: 500px;
                    background: #0068c9;
                    padding: 5px 10px 5px;
                    border-radius: 10px;
                }
                .st-key-intro h4 {
                    padding: 0px 0 5px;
                }
                .st-key-intro h,
                .st-key-intro p {
                    color: #fff;
                }
                .st-key-intro p strong:last-child {
                    display: block;
                    margin: 0 0 0 0;
                    font-size: 14px;
                    padding: 0 0 0 8px;
                    text-indent: 10px;
                }
            </style>
        """, unsafe_allow_html=True)
        Instructions = st.container(height=200, border=False, key="intro")
        Instructions.write("### Instructions")
        Instructions.markdown(f"""
        **1. Choose a question from the list below, then click submit.**  
        **2. The question will appear in the chat box.**  
        **3. Click the arrow button to see the chatbot's response.**  
        **<If you want to change your question, you can select a new one from the list and then click the arrow.>**  
        """)

        st .write("### Question List")
        container = st.container(height=600, border=False, key="q_list")
        selected_question = container.radio(
            "Click a question:",
            options=st.session_state.questions,
            index=None,
            label_visibility="collapsed"
        )

        # Add submit button for the selected question
        if selected_question and st.session_state.ai_thinking == 0:
            st.session_state.interaction_box = selected_question  # Only paste when submit is clicked

    # Right column: Chat window and interaction box
    with col2:
        st.write("### Chat Box")
        
        chat_container = st.container(height=420, border=False, key="chat_box")
        st.markdown("""
            <style>
                div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > .st-key-chat_box) {
                    height: calc(100vh - 440px);
                }
                div:has(> .st-key-chat_box) {
                    height: 100%;
                }
                .st-key-chat_box {
                    display: flex;
                    flex-direction: column;
                    gap: 0;
                }
                .st-key-chat_box * {
                    margin: 0;
                }
            
                button[kind="pills"]:first-child,
                button[kind="pills"]:last-child,
                button[kind="pills"]:focus:first-child,
                button[kind="pills"]:focus:last-child,
                button[kind="pillsActive"]:first-child,
                button[kind="pillsActive"]:last-child,
                button[kind="pillsActive"]:focus:first-child,
                button[kind="pillsActive"]:focus:last-child
                {
                    color: inherit;
                    background: #fff;
                    border: none;
                    box-shadow: none;
                    pointer-events: none;
                }
            </style>
        """, unsafe_allow_html=True)
        with chat_container:
            # Display chat history (all user questions, AI responses, and thinking messages)
            for interaction in st.session_state.h_responses:
                st.markdown(interaction, unsafe_allow_html=True)

            # Create a persistent container for new messages
            message_container = st.empty()

            # Handle AI response after "thinking"
            if st.session_state.ai_thinking == 0 and not st.session_state.last_response:
                st.markdown("""
                    <div class="float_message" style="
                        position: fixed;
                        top: 50%;
                        left: 60%;
                        padding: 5px 10px;
                        color: #243686;
                        font-weight: 700;
                        border: 1px solid #243686;
                        border-radius: 100px;
                        user-select: none;
                        pointer-events: none;
                    ">
                    Select one of the questions from the left and click the arrow
                    </div>
                """, unsafe_allow_html=True)
                
            # Handle AI response after "thinking"
            if st.session_state.ai_thinking == 1:
                time.sleep(2)  # 🚀 2초 동안 "생각 중"

                # 🚀 "..." 제거 & AI 타이핑 준비 상태(2)로 변경
                st.session_state.h_responses = [
                    msg for msg in st.session_state.h_responses if """<div class="loader"></div>""" not in msg
                ]
                st.session_state.ai_thinking = 2  # ✅ "답변 출력" 상태로 변경
                st.rerun()  # 🚀 UI 업데이트 후 타이핑 시작

            # Handle AI response after "thinking"
            if st.session_state.ai_thinking == 2:
                fail_msg = "Sorry, I don't know the answer to that question. You may ask the question from the list!"
                ai_response_text = st.session_state.answers.get(st.session_state.user_question, fail_msg)
                fail = ai_response_text == fail_msg

                # Start with the div styling
                base_message = """
                <div style="display: flex; gap: 10px; padding: 0 40px 5px 0;">
                    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB8AAAAfCAYAAAAfrhY5AAAACXBIWXMAAAsSAAALEgHS3X78AAAD9klEQVRIicWXT4jbRRTHP41bPKibCNZr08NchHZXRAZ62dSTB8GIXgoFUxBBLPZXEO2ckr04CAVTUOitya2gYFDvuzkOHkzNcRCTiwh62NWLxT/rYd4k85v97WYrBR+E32/mzW++b968930vpw4ODvi/ZO2kC5W2bWAzmZoBI+/M3n8FP7Xq5ALaB85WqPeBvnem98jBlbYd4K4Mh8AgUbeBDlAHfgCekfco94GBd6b/0OBK2xawQzhd2zuzm+kbwE3gfeAxWTdJlmwlRnS8M6luJfiubPCad2aU6dKrqHS90rYpa14F5sBmHh+V4ErbTeA7YOydaWXz/eRUQ6A4LuiUtgPgTWA7N/BQtIs7P5DhKJnvA9dlOAZ66VUobd8AbgHfeGeuJVsWhPgogBJ46eRK254sioFz2TtzT3QHBBcX3plB8s154GvK2fAAuOKd+SI7/aXU4FqyyQDoJicD+JmyTDLgMfB9AjyX5+PA50rbmRgXAVOeCG5X2hZi2T7QIrhpiyNEafsp8G4y9SvwkndmKvqZGHRWjItGzdJ9anLHPRm3qlIikTNK2z8zYIDTwAtx4J1pAheA32UqeuZSCZzgijpwewUwwHMsg/Qz4Gngtnx/V2k7FX7AOzP1zqzLur/lm/eUth/GzdYIboblvaySqXfmQjIuJF7uABrYUdoOCdkwk8i/prT9DXgK+Aj4OJ48ykkKxDgDBkA8dlOG+4T4mUj2xDXrhCyoSaCWwJsVYG2JiYeRO8C2vHeVtik7XpHnxQgelZ1k0UBOcB2YSYE5qfwhTBbTamF8zHskbmrisjmwJZyNd2ZG8MQimPKNKuTJdCB7VMlf8SW6vSPPQRKte96ZAjjHknQ2lLYjKRoLEZ64d4xhqawB/yzAhfKuEk65kwJIxLYIOTonVKkflbY9pe0rStsJ8AnwxCpUISdK4AIyINReMoBGNFDI4waBPLoETt8geObyCuDzwDsy/KoELrIhBmwTAq5LEnBiSIOQrwC/EIpFi8N1IAeeCN4D78zrVeDRCz1CwA1ZstcugZu7YtgN78yzeYdTIRcJ/F4juPvFqMjBx4SgakrAdYDnZX5LDBkCzbQ3E8/ElM3J6rQ8YzczjYq8mRgJSCG/yF4t6WL20hSSzOgTrguSJjMhp5+Al1PQKHkz0SC4tg5cTWt3KpIJPQKNQvBMkRYmodYuoWAVVfsc6uGEaL5MTtKPmybl9y1Cas0FNG8wNwmFqg6cO4pwjmogWwT3Vf1RiHKfUP9LdyzAI/n2UNO4Elw2aRA6mjZlWv0WeBtYJ0T9iGWHskngCIChBOyRsvLv0jGG9cWweqauvIpHBp4Z0kqGeyfohhbyLyVMxSKyo1EIAAAAAElFTkSuQmCC"
                        width="30" height="30" style="margin: 6px 0;">
                    <div style="
                        display: flex;
                        background-color: #e9f2ff; 
                        padding: 10px;
                        border-radius: 10px; 
                        color: black; 
                        width: fit-content;
                        font-size: 16px;
                        margin-bottom: 5px;">
                """
                
                # Perform typing effect with the styled div
                displayed_text = base_message
                for char in ai_response_text:
                    displayed_text += char
                    message_container.markdown(displayed_text + "</div></div>", unsafe_allow_html=True)
                    time.sleep(0.02)
                
                typed_response = ai_response_text
                
                # Create final message with typed response
                ai_message = f"""
                <div style="display: flex; gap: 10px; padding: 0 40px 5px 0;">
                    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB8AAAAfCAYAAAAfrhY5AAAACXBIWXMAAAsSAAALEgHS3X78AAAD9klEQVRIicWXT4jbRRTHP41bPKibCNZr08NchHZXRAZ62dSTB8GIXgoFUxBBLPZXEO2ckr04CAVTUOitya2gYFDvuzkOHkzNcRCTiwh62NWLxT/rYd4k85v97WYrBR+E32/mzW++b968930vpw4ODvi/ZO2kC5W2bWAzmZoBI+/M3n8FP7Xq5ALaB85WqPeBvnem98jBlbYd4K4Mh8AgUbeBDlAHfgCekfco94GBd6b/0OBK2xawQzhd2zuzm+kbwE3gfeAxWTdJlmwlRnS8M6luJfiubPCad2aU6dKrqHS90rYpa14F5sBmHh+V4ErbTeA7YOydaWXz/eRUQ6A4LuiUtgPgTWA7N/BQtIs7P5DhKJnvA9dlOAZ66VUobd8AbgHfeGeuJVsWhPgogBJ46eRK254sioFz2TtzT3QHBBcX3plB8s154GvK2fAAuOKd+SI7/aXU4FqyyQDoJicD+JmyTDLgMfB9AjyX5+PA50rbmRgXAVOeCG5X2hZi2T7QIrhpiyNEafsp8G4y9SvwkndmKvqZGHRWjItGzdJ9anLHPRm3qlIikTNK2z8zYIDTwAtx4J1pAheA32UqeuZSCZzgijpwewUwwHMsg/Qz4Gngtnx/V2k7FX7AOzP1zqzLur/lm/eUth/GzdYIboblvaySqXfmQjIuJF7uABrYUdoOCdkwk8i/prT9DXgK+Aj4OJ48ykkKxDgDBkA8dlOG+4T4mUj2xDXrhCyoSaCWwJsVYG2JiYeRO8C2vHeVtik7XpHnxQgelZ1k0UBOcB2YSYE5qfwhTBbTamF8zHskbmrisjmwJZyNd2ZG8MQimPKNKuTJdCB7VMlf8SW6vSPPQRKte96ZAjjHknQ2lLYjKRoLEZ64d4xhqawB/yzAhfKuEk65kwJIxLYIOTonVKkflbY9pe0rStsJ8AnwxCpUISdK4AIyINReMoBGNFDI4waBPLoETt8geObyCuDzwDsy/KoELrIhBmwTAq5LEnBiSIOQrwC/EIpFi8N1IAeeCN4D78zrVeDRCz1CwA1ZstcugZu7YtgN78yzeYdTIRcJ/F4juPvFqMjBx4SgakrAdYDnZX5LDBkCzbQ3E8/ElM3J6rQ8YzczjYq8mRgJSCG/yF4t6WL20hSSzOgTrguSJjMhp5+Al1PQKHkz0SC4tg5cTWt3KpIJPQKNQvBMkRYmodYuoWAVVfsc6uGEaL5MTtKPmybl9y1Cas0FNG8wNwmFqg6cO4pwjmogWwT3Vf1RiHKfUP9LdyzAI/n2UNO4Elw2aRA6mjZlWv0WeBtYJ0T9iGWHskngCIChBOyRsvLv0jGG9cWweqauvIpHBp4Z0kqGeyfohhbyLyVMxSKyo1EIAAAAAElFTkSuQmCC"
                        width="30" height="30" style="margin: 6px 0;">
                    <div style="
                        display: flex;
                        background-color: #e9f2ff; 
                        padding: 10px;
                        border-radius: 10px; 
                        color: black; 
                        width: fit-content;
                        font-size: 16px;
                        margin-bottom: 5px;">
                        <span>{typed_response}</span>
                    </div>
                </div>
                """
                
                if not fail:
                    st.session_state.cfd = st.session_state.confidence.pop()
                else:
                    st.session_state.cfd = "None"
                
                if st.session_state.cfd != "None":
                    ai_message = f"""
                    <div style="display: flex; gap: 10px; padding: 0 40px 5px 0;">
                        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB8AAAAfCAYAAAAfrhY5AAAACXBIWXMAAAsSAAALEgHS3X78AAAD9klEQVRIicWXT4jbRRTHP41bPKibCNZr08NchHZXRAZ62dSTB8GIXgoFUxBBLPZXEO2ckr04CAVTUOitya2gYFDvuzkOHkzNcRCTiwh62NWLxT/rYd4k85v97WYrBR+E32/mzW++b968930vpw4ODvi/ZO2kC5W2bWAzmZoBI+/M3n8FP7Xq5ALaB85WqPeBvnem98jBlbYd4K4Mh8AgUbeBDlAHfgCekfco94GBd6b/0OBK2xawQzhd2zuzm+kbwE3gfeAxWTdJlmwlRnS8M6luJfiubPCad2aU6dKrqHS90rYpa14F5sBmHh+V4ErbTeA7YOydaWXz/eRUQ6A4LuiUtgPgTWA7N/BQtIs7P5DhKJnvA9dlOAZ66VUobd8AbgHfeGeuJVsWhPgogBJ46eRK254sioFz2TtzT3QHBBcX3plB8s154GvK2fAAuOKd+SI7/aXU4FqyyQDoJicD+JmyTDLgMfB9AjyX5+PA50rbmRgXAVOeCG5X2hZi2T7QIrhpiyNEafsp8G4y9SvwkndmKvqZGHRWjItGzdJ9anLHPRm3qlIikTNK2z8zYIDTwAtx4J1pAheA32UqeuZSCZzgijpwewUwwHMsg/Qz4Gngtnx/V2k7FX7AOzP1zqzLur/lm/eUth/GzdYIboblvaySqXfmQjIuJF7uABrYUdoOCdkwk8i/prT9DXgK+Aj4OJ48ykkKxDgDBkA8dlOG+4T4mUj2xDXrhCyoSaCWwJsVYG2JiYeRO8C2vHeVtik7XpHnxQgelZ1k0UBOcB2YSYE5qfwhTBbTamF8zHskbmrisjmwJZyNd2ZG8MQimPKNKuTJdCB7VMlf8SW6vSPPQRKte96ZAjjHknQ2lLYjKRoLEZ64d4xhqawB/yzAhfKuEk65kwJIxLYIOTonVKkflbY9pe0rStsJ8AnwxCpUISdK4AIyINReMoBGNFDI4waBPLoETt8geObyCuDzwDsy/KoELrIhBmwTAq5LEnBiSIOQrwC/EIpFi8N1IAeeCN4D78zrVeDRCz1CwA1ZstcugZu7YtgN78yzeYdTIRcJ/F4juPvFqMjBx4SgakrAdYDnZX5LDBkCzbQ3E8/ElM3J6rQ8YzczjYq8mRgJSCG/yF4t6WL20hSSzOgTrguSJjMhp5+Al1PQKHkz0SC4tg5cTWt3KpIJPQKNQvBMkRYmodYuoWAVVfsc6uGEaL5MTtKPmybl9y1Cas0FNG8wNwmFqg6cO4pwjmogWwT3Vf1RiHKfUP9LdyzAI/n2UNO4Elw2aRA6mjZlWv0WeBtYJ0T9iGWHskngCIChBOyRsvLv0jGG9cWweqauvIpHBp4Z0kqGeyfohhbyLyVMxSKyo1EIAAAAAElFTkSuQmCC"
                            width="30" height="30" style="margin: 6px 0;">
                        <div style="
                            display: flex;
                            background-color: #e9f2ff; 
                            padding: 10px;
                            border-radius: 10px; 
                            color: black; 
                            width: fit-content;
                            font-size: 16px;
                            margin-bottom: 5px;">
                            <span>{typed_response}</span>
                        </div>
                    </div>
                    <div style="display: flex; gap: 10px; padding: 0 40px 5px 0;">
                        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB8AAAAfCAYAAAAfrhY5AAAACXBIWXMAAAsSAAALEgHS3X78AAAD9klEQVRIicWXT4jbRRTHP41bPKibCNZr08NchHZXRAZ62dSTB8GIXgoFUxBBLPZXEO2ckr04CAVTUOitya2gYFDvuzkOHkzNcRCTiwh62NWLxT/rYd4k85v97WYrBR+E32/mzW++b968930vpw4ODvi/ZO2kC5W2bWAzmZoBI+/M3n8FP7Xq5ALaB85WqPeBvnem98jBlbYd4K4Mh8AgUbeBDlAHfgCekfco94GBd6b/0OBK2xawQzhd2zuzm+kbwE3gfeAxWTdJlmwlRnS8M6luJfiubPCad2aU6dKrqHS90rYpa14F5sBmHh+V4ErbTeA7YOydaWXz/eRUQ6A4LuiUtgPgTWA7N/BQtIs7P5DhKJnvA9dlOAZ66VUobd8AbgHfeGeuJVsWhPgogBJ46eRK254sioFz2TtzT3QHBBcX3plB8s154GvK2fAAuOKd+SI7/aXU4FqyyQDoJicD+JmyTDLgMfB9AjyX5+PA50rbmRgXAVOeCG5X2hZi2T7QIrhpiyNEafsp8G4y9SvwkndmKvqZGHRWjItGzdJ9anLHPRm3qlIikTNK2z8zYIDTwAtx4J1pAheA32UqeuZSCZzgijpwewUwwHMsg/Qz4Gngtnx/V2k7FX7AOzP1zqzLur/lm/eUth/GzdYIboblvaySqXfmQjIuJF7uABrYUdoOCdkwk8i/prT9DXgK+Aj4OJ48ykkKxDgDBkA8dlOG+4T4mUj2xDXrhCyoSaCWwJsVYG2JiYeRO8C2vHeVtik7XpHnxQgelZ1k0UBOcB2YSYE5qfwhTBbTamF8zHskbmrisjmwJZyNd2ZG8MQimPKNKuTJdCB7VMlf8SW6vSPPQRKte96ZAjjHknQ2lLYjKRoLEZ64d4xhqawB/yzAhfKuEk65kwJIxLYIOTonVKkflbY9pe0rStsJ8AnwxCpUISdK4AIyINReMoBGNFDI4waBPLoETt8geObyCuDzwDsy/KoELrIhBmwTAq5LEnBiSIOQrwC/EIpFi8N1IAeeCN4D78zrVeDRCz1CwA1ZstcugZu7YtgN78yzeYdTIRcJ/F4juPvFqMjBx4SgakrAdYDnZX5LDBkCzbQ3E8/ElM3J6rQ8YzczjYq8mRgJSCG/yF4t6WL20hSSzOgTrguSJjMhp5+Al1PQKHkz0SC4tg5cTWt3KpIJPQKNQvBMkRYmodYuoWAVVfsc6uGEaL5MTtKPmybl9y1Cas0FNG8wNwmFqg6cO4pwjmogWwT3Vf1RiHKfUP9LdyzAI/n2UNO4Elw2aRA6mjZlWv0WeBtYJ0T9iGWHskngCIChBOyRsvLv0jGG9cWweqauvIpHBp4Z0kqGeyfohhbyLyVMxSKyo1EIAAAAAElFTkSuQmCC"
                            width="30" height="30" style="margin: 6px 0; opacity: 0;">
                        <div style="
                            background-color: #e9f2ff; 
                            padding: 10px; 
                            border-radius: 10px; 
                            color: black; 
                            width: fit-content; 
                            font-size: 17px;
                            margin-bottom: 5px;
                            font-weight: bold;">
                            <span>{st.session_state.cfd}</span>
                        </div>
                    </div>
                    """

                if fail:
                    st.session_state.last_response = None
                else:
                    st.session_state.last_response = ai_response_text
                
                # Replace "thinking" message with the actual response
                st.session_state.h_responses.append(ai_message)
                st.session_state.ai_thinking = 0  # Reset AI thinking state
                st.rerun()

    # After conversation, collect user feedback
    with col2:
        with chat_container:
            if st.session_state.last_response:
                opinion_container = st.container(height=170, border=True, key="opinion")
                st.markdown("""
                    <style>
                        div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > .st-key-opinion) {
                            width: 550px;
                            height: 150px;
                            margin: auto auto 0;
                            padding: 10px;
                            border: 2px solid #243686;
                            border-radius: 30px;
                        }
                        div:has(> .st-key-opinion) {
                            height: 100%;
                        }
                        .st-key-opinion {
                            display: flex;
                            flex-direction: column;
                            justify-content: space-between;
                            align-items: center;
                            gap: 0;
                        }
                        .st-key-opinion * {
                            margin: 0;
                        }
                    
                        button[kind="pills"]:first-child,
                        button[kind="pills"]:last-child,
                        button[kind="pills"]:focus:first-child,
                        button[kind="pills"]:focus:last-child,
                        button[kind="pillsActive"]:first-child,
                        button[kind="pillsActive"]:last-child,
                        button[kind="pillsActive"]:focus:first-child,
                        button[kind="pillsActive"]:focus:last-child
                        {
                            color: inherit;
                            background: #fff;
                            border: none;
                            box-shadow: none;
                            pointer-events: none;
                        }
                    </style>
                """, unsafe_allow_html=True)
                with opinion_container:
                    # st.write("---")
                    # st.write("### :red[In your opinion, how accurate is this response?]")
                    st.write("**How accurate do you think this response is?**")
                    feedback = st.pills(
                        "C1. In your opinion, how accurate is this response?",
                        options=["(Not at all accurate)", "1", "2", "3", "4", "5", "6", "7", "(Very accurate)"],
                        label_visibility="collapsed"
                    )
                    
                    
                    if len(st.session_state.confidence) > 0:
                        st.markdown("""<div style="color: #FF2B2B; font-size: 14px;">If you are ready to proceed, click “Next”</div>""", unsafe_allow_html=True)
                        if st.button("Next", key="next_btn"):
                            if feedback is not None and "(" not in feedback[0]:
                                st.session_state.h_responses = []
                                st.session_state.last_response = None
                                st.session_state.experiments.append([st.session_state.user_question, st.session_state.cfd, feedback, st.session_state.question_idx, st.session_state.cfd_idx])
                                st.rerun()
                    else:
                        st.markdown("""<div style="font-size: 18px; font-weight: 700;">Done! Please proceed to the next stage of the study.</div>""", unsafe_allow_html=True)
                        if st.button("Next", key="next_done_btn"):
                            if feedback is not None and "(" not in feedback[0]:
                                if not st.session_state.interaction_done:
                                    st.session_state.experiments.append([st.session_state.user_question, st.session_state.cfd, feedback, st.session_state.question_idx, st.session_state.cfd_idx])
                                    st.session_state.page += 1
                                    st.rerun()
                                # st.session_state.interaction_done = True
        
        # Interaction box below the chat window
        # if st.session_state.last_response is None:
        st.markdown("""<hr style="margin: -10px 40px 0;">""", unsafe_allow_html=True)
        # st.write("### Type your question here")
        # st.write("*(select one of the questions from the left)*")
        chattext_container = st.container(border=False, key="chattext")
        st.markdown("""
            <style>
                div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > .st-key-chattext) {
                    height: 50px;
                    margin: 0 40px -25px;
                    padding: 5px;
                    border-radius: 10px;
                    box-shadow: 0px 0px 8px #ccc;
                }
                div:has(> .st-key-chattext) {
                    height: 100%;
                }
                .st-key-chattext {
                    display: flex;
                    flex-direction: row;
                    justify-content: space-between;
                }
                .st-key-input_box {
                    width: 100%;
                }
                .st-key-input_box div {
                    color: #000;
                    border: none;
                    background-color: transparent;
                }
                .st-key-input_box input {
                    color: #000;
                    -webkit-text-fill-color: #000;
                    cursor: default;
                }
                .st-key-input_box input::placeholder {
                    color: #ccc;
                    -webkit-text-fill-color: #ccc;
                }
                .st-key-chattext div:last-child {
                    align-self: flex-end;
                }
            </style>
        """, unsafe_allow_html=True)
        with chattext_container:
            user_input = st.text_input(
                label="Type your question here *(select one of the questions from the left)*:",
                value=st.session_state.interaction_box,
                key="input_box",
                label_visibility="collapsed",
                placeholder="Ask anything",
                disabled=True
            )

            # Submit button to send the question
            if st.button("⏎", key="Ask_button"):
                user_question = user_input.strip()
                if user_question and st.session_state.last_response == None:
                    st.session_state.user_question = user_question
                    if user_question:
                        
                        with chat_container:
                            st.markdown("""
                                <style>
                                    .float_message {
                                        display: none;
                                    }
                                </style>
                            """, unsafe_allow_html=True)
                        
                        # Start with the div styling for user message
                        base_message = """
                        <div style="display: flex; gap: 10px; padding: 0 0 10px 40px;">
                            <div style="
                                background-color: #f4f4f4; 
                                padding: 10px; 
                                border-radius: 10px; 
                                color: black; 
                                width: fit-content; 
                                font-size: 16px;
                                margin-bottom: 5px;
                                margin-left: auto;
                                margin-right: 0;">
                        """
                        
                        # Perform typing effect with the styled div
                        displayed_text = base_message
                        for char in user_question:
                            displayed_text += char
                            message_container.markdown(
                                displayed_text + """
                                </div>
                                <img src="data:data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB8AAAAfCAYAAAAfrhY5AAAACXBIWXMAAAsSAAALEgHS3X78AAACHUlEQVRIicWXrZLiQBDHf3u1VYmDahNceIPjVOShYskbHAp9j3CPsBpzHBLF4lDH8gScxG1kzBRxQXEiIZWPCUwWqP1XITJfv55muqfn6XQ68Vn68mlk4LntBKXUEBhqujbATkQOpms9mbg9A46BHwZrvgIvIrK5Ca6U6gIzYGQAreoNGIvIe2u4UmpA6srOB8BnxUDQ5AXtgbsTmGz+X6XUWNdZ2/kdwVV9E5FdsUG389kDwADL7Azp4Zl7vpqsFIZh/jOUC/wsNpTcrpR6zwZd1HQ6JYqi/NtxHCaTiYkBMdA/54J850qpwAQchmEJDBBFkakHOkBw/ii6PaiPfYi08MEtKx4Oxlk15xThRgetSd1u9/qgVPlf2/pWcxwHy7JKbZZl4ThO26Xaw23bxvO8Upvnedi2/Xh402nf7/et4XmcK6U2wPdL0PV6XQMX1el0GI1GuO7FiA1FpA/lYmKngydJwmKxMIrjOI6Zz+e4rovv+/R6Pd2wPL8X3b7RjVytVm1SKJB6abvdNnUva3ARWQI1SpIkrcBX5sVFeLWG+wX8Ljb4vs/xeGwNr4Zjppdijae7z3fcmHAa9E9ESllUF2oBqXvuqZi0AC2pBs8KvuGdDRhXqxgtPDNglxnQ7pjXFZOWT0tdZ2OGywwYAH8+CH4lLRxqOz7L9NHQJ42EgMv13TmUZjc/GhoMGZJ6pHiHHkifSleBN8Hvqf8cwNn91va8iAAAAABJRU5ErkJggg=="
                                        width="30" height="30" style="margin: 6px 0;">
                                </div>""", unsafe_allow_html=True)
                            time.sleep(0.05)
                        
                        # Add the final user message to chat history
                        user_message = f"""
                        <div style="display: flex; gap: 10px; padding: 0 0 10px 40px;">
                            <div style="
                                display: flex;
                                align-items: center;
                                justify-content: flex-end;
                                background-color: #f4f4f4;
                                padding: 10px;
                                border-radius: 10px;
                                color: black;
                                width: fit-content;
                                max-width: 80%;
                                font-size: 16px;
                                margin-bottom: 5px;
                                margin-left: auto;
                                margin-right: 0;">
                                <span>{user_question}</span>
                            </div>
                            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB8AAAAfCAYAAAAfrhY5AAAACXBIWXMAAAsSAAALEgHS3X78AAACHUlEQVRIicWXrZLiQBDHf3u1VYmDahNceIPjVOShYskbHAp9j3CPsBpzHBLF4lDH8gScxG1kzBRxQXEiIZWPCUwWqP1XITJfv55muqfn6XQ68Vn68mlk4LntBKXUEBhqujbATkQOpms9mbg9A46BHwZrvgIvIrK5Ca6U6gIzYGQAreoNGIvIe2u4UmpA6srOB8BnxUDQ5AXtgbsTmGz+X6XUWNdZ2/kdwVV9E5FdsUG389kDwADL7Azp4Zl7vpqsFIZh/jOUC/wsNpTcrpR6zwZd1HQ6JYqi/NtxHCaTiYkBMdA/54J850qpwAQchmEJDBBFkakHOkBw/ii6PaiPfYi08MEtKx4Oxlk15xThRgetSd1u9/qgVPlf2/pWcxwHy7JKbZZl4ThO26Xaw23bxvO8Upvnedi2/Xh402nf7/et4XmcK6U2wPdL0PV6XQMX1el0GI1GuO7FiA1FpA/lYmKngydJwmKxMIrjOI6Zz+e4rovv+/R6Pd2wPL8X3b7RjVytVm1SKJB6abvdNnUva3ARWQI1SpIkrcBX5sVFeLWG+wX8Ljb4vs/xeGwNr4Zjppdijae7z3fcmHAa9E9ESllUF2oBqXvuqZi0AC2pBs8KvuGdDRhXqxgtPDNglxnQ7pjXFZOWT0tdZ2OGywwYAH8+CH4lLRxqOz7L9NHQJ42EgMv13TmUZjc/GhoMGZJ6pHiHHkifSleBN8Hvqf8cwNn91va8iAAAAABJRU5ErkJggg=="
                                width="30" height="30" style="margin: 6px 0;">
                        </div>"""
                        st.session_state.h_responses.append(user_message)
                        
                        if user_question in st.session_state.questions:
                            st.session_state.question_idx = st.session_state.original_questions.index(user_question)
                            st.session_state.questions.remove(user_question)

                        # Add "thinking" message to chat history
                        thinking_message = """
                        <div style="display: flex; gap: 10px;">
                            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB8AAAAfCAYAAAAfrhY5AAAACXBIWXMAAAsSAAALEgHS3X78AAAD9klEQVRIicWXT4jbRRTHP41bPKibCNZr08NchHZXRAZ62dSTB8GIXgoFUxBBLPZXEO2ckr04CAVTUOitya2gYFDvuzkOHkzNcRCTiwh62NWLxT/rYd4k85v97WYrBR+E32/mzW++b968930vpw4ODvi/ZO2kC5W2bWAzmZoBI+/M3n8FP7Xq5ALaB85WqPeBvnem98jBlbYd4K4Mh8AgUbeBDlAHfgCekfco94GBd6b/0OBK2xawQzhd2zuzm+kbwE3gfeAxWTdJlmwlRnS8M6luJfiubPCad2aU6dKrqHS90rYpa14F5sBmHh+V4ErbTeA7YOydaWXz/eRUQ6A4LuiUtgPgTWA7N/BQtIs7P5DhKJnvA9dlOAZ66VUobd8AbgHfeGeuJVsWhPgogBJ46eRK254sioFz2TtzT3QHBBcX3plB8s154GvK2fAAuOKd+SI7/aXU4FqyyQDoJicD+JmyTDLgMfB9AjyX5+PA50rbmRgXAVOeCG5X2hZi2T7QIrhpiyNEafsp8G4y9SvwkndmKvqZGHRWjItGzdJ9anLHPRm3qlIikTNK2z8zYIDTwAtx4J1pAheA32UqeuZSCZzgijpwewUwwHMsg/Qz4Gngtnx/V2k7FX7AOzP1zqzLur/lm/eUth/GzdYIboblvaySqXfmQjIuJF7uABrYUdoOCdkwk8i/prT9DXgK+Aj4OJ48ykkKxDgDBkA8dlOG+4T4mUj2xDXrhCyoSaCWwJsVYG2JiYeRO8C2vHeVtik7XpHnxQgelZ1k0UBOcB2YSYE5qfwhTBbTamF8zHskbmrisjmwJZyNd2ZG8MQimPKNKuTJdCB7VMlf8SW6vSPPQRKte96ZAjjHknQ2lLYjKRoLEZ64d4xhqawB/yzAhfKuEk65kwJIxLYIOTonVKkflbY9pe0rStsJ8AnwxCpUISdK4AIyINReMoBGNFDI4waBPLoETt8geObyCuDzwDsy/KoELrIhBmwTAq5LEnBiSIOQrwC/EIpFi8N1IAeeCN4D78zrVeDRCz1CwA1ZstcugZu7YtgN78yzeYdTIRcJ/F4juPvFqMjBx4SgakrAdYDnZX5LDBkCzbQ3E8/ElM3J6rQ8YzczjYq8mRgJSCG/yF4t6WL20hSSzOgTrguSJjMhp5+Al1PQKHkz0SC4tg5cTWt3KpIJPQKNQvBMkRYmodYuoWAVVfsc6uGEaL5MTtKPmybl9y1Cas0FNG8wNwmFqg6cO4pwjmogWwT3Vf1RiHKfUP9LdyzAI/n2UNO4Elw2aRA6mjZlWv0WeBtYJ0T9iGWHskngCIChBOyRsvLv0jGG9cWweqauvIpHBp4Z0kqGeyfohhbyLyVMxSKyo1EIAAAAAElFTkSuQmCC"
                                width="30" height="30" style="margin: 6px 0;">
                            <div style="
                                background-color: #e9f2ff; 
                                padding: 10px; 
                                border-radius: 10px; 
                                color: grey; 
                                width: fit-content; 
                                font-size: 16px;
                                margin-bottom: 5px;">
                                <div class="loader"></div>
                            </div>
                        </div>
                        <style>
                            .loader {
                                width: 45px;
                                aspect-ratio: 2;
                                --_g: no-repeat radial-gradient(circle closest-side,#000 90%,#0000);
                                background: 
                                    var(--_g) 0%   50%,
                                    var(--_g) 50%  50%,
                                    var(--_g) 100% 50%;
                                background-size: calc(100%/3) 30%;
                                animation: l3 1s infinite linear;
                            }
                            @keyframes l3 {
                                20%{background-position:0%   0%, 50%  50%,100%  50%}
                                40%{background-position:0% 100%, 50%   0%,100%  50%}
                                60%{background-position:0%  50%, 50% 100%,100%   0%}
                                80%{background-position:0%  50%, 50%  50%,100% 100%}
                            }
                        </style>
                        """
                        st.session_state.h_responses.append(thinking_message)
                        st.session_state.ai_thinking = 1  # Set AI thinking state
                        st.session_state.interaction_box = ""  # Clear interaction box
                        st.rerun()  # Rerun to show "thinking" message first
                        
        st.markdown("""
            <span style="padding: 0 40px; color: #FF2B2B; font-weight: 600;">Your task: """ + str(len(st.session_state.confidence)) + """/13 questions remaining.</span>
        """, unsafe_allow_html=True)
