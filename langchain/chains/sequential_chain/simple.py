from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


model = ChatOpenAI()

prompt = PromptTemplate(
    template="Generate  5 insteresting fact about {topic}",
    input_variables=["topic"],
    input_types={"topic": "str"},
)

parser = StrOutputParser()

chain = prompt | model | parser
# secret to sequence is first we need to get PROMPT which will invoke MODEL and then we will get OUTPUT(PARSER)

result = chain.invoke({'topic':'Nepal'}) # input for the prompt
print(result)


# To visualize your chain
# chain.get_graph().print_ascii()