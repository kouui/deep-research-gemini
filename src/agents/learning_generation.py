from .agent_base import AgentBase
from pydantic import BaseModel
from datetime import datetime


class LearningGenerationAgent(AgentBase):

    def output_format(self):
        class Learnings(BaseModel):
            learnings: list[str]
        return Learnings

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

    def send_message(self, search_query:str, markdowns:list[str], language:str="English"):
        system = self.system_prompt()
        contents = ''.join([f"<content>\n{m if len(m)<10_0000 else m[:10_0000]}\n</content>\n" for m in markdowns])
        user = {
            "role": "user",
            "content": (
                f"Given the following contents from a SERP search for the query <query>{search_query}</query>, "
                "generate a list of learnings from the contents. "
                "Return a maximum of 3 learnings, but feel free to return less if the contents are clear. "
                "Make sure each learning is unique and not similar to each other. "
                "The learnings should be concise and to the point, as detailed and infromation dense as possible. "
                "Make sure to include any entities like people, places, companies, products, things, etc in the learnings, "
                "as well as any exact metrics, numbers, or dates. The learnings will be used to research the topic further."
                "\n\n"
                f"the learnings should be generated in {language}"
                "\n\n"
                "<contents>\n"
                f"{contents}"
                "</contents>"
            )
        }
        response = self.request_llm([system, user])
        return response
    