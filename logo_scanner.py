from groq import Groq
from dotenv import load_dotenv
import base64
import os

import json

class LogoScannerAgent :
    def __init__(self):
        load_dotenv()
        self.client = Groq(api_key=os.environ["GROQ_KEY"])



    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')


    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()


    def ask_logo_scanner_agent(self, image_path):
        image_object = LogoScannerAgent.encode_image(image_path)

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": LogoScannerAgent.read_file(file_path="./logo_scanner_agent_prompt_system.txt")
                },

                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_object}",
                            },
                        },
                    ],
                }
            ],

            model="qwen/qwen3.8-27b",
            response_format={"type": "json_object"},
        )

        return json.loads(chat_completion.choices[0].message.content)



if __name__ == "__main__":
    logo_1_path = "./carrefour.png"
    logo_scanner_agent_object = LogoScannerAgent()
    agent_response_1 = logo_scanner_agent_object.ask_logo_scanner_agent(image_path=logo_1_path)
    print(agent_response_1)
    print("-"*20)

    logo_2_path = "./carrefour_sans_text.png"
    agent_response_2 = logo_scanner_agent_object.ask_logo_scanner_agent(image_path=logo_2_path)
    print(agent_response_2)