import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page setup
st.set_page_config(
    page_title="Consulting AI Draft Generator",
    layout="wide"
)

st.title("🧠 Consulting AI Draft Generator")
st.caption("Turn messy client inputs into a structured first draft using Generative AI")

# API key check
if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY not found in .env file")
    st.stop()

# Sidebar
st.sidebar.header("Client Context")

industry = st.sidebar.selectbox(
    "Industry",
    ["Technology", "Fintech", "Healthcare", "Retail", "Other"]
)

client_type = st.sidebar.selectbox(
    "Client Type",
    ["Startup", "Mid-size Company", "Enterprise"]
)

model = st.sidebar.selectbox(
    "Model",
    ["gpt-4o-mini", "gpt-4o"]
)

# Input
raw_input = st.text_area(
    "Paste messy client inputs (emails, call notes, chats)",
    height=260,
    placeholder="Client is a fintech startup. Onboarding drop-offs are high after KYC..."
)

generate = st.button("🚀 Generate First Draft")


def generate_draft(raw_input, industry, client_type, model):
    user_prompt = USER_PROMPT_TEMPLATE.format(
        industry=industry,
        client_type=client_type,
        raw_input=raw_input
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


# Output
if generate:
    if not raw_input.strip():
        st.warning("Please paste some client input.")
    else:
        with st.spinner("Thinking like a consulting PM..."):
            try:
                output = generate_draft(
                    raw_input,
                    industry,
                    client_type,
                    model
                )
                st.success("Draft Generated")
                st.markdown("## 📄 Generated Draft")
                st.markdown(output)
            except Exception as e:
                st.error(f"Error generating draft: {e}")
