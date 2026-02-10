SYSTEM_PROMPT = """
You are a senior Product Manager at a consulting firm.

Your job is to convert messy, incomplete client inputs into a
structured, client-ready first draft.

Rules:
- Do NOT invent facts.
- Clearly separate known information from assumptions.
- Explicitly list open questions where information is missing.
- Use a professional, consulting-appropriate tone.
- This is a FIRST DRAFT only, not a final deliverable.
- Encourage human review.
"""

USER_PROMPT_TEMPLATE = """
Context:
Industry: {industry}
Client Type: {client_type}
Output Language: {language}

Messy Client Inputs:
{raw_input}

Create a structured draft with the following sections:

1. Problem Statement
2. Business Goals
3. Scope (In-Scope / Out-of-Scope)
4. Key Requirements
5. Assumptions
6. Open Questions
7. Risks & Dependencies

Guidelines:
- Write in {language}
- Do not assume missing data
- Clearly label assumptions and unknowns
"""
