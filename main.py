import streamlit as st
from scrape import (scrape_website,split_content,clean_body_content,extract_body_content)
from parse import parse_with_ollama

st.title("Web Scrapping AI")
url = st.text_input("Enter URL: ")

if st.button("Scrape"):
    st.write("Scraping...")
    
    result  = scrape_website(url)
    body = extract_body_content(result)
    processed_body_content = clean_body_content(body)
    
    st.session_state.dom_content = processed_body_content

    with st.expander("View Raw Content: "):
        st.text_area("DOM Content", processed_body_content, height=250)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")
    
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing...")

            dom_chunks = split_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)

            st.write(result)
    
