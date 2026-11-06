"""Class 2 - Temperature: same prompt, different temperatures.

Run:    python temperature.py
Predict first: which temperature gives 3 identical answers?
"""
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()          # reads OPENAI_API_KEY from .env
client = OpenAI()

prompt = "Suggest one name for a coffee shop. Reply with the name only."

# gpt-4.1-mini supports temperature; some reasoning models (e.g. GPT-5) may not
for temp in [0, 1.2]:
    print(f"\n--- temperature = {temp} ---")
    for _ in range(3):
        r = client.responses.create(
            model="gpt-5.4-mini",
            input=prompt,
            temperature=temp,
        )
        print(r.output_text)

# Bonus: try temperature=2.0 and see what happens
