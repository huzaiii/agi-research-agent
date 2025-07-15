import streamlit as st
import requests
from openai import OpenAI
import os

# Set up page
st.set_page_config(page_title="🧠 AGI Research Agent", page_icon="🤖")
st.title("🧠 AGI Research Agent")
st.markdown("Search AI/AGI papers and get intelligent summaries instantly.")

# Get API key from Streamlit secrets (via secrets.toml)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# UI Inputs
query = st.text_input("🔍 Enter your research question or topic:")
max_results = st.slider("📊 Max Results", 1, 15, 5)
sort_by = st.selectbox("🔄 Sort By", ["relevance", "lastUpdatedDate"])

# Search and summarize
if st.button("Search") and query:
    st.info("Searching arXiv...")
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}&sortBy={sort_by}"
    try:
        response = requests.get(url)
        entries = response.text.split("<entry>")[1:]

        for entry in entries:
            title = entry.split("<title>")[1].split("</title>")[0].strip()
            summary = entry.split("<summary>")[1].split("</summary>")[0].strip()
            link = entry.split("<id>")[1].split("</id>")[0].strip()

            st.subheader(f"📄 {title}")
            st.markdown(f"[Read Paper]({link})")

            # Summarize with OpenAI
            with st.spinner("Summarizing..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful AGI research assistant."},
                            {"role": "user", "content": f"Summarize this academic paper:\n{summary}"}
                        ]
                    )
                    ai_summary = response.choices[0].message.content
                    st.success("🧠 Summary:")
                    st.write(ai_summary)
                except Exception as e:
                    st.error(f"OpenAI Error: {e}")

    except Exception as e:
        st.error(f"arXiv fetch error: {e}")
