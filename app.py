import streamlit as st
import requests
import json

BACKEND_URL = "http://127.0.0.1:8000/analyze-issue"

st.set_page_config(
    page_title="AI GitHub Issue Assistant",
    layout="centered"
)

st.title("🤖 AI-Powered GitHub Issue Assistant")
st.write("Analyze and summarize GitHub issues using AI")

# ---- Inputs ----
repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="your repo URL here... "
)

issue_number = st.number_input(
    "Issue Number",
    min_value=1,
    step=1
)

analyze_button = st.button("Analyze Issue")

# ---- Action ----
if analyze_button:
    if not repo_url:
        st.error("Please enter a GitHub repository URL.")
    else:
        with st.spinner("Analyzing issue..."):
            try:
                response = requests.post(
                    BACKEND_URL,
                    json={
                        "repo_url": repo_url,
                        "issue_number": issue_number
                    },
                    timeout=60
                )

                if response.status_code != 200:
                    st.error(response.json().get("detail", "Error analyzing issue"))
                else:
                    result = response.json()

                    st.success("Analysis complete!")

                    st.subheader("📌 Summary")
                    st.write(result["summary"])

                    st.subheader("📂 Type")
                    st.write(result["type"])

                    st.subheader("⚠️ Priority")
                    st.write(result["priority_score"])

                    st.subheader("🏷 Suggested Labels")
                    st.write(", ".join(result["suggested_labels"]))

                    st.subheader("📈 Potential Impact")
                    st.write(result["potential_impact"])

                    # ---- Raw JSON ----
                    st.subheader("📄 Raw JSON Output")
                    formatted_json = json.dumps(result, indent=2)
                    st.code(formatted_json, language="json")

                    # ---- Copy / Download Button (FEATURE 3) ----
                    st.download_button(
                        label="⬇️ Download JSON",
                        data=formatted_json,
                        file_name="issue_analysis.json",
                        mime="application/json"
                    )
                    
            except requests.exceptions.RequestException:
                st.error("Could not connect to backend. Is FastAPI running?")
