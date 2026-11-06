"""Class 2 - Stretch goal: keep the history under a token limit.

Run:    python chat_trimmed.py
Test:   tell it your name, chat for a few turns, then ask your name again.
        With a low limit, the oldest messages get dropped and it forgets.
"""
from openai import OpenAI
from dotenv import load_dotenv
from tokenizer_setup import get_encoding

load_dotenv()
client = OpenAI()
enc = get_encoding()

MODEL = "gpt-4.1-mini"
MAX_HISTORY_TOKENS = 200   # low on purpose, so you can see trimming happen

history = [
    {"role": "system", "content": "You are a friendly tutor. Keep answers short."}
]


def count(msgs):
    return sum(len(enc.encode(m["content"])) for m in msgs)


while True:
    user = input("\nYou: ")
    if user.strip().lower() in ("quit", "exit"):
        break
    history.append({"role": "user", "content": user})

    # Drop the oldest messages, but always keep history[0] (the system prompt)
    while count(history) > MAX_HISTORY_TOKENS and len(history) > 2:
        dropped = history.pop(1)
        print(f"   [trimmed: {dropped['role']}: {dropped['content'][:40]}...]")

    print("AI: ", end="", flush=True)
    reply = ""
    stream = client.chat.completions.create(
        model=MODEL,
        messages=history,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            print(text, end="", flush=True)
            reply += text

    print()
    history.append({"role": "assistant", "content": reply})
    print(f"   [history: {count(history)} tokens, {len(history)} messages]")
