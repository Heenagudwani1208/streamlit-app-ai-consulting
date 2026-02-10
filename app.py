import streamlit as st
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

# ---------------- SETUP ----------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Consulting AI Draft Generator", layout="wide")
st.title("🧠 Consulting AI Draft Generator")
st.caption("AI-assisted first drafts for consulting Product Managers")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Client Context")

industry = st.sidebar.selectbox(
    "Industry",
    ["Technology", "Fintech", "Healthcare", "Retail", "Other"]
)

client_type = st.sidebar.selectbox(
    "Client Type",
    ["Startup", "Mid-size Company", "Enterprise"]
)

language = st.sidebar.selectbox(
    "Output Language",
    ["English", "Hindi", "Spanish", "French"]
)

model = st.sidebar.selectbox(
    "Model",
    ["gpt-4o-mini", "gpt-4o"]
)

# ---------------- INPUT ----------------
raw_input = st.text_area(
    "Paste messy client inputs (notes, emails, chats)",
    height=220
)

generate = st.button("🚀 Generate First Draft")

# ---------------- NON-AI FALLBACK ----------------
def fallback_draft():
    return """
### Problem Statement
Client has shared initial context, but details are incomplete.

### Business Goals
- To be clarified with the client.

### Scope
In-Scope:
- Initial discovery and clarification

Out-of-Scope:
- Final solution definition

### Key Requirements
- More information required

### Assumptions
- Inputs are preliminary

### Open Questions
- What are success metrics?
- What is the timeline?

### Risks & Dependencies
- Risk of misalignment due to missing data
"""

# ---------------- AI GENERATION ----------------
def generate_draft(text):
    user_prompt = USER_PROMPT_TEMPLATE.format(
        industry=industry,
        client_type=client_type,
        language=language,
        raw_input=text
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

# ---------------- OUTPUT ----------------
if generate:
    if not raw_input.strip():
        st.warning("Please enter client input.")
    else:
        with st.spinner("Generating first draft..."):
            try:
                output = generate_draft(raw_input)
                st.session_state["draft"] = output
                st.success("Draft generated")
            except Exception:
                st.session_state["draft"] = fallback_draft()
                st.warning("AI unavailable. Showing fallback draft.")

# ---------------- HUMAN-IN-THE-LOOP ----------------
if "draft" in st.session_state:
    st.markdown("## 📄 Generated Draft (Editable)")
    edited_draft = st.text_area(
        "Review and edit the draft below:",
        value=st.session_state["draft"],
        height=350
    )

    refine = st.button("🔁 Refine with AI")

    if refine:
        with st.spinner("Refining draft..."):
            refined = generate_draft(edited_draft)
            st.session_state["draft"] = refined
            st.success("Draft refined")

# ---------------- FEEDBACK LOOP ----------------
st.markdown("## 👍 Was this draft useful?")

feedback = st.radio(
    "Your feedback helps improve the system",
    ["Very useful", "Somewhat useful", "Not useful"]
)

if st.button("Submit Feedback"):
    record = {
        "industry": industry,
        "client_type": client_type,
        "language": language,
        "feedback": feedback
    }

    if not os.path.exists("feedback.json"):
        with open("feedback.json", "w") as f:
            json.dump([record], f, indent=2)
    else:
        with open("feedback.json", "r+") as f:
            data = json.load(f)
            data.append(record)
            f.seek(0)
            json.dump(data, f, indent=2)

    st.success("Feedback recorded. Thank you!")
