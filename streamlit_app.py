import streamlit as st
import fitz  # PyMuPDF
import openai

st.set_page_config(page_title="AI Loan Dashboard", page_icon="💼", layout="wide")
st.title("💼 AI Loan Analyzer Dashboard")

uploaded_file = st.file_uploader("Upload a PDF tax return", type="pdf")
openai_api_key = st.text_input("Enter your OpenAI API key", type="password")

if uploaded_file and openai_api_key:
    st.info("Reading PDF...")
    pdf_text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            pdf_text += page.get_text()

    prompt = f"""You are a business loan analyst. Based on this business tax return text:
{pdf_text}

    Summarize the key financials (revenue, net income, profit margin, etc.) and provide potential risks or red flags for loan approval.
    Then generate a professional, friendly email summary for the client explaining your findings and suggestions.
    """

    openai.api_key = openai_api_key
    with st.spinner("Analyzing..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        result = response.choices[0].message["content"]
        st.success("Analysis complete!")
        st.markdown("### 📊 AI Financial Summary + Email Draft")
        st.text_area("Result", result, height=400)