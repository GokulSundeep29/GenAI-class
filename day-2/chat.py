"""Class 2 - A chatbot with memory and a live token meter.

Run:    python chat.py      (type 'quit' to stop)
Watch the tokens per turn: why do they keep growing?
"""
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

MODEL = "gpt-4.1-mini"

# The "memory" lives here, in your app, not in the model
history = [
    {"role": "system", "content": "You are a friendly tutor. Keep answers short."}
]
total_tokens = 0

while True:
    user = input("\nYou: ")
    if user.strip().lower() in ("quit", "exit"):
        break

    history.append({"role": "user", "content": user})

    # Stream the response so text appears immediately instead of waiting
    print("AI: ", end="", flush=True)
    reply = ""
    usage = None
    stream = client.chat.completions.create(
        model=MODEL,
        messages=history,
        stream=True,
        stream_options={"include_usage": True},
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            print(text, end="", flush=True)
            reply += text
        if chunk.usage:
            usage = chunk.usage

    print()
    history.append({"role": "assistant", "content": reply})

    used = usage.prompt_tokens + usage.completion_tokens
    total_tokens += used
    print(f"   [in: {usage.prompt_tokens} | out: {usage.completion_tokens} "
          f"| this turn: {used} | total: {total_tokens}]")

print(f"\nSession total: {total_tokens} tokens")
