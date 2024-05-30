from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv
# from langchain_openai import OpenAI

# llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=512)
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
load_dotenv()

repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(repo_id=repo_id, temperature=0.7,)

prompt = PromptTemplate(
    input_variables=["question"],
    template="Your name is John, Only answer what i have ask, Answer this question in a happy manner: {question}"
)


class Chatbot:
    repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
    llm = HuggingFaceEndpoint(repo_id=repo_id, temperature=0.7, )

    prompt = PromptTemplate(
        input_variables=["question"],
        template="Your name is John, Only answer what i have ask, Answer this question in a happy manner: {question}"
    )

    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.userinput = ""
        self.bot_response = ""

    def response(self, userinput):
        if userinput != "":
            hub_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)
            self.bot_response = hub_chain.run(userinput)
            print(self.bot_response)
            return self.bot_response
        else:
            print("No input found please try again")


# Boot the AI
if __name__ == "__main__":
    AI_name = input("Name your chatbot:")
    ai = Chatbot(AI_name)
    ex = True
    while ex:
        ai.userinput = input("You:")
        ai.response(ai.userinput)

    print("----- Closing down chatbot -----")