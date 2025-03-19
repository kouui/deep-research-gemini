from .agent_base import AgentBase
from pydantic import BaseModel


class TitleGenerationAgent(AgentBase):

    def output_format(self):
        class Summary(BaseModel):
            title: str
            description: str
        return Summary

    def system_prompt(self):
        message = {
            "role": "system",
            "content": (
                ""
            )
        }
        return message

    def send_message(self, query:str, language:str="English"):
        system = self.system_prompt()
        user = {
            "role": "user",
            "content": (
                "Create a suitable title for the research report which will be created from the user's query.\n"
                f"<query>{query}</query>\n"
                f"the output language should be in {language}"
            )
        }
        response = self.request_llm([system, user])
        return response
    