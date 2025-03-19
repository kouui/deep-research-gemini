from .send_message_llm_genai import send_message
from pydantic import BaseModel

class AgentBase:
    def __init__(self):
        self.name = self.__class__.__name__
    
    def output_format(self):

        return None

    def request_llm(self, message_log:list[dict[str,str]]):

        config = None
        outfmt:None | BaseModel | list[str] | list[BaseModel] = self.output_format()
        if outfmt is not None:
            config = {
                'response_mime_type': 'application/json',
                'response_schema': outfmt,
                "temperature": 0.4,
                "max_output_tokens": 128000,
            }
        out: str = send_message(message_log, config=config)
        return out

    def system_prompt(self):
        
        return {"role": "system", "content": ""}



    