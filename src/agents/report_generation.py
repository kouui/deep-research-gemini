from .agent_base import AgentBase
from pydantic import BaseModel


class ReportGenerationAgent(AgentBase):

    def output_format(self):
        return None

    def system_prompt(self):
        message = {
            "role": "system",
            "content": (
                ""
            )
        }
        return message

    def send_message(self, query:str, all_learnings:list[str], language:str="English"):
        system = self.system_prompt()
        learnings = ''.join([f"<learning>\n{m}\n</learning>\n" for m in all_learnings])
        user = {
            "role": "user",
            "content": (
                "You are are an expert and insightful researcher.\n"
                "* Given the following prompt from the user, write a final report "
                "on the topic using the learnings from research.\n"
                "* Some learnings might be irrelevant to the query due to the lack of information on internet, "
                "feel free to ignore these irrelevant learnings\n"
                "* Make it as as detailed as possible, if possible aim for 3 or more pages, "
                "include ALL relavent learnings from research.\n"
                "* Format the report in markdown. Use headings, lists and tables only and where appropriate.\n"
                "* Do not contain the output in a markdown code block!!\n\n"
                f"the output language should be {language}\n\n"
                f"<prompt>{query}</prompt>\n\n"
                "Here are all the learnings from previous research:\n\n"
                "<learnings>\n"
                f"{learnings}"
                "</learnings>"
            )
        }
        response = self.request_llm([system, user])
        return response
    