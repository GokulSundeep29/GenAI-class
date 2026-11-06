# Day 2 — Tokens, Temperature & Chat Memory

## Setup

Make sure you have a `.env` file in this folder (or the parent folder) with your OpenAI API key:

```
OPENAI_API_KEY=your-api-key-here
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 1. Tokens — How the Model Sees Text

```bash
python tokens.py
```

This script shows how the tokenizer splits text into tokens — the actual units the model reads and charges you for.

**What to observe:**
- English words are often 1 token; longer or unusual words split into multiple tokens
- Non-English scripts (Hindi, Tamil) use more tokens per word than English
- The script also runs a cost estimate to show how token counts translate to real money

**Key idea:** You are billed per token, not per word or character. Understanding tokens helps you write prompts that are cheaper and more efficient.

---

## 2. Temperature — Controlling Randomness

```bash
python temperature.py
```

Sends the same prompt three times at two different temperatures and prints all six responses side by side.

**What to observe:**
- `temperature=0` → near-identical answers every time (deterministic)
- `temperature=1.2` → different, more creative answers each time

**Key idea:** Temperature controls how "random" the model is. Use low values when you need consistent, factual output; use higher values when you want variety or creativity.

---

## 3. Chat — Memory & the Token Meter

### chat.py — Full history (tokens grow every turn)

```bash
python chat.py
```

A chatbot that keeps the entire conversation in memory and sends it all to the API on every turn.

**What to observe:**
- The token meter prints after each reply: `[in: X | out: Y | this turn: Z | total: T]`
- Input tokens grow with every turn — because the full history is resent each time
- Output tokens vary based on the length of the model's reply

**Key idea:** The model has no memory of its own. Your app is responsible for passing the conversation history back on every call. This is why input tokens keep growing.

---

### chat_trimmed.py — Trimmed history (tokens stay bounded)

```bash
python chat_trimmed.py
```

Same chatbot, but drops the oldest messages once the history exceeds `MAX_HISTORY_TOKENS`.

**What to observe:**
- History token count stays roughly flat after a few turns
- When trimming happens, it prints which message was dropped
- Tell the bot your name, chat for several turns, then ask it your name — with a low limit it will forget

**Key idea:** In production apps you need to manage context size. Common strategies are trimming old messages (this script), summarising old turns, or using a vector store for long-term memory.
