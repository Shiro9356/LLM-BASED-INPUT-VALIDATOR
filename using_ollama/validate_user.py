import json
import sys
import time
from typing import List

from langchain_ollama import OllamaLLM
from pydantic import BaseModel, ValidationError


class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str]
    warnings: List[str]


SYSTEM_PROMPT = open("prompts/validate.txt", encoding="utf-8").read()

USER_PROMPT = """
Validate the following user profile object.

User input:
{input_json}
"""


def validate_with_llm(data: dict, llm: OllamaLLM) -> ValidationResult:
    prompt = USER_PROMPT.format(input_json=json.dumps(data))
    full_prompt = SYSTEM_PROMPT + "\n" + prompt

    for _ in range(3):
        response = llm.invoke(full_prompt)
        try:
            parsed = json.loads(response)
            return ValidationResult(**parsed)
        except (json.JSONDecodeError, ValidationError):
            time.sleep(0.5)

    raise RuntimeError("LLM failed to return valid structured output")


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_user.py <input.json>")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8-sig") as f:
        input_data = json.load(f)

    llm = OllamaLLM(model="mistral", temperature=0)
    result = validate_with_llm(input_data, llm)

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()
