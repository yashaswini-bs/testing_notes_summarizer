# Exploratory Testing Notes Summarizer

**Objective:** Convert raw exploratory testing session notes into structured bug candidates, coverage summaries, and open questions.

# Phase 1: Requirements & Scope

## Problem Statement
Exploratory software testing yields high-value insights, but documenting these sessions is heavily manual. QA engineers lose approximately 30–40% of their testing time parsing through rough notes to extract reproducible steps, deduce root causes, and write structured bug tickets (e.g., for Jira). Furthermore, test leads lack immediate visibility into session coverage and testing gaps. 

## Target Personas
1. **QA Engineer / Tester:** Needs a zero-friction way to dump raw stream-of-consciousness observations and instantly receive defensible, structured defect candidates without losing data privacy.
2. **QA Lead / Engineering Manager:** Needs an immediate, high-level summary of what was tested, what wasn't, and what ambiguities exist to dynamically steer the next testing session.

## User Stories (Given-When-Then)

### 1. Defect Extraction
**Given** I am a QA engineer finishing an exploratory testing session,
**When** I paste my unstructured testing notes into the workspace,
**Then** the system should automatically extract and rank structured defect cards containing severity, heuristic tags (SFDPOT), reproduction steps, and root cause hypotheses.

### 2. Coverage & Gap Analysis
**Given** I am a QA Lead reviewing a tester's session,
**When** the AI analyzes the notes,
**Then** it should generate a coverage summary and explicitly list open ambiguities and suggested areas for the next focus, so I can optimize team resources.

### 3. Data Privacy
**Given** I am testing unreleased, confidential software,
**When** I review my analysis history,
**Then** the data must be retained only in my browser's session storage and destroyed upon closure, ensuring no proprietary data lingers on external servers.

### 4. Enterprise Handoff
**Given** I need to log the defects into our tracking system,
**When** I click export,
**Then** the system should instantly generate a formatted Markdown, PDF, or JSON file for seamless Jira/GitHub integration.

## Task Planning & Execution
The project execution was managed via a Kanban methodology, ensuring strict progression through Understanding, Design, Build, and Testing phases.

*(See Kanban Board evidence below)*

![Task Planning Board](./docs/kanban_board.png)
<!-- Ensure you create a quick Kanban board on GitHub Projects or Trello, screenshot it, and save it in a docs folder! -->