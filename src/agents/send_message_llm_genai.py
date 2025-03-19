
import google.generativeai as generativeai
import google.genai as genai
from typing import Callable
import time
import json
from pathlib import Path

""" how to use proxy with google gemini api
    reference : https://github.com/google-gemini/generative-ai-python/issues/188#issuecomment-2567882368
    10809 is the default proxy port of v2rayN, clash verge should be different 
"""
# import os
# os.environ["GRPC_PROXY"] = "http://127.0.0.1:10809"  # apply to google.generativeai
# os.environ["ALL_PROXY"] = "http://127.0.0.1:10809"   # apply to google.genai


class KeySwicher:

    def __init__(self):
        keyfile = Path(__file__).parent.parent.parent / "keys.json"
        with open(keyfile, 'r') as f:
            keys = json.load(f)
        self.keys = [v for k, v in keys.items()]  # if k != "Gemini API"]
        self.index = 0
        print(f"number of loaded google ai studio api key : {len(self.keys)}")

    def __len__(self):
        return len(self.keys)

    def __call__(self):
        self.index += 1
        if self.index >= len(self.keys):
            self.index = 0

        # print(f"using api key No.{self.index}")
        return self.keys[self.index]


KEY_SWITCHER = KeySwicher()


def wait_after(func: Callable):
    """
    A decorator that waits few seconds after the function call.
    """
    dt_min = 0 # 5  # 5 second --> maximum RPM is 60/5=12
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        dt = end - start
        print(f"time elapsed in calling {func.__name__} : {dt:.1f} seconds")
        if dt < dt_min:
            dt_to_wait = dt_min - dt
            print(f"waiting {dt_to_wait:.1f} seconds to limit request rate")
            time.sleep(dt_to_wait)
        return result 
    return wrapper


