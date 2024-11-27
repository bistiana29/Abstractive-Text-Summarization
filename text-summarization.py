# Import Library
import re 
import streamlit as st
from transformers import pipeline

# Streamlit UI
st.markdown(
    """<div><h1 style='font-size: 35px; margin: 0;'><center>📄 Text Summarization 📄</center></h1></div>""",
    unsafe_allow_html=True
    )

# Input long text
input_text = st.text_area("Input Original Text:", height=250)

# Preprocessing
def text_preprocessing(text):
    # sign end of sentences
    text = text.replace('.', '.<eos>')
    text = text.replace('?', '?<eos>')
    text = text.replace('!', '!<eos>')

    # clean text (lowercase, remove hashtag, non-alfanumeric, mention, url, etc.)
    def clean_text(text):
        text = re.sub(r'#\w+', '', text)
        text = re.sub(r"[^\w\s?!]", '', text)
        text = re.sub(r'https?://\S+', '', text)
        text = re.sub(r'@[A-Za-z0-9_]+', '', text)
        text = text.lower()
        words = text.split()
        
        return ' '.join(words)

    return clean_text(text)

processed_text = text_preprocessing(input_text)

# Text Summarization
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
if st.button('Summarize'):
    with st.spinner('Generating Summary.....'):
        summarized_text = summarizer(processed_text,
                                    max_length=150,
                                    min_length=50,
                                    do_sample=False)
        summarized_text = summarized_text[0]['summary_text']
    st.success('Text has been summarized')
    st.text_area("Summarized Text:", summarized_text, height=250)

    word_count_original = len(input_text.split())
    word_count_summarized = len(summarized_text.split())

    st.write(f'Original word count: {word_count_original}')
    st.write(f'Summarized word count: {word_count_summarized}')
