import os

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI


def test_chain():
    os.environ["OPENAI_API_VERSION"] = os.getenv("PROXY_API_VERSION")
    os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
    os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")

    llm = AzureChatOpenAI(
        deployment_name=os.getenv("API_AZURE_DEPLOYMENT")
    )
    prompt = PromptTemplate(
        template="请问，{country}的首都是哪里 ?",
        input_variables=["country"],
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    print("\n", chain.invoke("中国"))

    print("\n\n")
    assert True