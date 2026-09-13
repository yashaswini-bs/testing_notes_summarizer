import os
import json
from typing import List, Optional, Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from groq import Groq

load_dotenv()

# --- Pydantic Schema ---

class BugCandidate(BaseModel):
    title: str = Field(description="Clear, ultra-concise defect title (under 10 words).")
    steps_to_reproduce: List[str] = Field(description="Explicit steps from the notes. Keep them very brief. If not provided, use 'Steps not specified'.")
    severity: Literal["Critical", "High", "Medium", "Low"] = Field(description="Severity: Critical, High, Medium, or Low.")
    heuristic_tag: Literal["Structure", "Function", "Data", "Platform", "Operations", "Time", "Boundary/Validation", "Other"] = Field(description="The SFDPOT or Boundary testing heuristic.")
    possible_root_cause: str = Field(description="Brief technical hypothesis starting with 'Hypothesis: ' (max 2 sentences).")

class SummaryOutput(BaseModel):
    is_testing_notes: bool = Field(description="True if exploratory testing notes. False if unrelated text.")
    rejection_reason: Optional[str] = Field(default=None, description="Reason for rejection if is_testing_notes is False.")
    bugs: List[BugCandidate] = Field(default_factory=list, description="List of detected bugs.")
    coverage_summary: str = Field(default="", description="One highly concise paragraph summarizing coverage.")
    open_questions: List[str] = Field(default_factory=list, description="Max 3 brief open questions.")
    suggested_next_focus: List[str] = Field(default_factory=list, description="Max 3 brief focus areas for next testing.")

# --- Core Pipeline Function ---

def analyze_notes(notes: str) -> SummaryOutput:
    stripped_notes = notes.strip()

    if len(stripped_notes) < 20:
        return SummaryOutput(
            is_testing_notes=False,
            rejection_reason="Input too short to represent actionable testing notes.",
            bugs=[], coverage_summary="", open_questions=[], suggested_next_focus=[]
        )

    if len(stripped_notes) > 15000:
        return SummaryOutput(
            is_testing_notes=False,
            rejection_reason="Input exceeds the max token limit. Please split into smaller chunks.",
            bugs=[], coverage_summary="", open_questions=[], suggested_next_focus=[]
        )

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in your environment or .env file.")

    client = Groq(api_key=api_key)

    system_prompt = (
        "You are a QA Lead. BE EXTREMELY CONCISE to conserve API tokens.\n"
        "1. CLASSIFICATION: Set is_testing_notes to false if text is casual/articles/unrelated.\n"
        "2. BUGS: Extract defects briefly. Do not invent steps. Tag with SFDPOT heuristics.\n"
        "3. LIMITS: Max 3 open questions, max 3 focus areas, very brief root causes.\n"
        "Output MUST be pure JSON matching the schema."
    )

    schema_json = json.dumps(SummaryOutput.model_json_schema(), indent=2)

    prompt = (
        f"Analyze these session notes concisely:\n\n"
        f"\"\"\"\n{stripped_notes}\n\"\"\"\n\n"
        f"Respond in pure JSON:\n{schema_json}"
    )

    try:
        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=900,
        )
        
        raw_json = response.choices[0].message.content
        return SummaryOutput.model_validate_json(raw_json)
        
    except (ValidationError, json.JSONDecodeError) as e:
        return SummaryOutput(
            is_testing_notes=True,
            rejection_reason="Warning: AI output was truncated due to API free-tier token limits.",
            bugs=[],
            coverage_summary="The notes were partially processed, but the AI ran out of tokens to complete the summary.",
            open_questions=[],
            suggested_next_focus=[]
        )

if __name__ == "__main__":
    sample_path = os.path.join("data", "samples", "food_delivery.txt")
    if os.path.exists(sample_path):
        with open(sample_path, "r", encoding="utf-8") as f:
            test_content = f.read()

        print("=== TEST 1: Valid Session Notes ===")
        res = analyze_notes(test_content)
        print(json.dumps(res.model_dump(), indent=2))

    fake_notes = (
        "Yesterday we walked into the biology lab to study an insect bug sample. "
        "The supervisor observed structural defects on the wing under the microscope. "
        "We took 5 photos and then proceeded to eat lunch."
    )
    print("\n=== TEST 2: False-Positive Keyword Trap ===")
    trap_res = analyze_notes(fake_notes)
    print(json.dumps(trap_res.model_dump(), indent=2))