"""Class 2 - Tokens: count how the model sees your text.

Setup:  pip install tiktoken
Run:    python tokens.py
"""
from tokenizer_setup import get_encoding

# o200k_base is the tokenizer used by OpenAI's recent models.
# The first run downloads its vocabulary (with a progress bar); after that it's instant.
enc = get_encoding()

texts = [
    "Hello, how are you?",
    "नमस्ते, आप कैसे हैं?",                 # Hindi
    "வணக்கம், எப்படி இருக்கிறீர்கள்?",       # Tamil
    "strawberry",
    # Try your own: your name, a long technical word, a sentence in your language
]

for text in texts:
    ids = enc.encode(text)
    pieces = [enc.decode([i]) for i in ids]
    print(f"{len(ids):>3} tokens | {text}")
    print(f"      pieces: {pieces}")
    print(f"      ids:    {ids}\n")

# --- Cost estimate -------------------------------------------------------
# Fill in the real prices from OpenAI's pricing page (USD per 1 million tokens).
# Output tokens (what the model writes) usually cost several times more than input.
PRICE_PER_MILLION_INPUT = 0.75    # look up your model's input price
PRICE_PER_MILLION_OUTPUT = 4.5   # look up your model's output price

# Measure these with chat.py: it prints "in" and "out" tokens every turn
input_tokens_per_call = 1200      # prompt + instructions + chat history
output_tokens_per_call = 300      # the model's reply
calls = 1000

total_input = input_tokens_per_call * calls
total_output = output_tokens_per_call * calls

input_cost = total_input / 1_000_000 * PRICE_PER_MILLION_INPUT
output_cost = total_output / 1_000_000 * PRICE_PER_MILLION_OUTPUT
total_cost = input_cost + output_cost

print(f"For {calls:,} calls:")
print(f"  Input:  {total_input:>10,} tokens  ->  ${input_cost:.4f}")
print(f"  Output: {total_output:>10,} tokens  ->  ${output_cost:.4f}")
print(f"  Total:                       ${total_cost:.4f}")
