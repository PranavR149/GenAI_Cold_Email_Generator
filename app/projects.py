import pandas as pd
import chromadb
import uuid

class Projects:
    def __init__(self, file_path="app/resource/github_projects.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient(path='vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="projects")


    def load_projects(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row['Techstack']],  # must be a list of strings
                    metadatas=[{'URL': row["URL"]}],  # list of dicts
                    ids=[str(uuid.uuid4())]  # list of strings
                )

    #def query_links(self, skills):
     #   results = self.collection.query(query_texts=skills, n_results=2).get('metadata', [])

    def query_links(self, skills):
        if isinstance(skills, list):
            query = " ".join(skills)  # Join list of skills into a single string
        else:
            query = str(skills)  # Just in case it's not a list

        results = self.collection.query(query_texts=[query], n_results=2)
        return results.get('metadatas', [])