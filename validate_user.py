import json
import os
import sys
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a strict validation engine.

Validate user-provided profile data using real-world standards.
Use only the provided input values.
Do not infer, fabricate, or assume missing data.
Apply validation only to fields that are present and not null.

Return ONLY valid JSON in the exact schema:

{
  "is_valid": boolean,
  "errors": string[],
  "warnings": string[]
}

Errors indicate invalid input.
Warnings indicate soft concerns that do not invalidate the input.
Report all applicable issues.
"""

USER_PROMPT = """
Validate the following user profile object.

High-level expectations:
- Required fields must be meaningfully present
- Emails must follow real-world email standards
- Phone numbers must follow international E.164 format
- Country codes must follow ISO-2 standards
- Ages must follow reasonable human constraints
- Warnings reflect best-practice or safety concerns

Only evaluate fields present in the input.

User input:
{input_json}
"""

EXPECTED_KEYS = {"is_valid", "errors", "warnings"}


def validate_with_llm(data):
    prompt = USER_PROMPT.format(input_json=json.dumps(data))

    for _ in range(3):
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )

        try:
            output = json.loads(response.choices[0].message.content)
            if set(output.keys()) != EXPECTED_KEYS:
                raise ValueError
            return output
        except Exception:
            time.sleep(0.5)

    raise RuntimeError("LLM failed to return valid structured output")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_user.py <input.json>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        input_data = json.load(f)

    result = validate_with_llm(input_data)
    print(json.dumps(result, indent=2))
