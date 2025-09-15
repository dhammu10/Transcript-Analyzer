import streamlit as st
import requests
import pandas as pd
import os
import json

API_URL = "URL - here"   
API_KEY = "your_api_key_here"

# Call API
def analyze_transcript(transcript):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    prompt = f"""
    Summarize the following customer transcript in 2-3 sentences, 
    and provide the sentiment as one of: Positive, Neutral, Negative.
    Respond ONLY in valid JSON with keys 'summary' and 'sentiment'.
    
    Transcript:
    {transcript}
    """

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()


    output = result["choices"][0]["message"]["content"]

    clean_output = output.strip("`").strip()


    try:
        parsed = json.loads(clean_output)
        summary = parsed.get("summary", "N/A")
        sentiment = parsed.get("sentiment", "N/A")
    except Exception as e:
        summary, sentiment = output, "N/A"  # fallback if parsing fails

    return summary, sentiment


# Create CSV file
def save_to_csv(transcript, summary, sentiment, filename="call_analysis.csv"):
    row = pd.DataFrame([[transcript, summary, sentiment]], 
                       columns=["Transcript", "Summary", "Sentiment"])
    if os.path.exists(filename):
        row.to_csv(filename, mode="a", header=False, index=False)
    else:
        row.to_csv(filename, index=False)

# ---- STREAMLIT UI ----
st.title("📞 Call Transcript Analyzer")
st.write("Enter a customer call transcript, and get a summary + sentiment analysis.")

transcript = st.text_area("Enter Transcript", height=150)


col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    analyze_clicked = st.button("Analyze", key="analyze_button", use_container_width=True)

if analyze_clicked:
    if transcript.strip():
        summary, sentiment = analyze_transcript(transcript)
        st.subheader("Results")
        st.write("**Transcript:**", transcript)
        st.write("**Summary:**", summary)
        st.write("**Sentiment:**", sentiment)

        save_to_csv(transcript, summary, sentiment)
        st.success("✅ Saved to call_analysis.csv")
    else:
        st.warning("Please enter a transcript first!")

 
