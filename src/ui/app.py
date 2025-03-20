import streamlit as st    

def init_session_state():
    if 'query' not in st.session_state:
        st.session_state.query = ''
    if 'depth' not in st.session_state:
        st.session_state.depth = 1
    if 'breadth' not in st.session_state:
        st.session_state.breadth = 1
    if 'language' not in st.session_state:
        st.session_state.language = 'Chinese'
    if 'search_language' not in st.session_state:
        st.session_state.search_language = ['Chinese']
    if 'acknowledge' not in st.session_state:
        st.session_state.acknowledge = False
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'qa_completed' not in st.session_state:
        st.session_state.qa_completed = False

def reset_session_state():
    # st.session_state.query = ''
    # st.session_state.depth = 1
    # st.session_state.breadth = 1
    # st.session_state.language = 'Chinese'
    # st.session_state.search_language = ['Chinese']
    # st.session_state.acknowledge = False
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.current_question = 0
    st.session_state.qa_completed = False

def on_query_change():
    st.session_state.query = st.session_state.query_input

def on_depth_change():
    st.session_state.depth = st.session_state.depth_input

def on_breadth_change():
    st.session_state.breadth = st.session_state.breadth_input

def on_language_change():
    st.session_state.language = st.session_state.language_input

def on_search_language_change():
    st.session_state.search_language = st.session_state.search_language_input

def on_acknowledge_change():
    st.session_state.acknowledge = st.session_state.acknowledge_input

def render_form():
    st.title('Deep Research with Gemini')
    
    if not st.session_state.questions and not st.session_state.qa_completed:
        # Research query input
        st.text_area(
            'Research Query',
            key='query_input',
            on_change=on_query_change,
            height=100,
            placeholder='Enter your research query here...'
        )
        
        # Research depth, breadth and language controls
        st.number_input(
            'Research Depth',
            min_value=1,
            max_value=2,
            key='depth_input',
            on_change=on_depth_change,
            help='Controls how deep the research goes'
        )
        
        st.number_input(
            'Research Breadth',
            min_value=1,
            max_value=3,
            key='breadth_input',
            on_change=on_breadth_change,
            help='Controls how broad the research is'
        )
        
        lans = ['English', 'Chinese', 'Japanese']
        st.selectbox(
            'Output Language',
            options=lans,
            key='language_input',
            index=lans.index(st.session_state.language),
            on_change=on_language_change,
            help='Select the language for research output'
        )
        
        st.multiselect(
            'Search Language',
            options=lans,
            key='search_language_input',
            default=st.session_state.search_language,
            on_change=on_search_language_change,
            help='Select one or more languages for search queries'
        )
        
        # Acknowledgement checkbox
        st.checkbox(
            'I acknowledge that this research may take a while depending on the depth and breadth settings',
            key='acknowledge_input',
            on_change=on_acknowledge_change
        )
        
        # Start button
        start_disabled = not (st.session_state.query and st.session_state.acknowledge and st.session_state.search_language)
        if st.button('Generate Questions', disabled=start_disabled):
            from ..agents.question_generation import QuestionGenerationAgent
            import json
            
            with st.spinner('Generating questions...'):
                res = QuestionGenerationAgent().send_message(st.session_state.query, language=st.session_state.language)
                res = json.loads(res)
                st.session_state.questions = res['questions']
                st.rerun()
    
    elif st.session_state.questions and not st.session_state.qa_completed:
        st.write('Please answer the following questions to help us better understand your research needs:')
        current_q = st.session_state.current_question
        
        if current_q < len(st.session_state.questions):
            st.write(f'Question {current_q + 1}/{len(st.session_state.questions)}:')
            st.write(st.session_state.questions[current_q])
            answer = st.text_area('Your Answer:', key=f'answer_{current_q}')
            
            if st.button('Next' if current_q < len(st.session_state.questions) - 1 else 'Complete'):
                if answer:  # Only proceed if an answer is provided
                    st.session_state.answers.append(answer)
                    st.session_state.current_question += 1
                    if current_q == len(st.session_state.questions) - 1:
                        st.session_state.qa_completed = True
                    st.rerun()
                else:
                    st.error('Please provide an answer before proceeding.')
    
    elif st.session_state.qa_completed:
        st.success('Questions completed! Starting research...')
        return True
    
    return False