# AI B2B Enquiry Assistant

A small applied-AI prototype that helps a B2B supplier triage a buyer enquiry. It extracts stated requirements, flags missing details, proposes clarification questions, and drafts a reply. Built as a learning project for an Assistant Product Manager application; it is not affiliated with or connected to IndiaMART.

## Features
- Structured extraction of product, quantity, budget, location, and delivery timeline.
- Heuristic intent label with a reason (not a sales prediction).
- Missing-information checks and suggested follow-up questions.
- Draft reply with instructions not to promise stock, pricing, or delivery.
- Transparent confidence and verification notes.

## Stack
- Python
- Streamlit for the user interface
- Google Gemini API (`gemini-2.5-flash`) for structured LLM output
- JSON output mode and a low temperature to improve consistency

## Run locally
1. Install Python 3.10+.
2. Download/clone this repository and open a terminal in its folder.
3. Install dependencies: `pip install -r requirements.txt`
4. Create a Gemini API key in Google AI Studio.
5. Set an environment variable named `GEMINI_API_KEY` (do not put the key in source code).
   - Windows PowerShell: `$env:GEMINI_API_KEY="your-key-here"`
   - macOS/Linux: `export GEMINI_API_KEY="your-key-here"`
6. Run: `streamlit run app.py`

## Deploy on Streamlit Community Cloud
1. Push this repository to your GitHub account.
2. Open https://share.streamlit.io and create an app from your repository, selecting `app.py`.
3. In the app's settings, add a secret named `GEMINI_API_KEY` with your API key, for example:
   `GEMINI_API_KEY = "your-key-here"`
4. Deploy and test the live app. Never commit your API key to GitHub.

## Manual evaluation plan
Try at least these cases and record what worked or failed:
1. Complete enquiry: "Need 200 safety helmets delivered to Pune by 20 November. Budget ₹300 each."
2. Missing quantity: "Please quote your best price for office chairs."
3. Vague timeline: "Need packaging material soon."
4. Contradictory request: "Need 50 laptops tomorrow, but delivery can happen next month."
5. Minimal enquiry: "Interested. Call me."

For each test, check whether the model preserves stated facts, leaves missing fields unknown, asks useful follow-up questions, and avoids making unsupported promises. The intent label is only a heuristic; do not treat it as a validated prediction.

## Limitations and next steps
- The model can still make mistakes; human review is required.
- Intent labels are heuristic and have not been validated against labelled historical enquiries.
- This version does not connect to a CRM, marketplace, supplier inventory, or private company data.
- A next iteration could add a labelled test set, field-level accuracy scoring, response-time/cost tracking, and a human feedback button.

## Responsible use
Use fictional or anonymised enquiry text in the demo. Do not submit personal or confidential customer information. Check model outputs before contacting a buyer or making commercial commitments.
