# Getting response experimental
# installed packages: python-dotenv, langchain, langchainopenai (partner package)

from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

os.environ['HUGGINGFACEHUB_API_TOKEN'] = 'Your hugging face token'

load_dotenv()

hub_llm = HuggingFaceHub(
    repo_id="google/flan-t5-large",
    model_kwargs={'temperature': 0.8, 'min_length': 20, 'max_length': 100}
    )

prompt = PromptTemplate(
    input_variables=["question"],
    template="Answer this question in a happy manner: {question}"
)
hub_chain = LLMChain(prompt =prompt, llm= hub_llm, verbose=True)
print(hub_chain.run("Where is Malaysia"))
