from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()
from langchain.schema.runnable import RunnableParallel,RunnableBranch,RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from typing import Literal


model = ChatOpenAI()


parser = StrOutputParser()
#to use condition we have to make sure we get the output of first chain either positive or negative not Positive or This is positve format (it should be consistent)
class Feedback(BaseModel):
    sentiment : Literal['Positive', 'Negative'] = Field(description="Give the sentiment of the feedback either positive or negative and Respond in this JSON format: {{\"sentiment\": \"Positive\" or \"Negative\"}}")

parser2 = PydanticOutputParser(pydantic_object=Feedback)



prompt1 = PromptTemplate(
     template=(
        "Classify the sentiment of the following feedback into either 'Positive' or 'Negative'.\n"
        "Respond only in the following JSON format:\n"
        "{{\"sentiment\": \"Positive\"}}\n\n"
        "Feedback: {feedback}"
    ),
    input_variables=['feedback']
)
 
prompt2 = PromptTemplate(
    template='Write an appropriate response to this positive feedback \n {feedback}',
    input_variables=['feedback']
)
 
prompt3 = PromptTemplate(
    template='Write an appropriate response to this negative feedback \n {feedback}',
    input_variables=['feedback']
)


classifier_chain = prompt1 | model | parser2


branch_chain = RunnableBranch(
    (lambda x: x.sentiment == 'Positive' , prompt2 | model | parser),
    (lambda x: x.sentiment == 'Negative', prompt3 | model | parser),
    RunnableLambda(lambda x : 'could not find sentiment')
)



#Merging chains
chain = classifier_chain | branch_chain
result = chain.invoke({'feedback':'This is a terrible  product'})
print(result)