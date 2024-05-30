from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
# from langchain_openai import OpenAI
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
load_dotenv()

#llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=512)

repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(repo_id= repo_id, max_length=40, temperature=0.7,)

hub_llm = HuggingFaceHub(
        repo_id="mistralai/Mistral-7B-Instruct-v0.3",
        model_kwargs={'temperature': 0, 'repetition_penalty': 1.2, 'num_return_sequences': 1, 'min_length': 40, 'max_length': 80}
    )

prompt = PromptTemplate(
    input_variables=["question"],
    template="Answer this question in a happy manner: {question}"
)

class Chatbot:
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.userinput =""
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
    ai = Chatbot("John")
    ex = True
    while ex:
        ai.userinput = input("You:")
        ai.response(ai.userinput)

    print("----- Closing down chatbot -----")