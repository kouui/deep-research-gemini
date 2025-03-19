from .agent_base import AgentBase
from pydantic import BaseModel
from datetime import datetime


class QuestionGenerationAgent(AgentBase):

    def output_format(self):
        class Questions(BaseModel):
            questions: list[str]
        return Questions

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

    def send_message(self, query:str, language:str="English"):
        system = self.system_prompt()
        user = {
            "role": "user",
            "content": (
                "Given the following query from the user, ask some follow up questions to clarify the research direction. "
                f"Return a maximum of 3 questions in {language}, but feel free to return less if the original query is clear: "
                f"<query>{query}</query>"
            )
        }
        response = self.request_llm([system, user])
        return response
    