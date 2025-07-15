import streamlit as st
import requests
import openai
import os

st.set_page_config(page_title="🧠 AGI Research Agent", page_icon="🤖")
st.title("🧠 AGI Research Agent")
st.markdown("Search AI/AGI papers and get intelligent summaries instantly.")

# Input
query = st.text_input("🔍 Enter your research question or topic:")
max_results = st.slider("📊 Max Results", 1, 15, 5)
sort_by = st.selectbox("🔄 Sort By", ["relevance", "lastUpdatedDate"])

if query:
    st.info("Searching arXiv...")
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}&sortBy={sort_by}"
    response = requests.get(url)
    entries = response.text.split("<entry>")[1:]

    for entry in entries:
        title = entry.split("<title>")[1].split("</title>")[0].strip()
        summary = entry.split("<summary>")[1].split("</summary>")[0].strip()
        link = entry.split("<id>")[1].split("</id>")[0].strip()

        st.subheader(title)
        st.markdown(f"[Read Paper]({link})")

        st.write("🧠 AI Summary:")
        try:
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            result = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AGI researcher."},
                    {"role": "user", "content": f"Summarize this:\n{summary}"}
                ]
            )
            st.success(result.choices[0].message.content)
        except Exception as e:
            st.error(f"OpenAI failed: {e}")
