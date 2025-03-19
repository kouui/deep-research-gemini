from src.agents.question_generation import QuestionGenerationAgent
from src.agents.title_generation import TitleGenerationAgent
from src.agents.search_query_generation import SearchQueryGenerationAgent
from src.agents.learning_generation import LearningGenerationAgent
from src.agents.report_generation import ReportGenerationAgent
from src.tools.apify_tools import ApifyRagWebBrowser
from pathlib import Path
import json

def _test():
    query = "推荐和全知读者视角类似的完结漫画"
    depth = 1
    breadth = 2
    language = "Chinese"
    search_query_language = "Chinese,Japanese"
    # style = "informative"

    print(f"[query]\n{query}\n[depth]\n{depth}\n[breadth]\n{breadth}\n[language]\n{language}\n\n")

    qa = ""
#     qa = f"""
# Initial query: {query}

# Follow-up Questions and Answers:
# Question: 您对“类似”的具体要求是什么？例如，您更看重剧情设定、人物关系、叙事风格还是其他方面？
# Answer: 剧情设定，人物能力设定，叙事风格

# Question: 您偏好哪种漫画类型？例如，是偏好奇幻、冒险、战斗还是其他类型？
# Answer: 除开历史政治类型

# Question: 您对漫画的画风有什么偏好吗？例如，是偏好写实、唯美还是其他风格？
# Answer: 不要唯美
#     """
    """ step 1. test the question generation """
    if not qa:
        print("[question generation]\n")
        res = QuestionGenerationAgent().send_message(query, language=language)
        res = json.loads(res)
        qa = f"Initial query: {query}\n\nFollow-up Questions and Answers:\n"
        for q in res["questions"]:
            print(q)
            ans = input("answer: ")
            print()
            qa += f"Question: {q}\nAnswer: {ans}\n\n"
        print(qa)
    
    """ step 2. test the title generation """
    # print("[title generation]\n")
    # res = TitleGenerationAgent().send_message(qa, language=language)
    # res = json.loads(res)
    # title = res["title"]
    # description = res["description"]

    """ step 3. research """
    all_learnings = []
    all_urls = []
    # research_goal = "" if style=="informative" else (
    #     "First talk about the goal of the research that this query is meant to accomplish, "
    #     "then go deeper into how to advance the research once the results are found, "
    #     "mention additional research directions. "
    #     "Be as specific as possible, especially for additional research directions."
    # )
    fetcher = ApifyRagWebBrowser()
    for i in range(depth):
        """ step 4. generate nbreath search query """
        print("[search query generation]\n")
        res = SearchQueryGenerationAgent().send_message(qa, breadth, all_learnings, search_query_language)
        res = json.loads(res)
        for search_query in res["queries"]:
            print(f"{search_query=}")
            ret = fetcher.fetch_web_content(search_query)
            if not ret:
                continue
            print("[learning generation]\n")
            res = LearningGenerationAgent().send_message(search_query, [r["markdown"] for r in ret], language)
            res = json.loads(res)
            learnings = res["learnings"]
            urls = [r["searchResult"]["url"] for r in ret]
            all_learnings.extend( learnings )
            all_urls.extend( urls)
            print(f"{len(learnings)=}, {len(urls)=}")
    print("[report generation]\n")
    draft = ReportGenerationAgent().send_message(qa, all_learnings, language)
    with open(Path(__file__).parent / "draft.md", "w", encoding="utf-8") as f:
        f.write(draft)
            
    return 0


if __name__ == "__main__":
    _test()