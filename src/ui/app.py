import streamlit as st

def init_session_state():
    if 'query' not in st.session_state:
        st.session_state.query = ''
    if 'depth' not in st.session_state:
        st.session_state.depth = 1
    if 'breadth' not in st.session_state:
        st.session_state.breadth = 1
    if 'language' not in st.session_state:
        st.session_state.language = 'English'
    if 'acknowledge' not in st.session_state:
        st.session_state.acknowledge = False

def render_form():
    st.title('Deep Research with Gemini')
    
    # Research query input
    st.text_area(
        'Research Query',
        key='query',
        height=100,
        placeholder='Enter your research query here...'
    )
    
    # Research depth, breadth and language controls
    st.number_input(
        'Research Depth',
        min_value=1,
        max_value=2,
        key='depth',
        help='Controls how deep the research goes'
    )
    
    st.number_input(
        'Research Breadth',
        min_value=1,
        max_value=3,
        key='breadth',
        help='Controls how broad the research is'
    )
    
    st.selectbox(
        'Language',
        options=['English', 'Chinese', 'Japanese'],
        key='language',
        help='Select the language for research output'
    )
    
    # Acknowledgement checkbox
    st.checkbox(
        'I acknowledge that this research may take a while depending on the depth and breadth settings',
        key='acknowledge'
    )
    
    # Start button
    start_disabled = not (st.session_state.query and st.session_state.acknowledge)
    if st.button('Start Research', disabled=start_disabled):
        return True
    return False

def main():
    init_session_state()
    if render_form():
        st.write('Starting research...')
        # TODO: Implement research process

if __name__ == '__main__':
    main()