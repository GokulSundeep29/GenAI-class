# Day 1 — Getting Started with OpenAI

## How to Get an OpenAI API Key

1. **Create an account** — Go to [platform.openai.com](https://platform.openai.com) and sign up (or log in if you already have one).

2. **Navigate to API Keys** — Click your profile icon in the top-right corner and select **"API keys"**, or go directly to [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

3. **Create a new key** — Click **"Create new secret key"**, give it a name, and click **"Create secret key"**.

4. **Copy the key immediately** — OpenAI shows the key only once. Copy it now and store it somewhere safe.

5. **Add billing** — Free-tier credits may be limited or expired. Add a payment method at [platform.openai.com/settings/billing](https://platform.openai.com/settings/billing) to ensure your key works.

## Setting Up Your Environment

Create a `.env` file in this folder (it is git-ignored and will not be committed):

```
OPENAI_API_KEY=sk-...your-key-here...
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Script

```bash
python intro.py
```

## Security Tips

- **Never commit your API key** to git. The `.gitignore` in this repo already excludes `.env`.
- Rotate your key immediately at [platform.openai.com/api-keys](https://platform.openai.com/api-keys) if it is ever accidentally exposed.
- Set usage limits at [platform.openai.com/settings/limits](https://platform.openai.com/settings/limits) to avoid unexpected charges.
