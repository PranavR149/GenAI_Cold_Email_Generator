import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama3-70b-8192"  # Make sure the model name is valid
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            The scraped text is from the careers page of a website.
            Your task is to extract the exact job postings and return them in JSON format containing the following keys: 
            'role', 'experience', 'skills', and 'description'.

            Only return the valid JSON.

            ### VALID JSON (NO PREAMBLE):
            """
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            json_res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big, unable to parse jobs.")
        return json_res if isinstance(json_res, list) else [json_res]

    def write_email(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Pranav R looking for a relevant full-time opportunity in the field of data science and machine learning. 
            Your notice period is 30 days & you have 3.5+ years of relevant professional experience. Your techstack
            includes Tableau, Power Apps, Power Automate, Machine Learning, Pandas, Numpy, Scikit-learn, Matplotlib, Deep
            Learning, PyTorch, TensorFlow, Azure DevOps, Web Scraping, Python, HTML/CSS, Alteryx, SQL. Your current company 
            is Decision Point Analytics and your designation is Senior Data Scientist.

            Your job is to write a tailored cold email to the recruiter regarding the job opening mentioned above, 
            describing relevant experience that fulfills their needs.

            Also, add the most relevant projects from the following links to showcase the experience in that domain: {link_list}
            Remember you are a candidate looking for a full-time opportunity and ready to join in 30 days. 

            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke(input={"job_description": str(job), "link_list": links})
        return res.content
