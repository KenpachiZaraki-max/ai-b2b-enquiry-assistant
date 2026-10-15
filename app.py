import json
import os
import re
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="B2B Enquiry Assistant", page_icon="🧾", layout="centered")
st.title("🧾 AI B2B Enquiry Assistant")
st.caption("A prototype for helping marketplace suppliers understand buyer enquiries and respond faster.")

with st.sidebar:
    st.subheader("About this prototype")
    st.write("This demo uses an LLM to extract enquiry details, flag missing information, and draft a reply. It is not affiliated with or connected to IndiaMART.")
    st.write("**Important:** AI outputs may be wrong. Verify details before acting on an enquiry.")

api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))

sample = "I need 500 office chairs delivered to Bhubaneswar next month. Please share your best price."
enquiry = st.text_area("Paste a buyer enquiry", value=sample, height=130, max_chars=4000,
                       help="Use fictional or non-sensitive enquiry text for this demo.")

SYSTEM_INSTRUCTIONS = """You are an assistant helping a B2B supplier triage buyer enquiries.
Extract only facts explicitly stated or strongly supported by the enquiry. Never invent details.
If a field is missing or ambiguous, use null and add a clarification question.
Do not infer a buyer's identity, financial status, or intent beyond the provided text.
Return valid JSON with exactly these keys:
product (string or null), quantity (string or null), budget (string or null),
location (string or null), delivery_timeline (string or null),
intent (one of: high, medium, low, unclear),
intent_reason (short string), missing_information (array of strings),
follow_up_questions (array of strings), suggested_reply (string),
confidence (one of: high, medium, low), verification_notes (array of strings).
Intent is a heuristic triage label, not a prediction of whether a sale will happen.
Keep the reply professional, concise, and do not promise stock, prices, or delivery."""

if st.button("Analyse enquiry", type="primary", use_container_width=True):
    if not enquiry.strip():
        st.warning("Enter an enquiry first.")
    elif not api_key:
        st.error("API key not configured. Add GEMINI_API_KEY in Streamlit Secrets or as an environment variable. See README for setup.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            with st.spinner("Analysing enquiry…"):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"Analyse this buyer enquiry:\n\n{enquiry}",
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTIONS,
                        response_mime_type="application/json",
                        temperature=0.2,
                    ),
                )
                raw = response.text or "{}"
                # Parse JSON strictly; surface errors rather than silently inventing results.
                result = json.loads(raw)
            st.subheader("Enquiry summary")
            a, b, c = st.columns(3)
            a.metric("Purchase intent", str(result.get("intent", "unclear")).title())
            b.metric("Confidence", str(result.get("confidence", "low")).title())
            c.metric("Quantity", result.get("quantity") or "Not stated")
            left, right = st.columns(2)
            with left:
                st.markdown("**Product**")
                st.write(result.get("product") or "Not stated")
                st.markdown("**Budget**")
                st.write(result.get("budget") or "Not stated")
                st.markdown("**Location**")
                st.write(result.get("location") or "Not stated")
            with right:
                st.markdown("**Delivery timeline**")
                st.write(result.get("delivery_timeline") or "Not stated")
                st.markdown("**Why this intent label?**")
                st.write(result.get("intent_reason") or "Not provided")
            st.markdown("### Missing information")
            missing = result.get("missing_information") or []
            if missing:
                for item in missing:
                    st.write(f"- {item}")
            else:
                st.write("No key gaps identified by the model; verify before acting.")
            st.markdown("### Suggested follow-up questions")
            for q in result.get("follow_up_questions") or ["No questions generated."]:
                st.write(f"- {q}")
            st.markdown("### Draft reply to buyer")
            st.info(result.get("suggested_reply") or "No reply generated.")
            notes = result.get("verification_notes") or []
            if notes:
                st.markdown("### Verification notes")
                for note in notes:
                    st.write(f"- {note}")
            with st.expander("View raw structured output (JSON)"):
                st.json(result)
            st.caption("Prototype only: review every extracted field and drafted response before using it.")
        except json.JSONDecodeError:
            st.error("The model returned an invalid structured response. Try again or inspect the deployment logs.")
        except Exception as exc:
            st.error(f"The request failed: {exc}")
            st.caption("Check that the API key is valid and the selected model is available to your account.")

st.divider()
st.markdown("**Suggested evaluation:** test vague enquiries, missing quantities, contradictory timelines, and enquiries with no budget. Check whether the app marks missing details as unknown rather than making them up.")