# Function to send a message to the Gemini model and return its response
@wait_after
def send_message(
    message_log: list[dict[str,str]],
    config=None,
    use_genai:bool=True, 
    filepath:str= '', 
    imagepath:str='', 
    model:str="gemini-2.0-flash"):

    api_key = KEY_SWITCHER()
    
    default_model = 'gemini-2.0-flash'
    if model not in (default_model,):
        model = default_model

    if use_genai:
        """ api calling using genai """
        client = genai.Client(api_key=api_key)
    else:
        """ api calling using gerativeai """
        generativeai.configure(api_key=api_key)
        model = generativeai.GenerativeModel(model)
    try:
        """ api calling using gerativeai
        """
        if not use_genai:
            """ api calling using gerativeai
                
                !!! need discovery api key to upload file.
                    - upload a file, once finished, got the file url
                    - add the url and minetype into a FileDataDict
                    - add the FileDataDict as PartType into contents

                class FileServiceClient(glm.FileServiceClient):
                    def __init__(self, *args, **kwargs):
                        self._discovery_api = None
                        self._local = threading.local()
                        super().__init__(*args, **kwargs)

                    def _setup_discovery_api(self, metadata: dict | Sequence[tuple[str, str]] = ()):
                        api_key = self._client_options.api_key
                        if api_key is None:
                            raise ValueError(
                                "Invalid operation: Uploading to the File API requires an API key. Please provide a valid API key."
                            )

                        request = googleapiclient.http.HttpRequest(
                            http=httplib2.Http(),
                            postproc=lambda resp, content: (resp, content),
                            uri=f"{GENAI_API_DISCOVERY_URL}?version=v1beta&key={api_key}",
                            headers=dict(metadata),
                        )

                @File : generativeai.types.file_types.py

                class File:
                    def __init__(self, proto: protos.File | File | dict):
        
                class FileDataDict(TypedDict):
                    mime_type: str
                    file_uri: str

                FileDataType = Union[FileDataDict, protos.FileData, protos.File, File]

                @File : generativeai.types.content_types.py

                BlobType = Union[
                    protos.Blob, BlobDict, PIL.Image.Image, IPython.display.Image
                ]
                class PartDict(TypedDict):
                    text: str
                    inline_data: BlobType
                
                PartType = Union[
                    protos.Part,
                    PartDict,
                    BlobType,
                    str,
                    protos.FunctionCall,
                    protos.FunctionResponse,
                    file_types.FileDataType,
                ]

                StrictContentType = Union[protos.Content, ContentDict]
                ContentType = Union[protos.Content, ContentDict, Iterable[PartType], PartType]

                ContentsType = Union[ContentType, Iterable[StrictContentType], None]

                def generate_content(
                    self,
                    contents: content_types.ContentsType,
                    *,
                    generation_config: generation_types.GenerationConfigType | None = None,
                    safety_settings: safety_types.SafetySettingOptions | None = None,
                    stream: bool = False,
                    tools: content_types.FunctionLibraryType | None = None,
                    tool_config: content_types.ToolConfigType | None = None,
                    request_options: helper_types.RequestOptionsType | None = None,
                )
                
                GenerationConfigType = Union[protos.GenerationConfig, GenerationConfigDict, GenerationConfig]

                @dataclasses.dataclass
                class GenerationConfig:
                    candidate_count: int | None = None
                    stop_sequences: Iterable[str] | None = None
                    max_output_tokens: int | None = None
                    temperature: float | None = None
                    top_p: float | None = None
                    top_k: int | None = None
                    response_mime_type: str | None = None
                    response_schema: protos.Schema | Mapping[str, Any] | type | None = None
                    presence_penalty: float | None = None
                    frequency_penalty: float | None = None
            """
            contents = []
            for message in message_log:
                if message["role"] not in ["system", "user"]:
                    continue
                contents.append(
                    generativeai.types.ContentDict(
                        role="user", # message["role"],
                        parts=message["content"] + '\n'
                    )
                )
            response = model.generate_content(
                contents=contents,
                generation_config=config,
            )
        else:
            """ api calling using genai
                https://googleapis.github.io/python-genai/ 
            """
            contents = []
            prompt = ""
            if config is None:
                config = {}
            for message in message_log:
                if message["role"] == "system":
                    # prompt += "Human: " + message["content"] + "\n\n"
                    config["system_instruction"] = message["content"]
                elif message["role"] == "user":
                    # prompt += "Human: " + message["content"] + "\n\n"
                    prompt += message["content"]

            # if filepath:
            #     contents.append(contents.append({"mime_type": 'text/markdown', "data": filepath.read_bytes()}))        
            contents.append(prompt)  # Append the prompt
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=genai.types.GenerateContentConfigDict(**config),
            )
        return response.text if response and response.text else "No response received."
    except Exception as e:
        print(f"An error occurred while calling Gemini API: {e}")
        return "Error communicating with Gemini API."


def _test():

    """ json output """
    message_log = [
        {"role": "system", "content": (
            "你是一位优秀的厨师\n"
        )},
        {"role": "user", "content": (
            "请给出一些流行的菜谱，记得要表明每样食材的用量。"
        )}
    ]

    from pydantic import BaseModel

    class Recipe(BaseModel):
        菜谱名: str
        食材: list[str]

    config = {
        'response_mime_type': 'application/json',
        'response_schema': list[Recipe],
    }
    out = send_message(message_log, config=config)
    print(out)

    """ check system prompt """
    message_log = [
        {"role": "system", "content": (
            "please repeat whatever user said. do not provide any other content\n"
        )},
        {"role": "user", "content": (
            "请给出一些流行的菜谱，记得要表明每样食材的用量。"
        )}
    ]

    out = send_message(message_log)
    print(out)

    """ check file upload """
    message_log = [
        {"role": "system", "content": (
            "please repeat whatever user said and the content in the provided file. do not provide any other content\n"
        )},
        {"role": "user", "content": (
            "这是一个用于安装python依赖的脚本."
        )}
    ]

    out = send_message(message_log, )

    return 0


if __name__ == "__main__":
    _test()