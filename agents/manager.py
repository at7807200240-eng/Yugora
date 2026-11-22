from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage


class ManagerAgent:
    def __init__(self):
        self.llm = ChatOllama(model="llama3", temperature=0.2)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Alex, the Engineering Manager at a tech startup. 
            Your tone is professional, direct, and helpful. 
            You are speaking to a junior developer. 
            Do NOT make up technical details outside the provided project scope.
            Project Scope: The team is building a Python web scraper. 
            Current Task: The user is assigned to write a function that extracts titles from a list of URLs."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{user_message}")
        ])

        self.chain = self.prompt | self.llm | StrOutputParser()

    def chat_with_developer(self, user_message: str, chat_history: list) -> str:
        formatted_history = []
        for msg in chat_history:
            if msg["role"] == "user":
                formatted_history.append(HumanMessage(content=msg["content"]))
            else:
                formatted_history.append(AIMessage(content=msg["content"]))

        response = self.chain.invoke({
            "user_message": user_message,
            "chat_history": formatted_history
        })
        return response