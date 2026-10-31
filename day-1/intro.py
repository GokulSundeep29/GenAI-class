from openai import OpenAI
from dotenv import load_dotenv
 
load_dotenv() # reads OPENAI_API_KEY from .env
client = OpenAI()
 
response = client.responses.create(
    model="gpt-5",
    input="Explain AI in one line",
)
 
print(response.output_text)




