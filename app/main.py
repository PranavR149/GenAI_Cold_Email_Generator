import streamlit as st
from chains import Chain
from projects import Projects
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader


def create_streamlit_app(llm, projects, clean_text):
    st.title("Cold Email Generator")
    url_input = st.text_input("Enter a URL: ", value="https://careers.nike.com/lead-data-engineer-itc/job/R-56784")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            projects.load_projects()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills',[])
                url = projects.query_links(skills)
                email = llm.write_email(job, url)
                st.code(email, language = 'markdown')
        except Exception as e:
            st.error(f"An Error Occured: {e}")

if __name__ == "__main__":
    chain = Chain()
    projects = Projects()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📮")
    create_streamlit_app(chain, projects, clean_text)

