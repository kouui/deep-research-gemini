from .agent_base import AgentBase
from pydantic import BaseModel
from datetime import datetime


class SearchQueryGenerationAgent(AgentBase):

    def output_format(self):
        class Queries(BaseModel):
            queries: list[str]
        return Queries

    def system_prompt(self):
        message = {
            "role": "system",
            "content": (
                f"You are an expert researcher. Today is {datetime.now().strftime('%Y-%m-%d')}. Follow these instructions when responding:\n"
                "- You may be asked to research subjects that is after your knowledge cutoff, assume the user is right when presented with news.\n"
                "- The user is a highly experienced analyst, no need to simplify it, be as detailed as possible and make sure your response is correct.\n"
                "- Be highly organized.\n"
                "- Suggest solutions that I didn't think about.\n"
                "- Be proactive and anticipate my needs.\n"
                "- Treat me as an expert in all subject matter.\n"
                "- Mistakes erode my trust, so be accurate and thorough.\n"
                "- Provide detailed explanations, I'm comfortable with lots of detail.\n"
                "- Value good arguments over authorities, the source is irrelevant.\n"
                "- Consider new technologies and contrarian ideas, not just the conventional wisdom.\n"
                "- You may use high levels of speculation or prediction, just flag it for me.\n"
            )
        }
        return message

    def send_message(self, query:str, breadth:int, learnings:list[str], language:str):
        system = self.system_prompt()
        learned = "" if not learnings else ( 
            f"Here are some learnings from previous research, "
            "use them to generate more specific queries by "
            "targeting the topics in the query that not yet covered by previous learnings:\n"
            f"{''.join([f'* {text}\n' for text in learnings])}"
        )
        user = {
            "role": "user",
            "content": (
                "Given the following prompt from the user, generate a list of SERP queries to research the topic.\n"
                "Reduce the number of words in each query to its keywords only.\n"
                f"search query should be generated in language : {' and '.join([v.strip() for v in language.split(',')])}\n"
                f"Return a maximum of {breadth} queries, but feel free to return less "
                "if the original prompt is clear. Make sure each query is unique and not similar to each other:\n"
                f"<prompt>{query}</prompt>\n\n"
                f"{learned}"
            )
        }
        response = self.request_llm([system, user])
        return response
    