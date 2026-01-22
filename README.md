# LLM-Based Input Validator

This project demonstrates using an LLM as the sole validation engine for structured user input.

## Key Properties
- No regex or validation libraries
- High-level, standards-based prompting
- Strict JSON output schema
- Deterministic behavior
- Automated evals via Promptfoo

## Setup

pip install -r requirements.txt  
cp .env.example .env

Add your OpenAI API key.

## Run Validator

python validate_user.py user.json

## Run Evals

npx promptfoo eval
