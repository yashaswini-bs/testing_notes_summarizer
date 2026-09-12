import os
import json
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from groq import Groq

load_dotenv()

# --- Pydantic Schema ---
class BugCandidate(BaseModel):
    title: str = Field(description="Short, descriptive title of the defect")
    steps_to_reproduce: List[str] = Field(description="Steps to reproduce the observed bug")
    severity: str = Field(description="Severity rating: Critical, High, Medium, or Low")
    category: str = Field(description="Category: Functional, UI/UX, Performance, or Security")
    possible_root_cause: str = Field(description="Speculative AI hypothesis of why this occurred (labeled as hypothesis)")

class SummaryOutput(BaseModel):
    bugs: List[BugCandidate] = Field(default_factory=list, description="List of detected bug candidates")
    coverage_summary: str = Field(description="One concise paragraph summarizing the testing coverage")
    open_questions: List[str] = Field(default_factory=list, description="Questions or ambiguities raised by the notes")
    suggested_next_focus: List[str] = Field(default_factory=list, description="Recommended areas or flows to test next")

# --- Pipeline Function ---
def analyze_notes(notes: str) -> Optional[SummaryOutput]:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in your environment or .env file.")

    client = Groq(api_key=api_key)

    system_prompt = (
        "You are an expert QA lead analyzing raw exploratory testing session notes. "
        "Extract actionable testing deliverables according to the required schema. "
        "Guidelines:\n"
        "- Extract genuine bugs into bug candidates. For 'possible_root_cause', provide a clear speculative technical hypothesis.\n"
        "- If notes show no bugs, return an empty bug list rather than inventing defects.\n"
        "- Summarize what was tested in a single coherent paragraph for 'coverage_summary'.\n"
        "- Identify open questions, missing information, or unverified requirements.\n"
        "- Suggest concrete next areas to test based on coverage gaps.\n"
        "Output MUST be valid JSON conforming strictly to the requested schema."
    )

    schema_json = json.dumps(SummaryOutput.model_json_schema(), indent=2)

    prompt = (
        f"Analyze the following exploratory notes:\n\n"
        f"\"\"\"\n{notes}\n\"\"\"\n\n"
        f"Respond with pure JSON conforming strictly to this schema:\n{schema_json}"
    )

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    raw_json = response.choices[0].message.content
    return SummaryOutput.model_validate_json(raw_json)

if __name__ == "__main__":
    # Test run against one of our sample files
    sample_path = os.path.join("data", "samples", "food_delivery.txt")
    if os.path.exists(sample_path):
        with open(sample_path, "r", encoding="utf-8") as f:
            sample_notes = f.read()

        print("Analyzing food_delivery.txt with Groq...")
        result = analyze_notes(sample_notes)
        print("\n--- Structured Summary Result ---")
        print(json.dumps(result.model_dump(), indent=2))
    else:
        print(f"Sample file not found at {sample_path}")