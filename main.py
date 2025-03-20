
async def run_research(query: str, depth: int, breadth: int, language: str, search_language: list[str]) -> str:
    import json
    import asyncio
    # from src.agents.title_generation import TitleGenerationAgent
    from src.agents.search_query_generation import SearchQueryGenerationAgent
    from src.agents.learning_generation import LearningGenerationAgent
    from src.agents.report_generation import ReportGenerationAgent
    from src.tools.apify_tools import ApifyRagWebBrowser

    print(query)
    print(f"{depth=}, {breadth=}, {language=}, {search_language=}")
    # Initialize research state
    all_learnings = []
    all_urls = []
    fetcher = ApifyRagWebBrowser()
    # Conduct research at specified depth
    for _ in range(depth):
        """ enerate nbreath search query """
        print("[search query generation]\n")
        res = SearchQueryGenerationAgent().send_message(query, breadth, all_learnings, search_language)
        res = json.loads(res)
        for search_query in res["queries"]:
            print(f"{search_query=}")
            """ fetch web content and url """
            ret = fetcher.fetch_web_content(search_query)
            if not ret:
                continue
            print("[learning generation]\n")
            res = LearningGenerationAgent().send_message(search_query, [r["markdown"] for r in ret], language)
            res = json.loads(res)
            learnings = res["learnings"]
            urls = [r["searchResult"]["url"] for r in ret]
            all_learnings.extend( learnings )
            all_urls.extend(urls)
            print(f"{len(learnings)=}, {len(urls)=}")
    print("[report generation]\n")
    draft = ReportGenerationAgent().send_message(query, all_learnings, language) + (
        f"# {'参考' if language=='Chinese' else '引用' if language=='Japanese' else 'Reference'}\n"
        f"{'\n'.join(['* ' + url for url in all_urls])}"
        "\n"
    )
    
    return draft


def main():
    from src.ui.app import init_session_state, render_form, st, reset_session_state
    init_session_state()
    if render_form():
        st.write('Starting research...')

        import asyncio
        from main import run_research
        
        try:
            query = ""
            for q, a in zip(st.session_state.questions, st.session_state.answers):
                query += f"Question: {q}\nAnswer: {a}\n\n"
            # Show progress message
            with st.spinner('Conducting research... This may take a few minutes depending on depth and breadth settings.'):
                # Run research with user inputs
                report = asyncio.run(run_research(
                    query,
                    st.session_state.depth,
                    st.session_state.breadth,
                    st.session_state.language,
                    st.session_state.search_language
                ))
                
                # Display research results
                st.success('Research completed!')
                st.markdown(report)
                reset_session_state()
        except Exception as e:
            st.error(f'An error occurred during research: {str(e)}')
            st.info('Please try again with different parameters or check your internet connection.')


if __name__ == '__main__':
    main()