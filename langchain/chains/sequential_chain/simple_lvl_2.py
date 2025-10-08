# topic----->llm ------> report(obtained)------->llm------>get impt points from report


from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic'],
)
prompt2 = PromptTemplate(
    template='Extract the most important points from the {report}',
    input_variables=['report'],
)

model = ChatOpenAI()

parser = StrOutputParser()


chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({'topic':'Genz revolution in Nepal'})
print(result)