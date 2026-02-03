# LLM-Based Input Validator

This project demonstrates using a **Large Language Model (LLM)** as the sole validation engine for structured user input.

## 🚀 Key Properties

- **No Regex:** Traditional validation libraries and complex regular expressions are entirely removed.
- **Logic Delegation:** Validation logic is fully delegated to the LLM.
- **Standards-Based:** Uses high-level, standards-based prompting for evaluation.
- **Strict Output:** Ensures a strict JSON output schema for easy parsing.
- **Deterministic:** Configured for deterministic model behavior to ensure consistency.
- **Automated Evals:** Includes automated evaluations via **Promptfoo**.

---

## 🛠️ Setup

### 1. Environment Preparation
Create and activate a virtual environment (recommended):

# Create the environment
python -m venv validate_env

# Activate (macOS / Linux)
source validate_env/bin/activate

# Activate (Windows)
validate_env\Scripts\activate

### 2. Install Dependencies
pip install -r requirements.txt
### 3. Model Configuration
Install and run Ollama, then pull the required model:
ollama pull mistral
Note: Ensure Ollama is running in the background before execution.

### 🏃 Execution
Run Validator
To validate a local JSON file:

python validate_user.py user.json
Run Automated Evals
To run the evaluation suite:

promptfoo eval -c promptfoo.config.yaml

### 📝 Project Notes
Logic Isolation: The Python code only handles input/output orchestration; the LLM performs all validation logic.

Field Handling: Missing fields are ignored rather than filled with "hallucinated" data.

Data Integrity: No data is inferred or fabricated during the process.

Output Reliability: The output is guaranteed to be valid JSON.