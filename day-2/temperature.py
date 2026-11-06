"""Class 2 - Temperature: same prompt, different temperatures.

Run:    python temperature.py
Predict first: which temperature gives 3 identical answers?
"""
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()          # reads OPENAI_API_KEY from .env
client = OpenAI()

prompt = "Suggest one name for a coffee shop. Reply with the name only."

# gpt-4.1-mini supports temperature; some reasoning models (e.g. o3) may not
for temp in [0, 1.2]:
    print(f"\n--- temperature = {temp} ---")
    for _ in range(3):
        r = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
        )
        print(r.choices[0].message.content)

# Bonus: try temperature=2.0 and see what happens
