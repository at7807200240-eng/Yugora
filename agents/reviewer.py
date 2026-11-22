from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class QAAgent:
    def __init__(self):
        self.llm = ChatOllama(model="llama3", temperature=0.1)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Sarah, the Senior QA Engineer. 
            A junior developer is submitting Python code for a web scraper that extracts titles from URLs.
            Review the code carefully. 
            If the code looks like it will successfully extract titles, start your response exactly with the word: PASS
            If it has errors or is incomplete, start your response exactly with the word: FAIL
            After PASS or FAIL, provide 1-2 sentences of feedback."""),
            ("human", "Here is my code submission:\n\n{student_code}")
        ])

        self.chain = self.prompt | self.llm | StrOutputParser()

    def review_code(self, student_code: str) -> str:
        return self.chain.invoke({"student_code": student_code})