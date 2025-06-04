# Импортируем необходимые библиотеки
from typing import List, Union

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain.schema import StrOutputParser

import os

__all__=['graph']


examples = [
    "1. В этом ресторане подают сезонные блюда, приготовленные с исключительным вниманием к деталям.",
    "2. Элегантный интерьер и изысканная подача блюд создают атмосферу праздника.",
    "3. Местные ингредиенты в сочетании с французской техникой придают блюдам особый характер.",
    "4. Шеф-повар предлагает дегустационное меню, раскрывающее богатство вкусов региона.",
    "5. Каждое блюдо — это произведение искусства, в котором вкус и визуальное исполнение на высшем уровне.",
    "6. Приветливый персонал и уютная атмосфера делают этот ресторан идеальным для романтического вечера.",
    "7. Меню вдохновлено сезонными продуктами и авторской кулинарией шефа.",
    "8. Великолепная винная карта дополняет изысканные блюда, усиливая впечатление от ужина.",
    "9. Панорамный вид и креативная кухня делают ужин здесь незабываемым.",
    "10. Современная гастрономия с уважением к традициям — визитная карточка этого заведения."
]

class State(dict):
    messages: List[Union[HumanMessage, AIMessage]]


improve_prompt = ChatPromptTemplate.from_template(
    """
    На основе следующих описаний ресторанов:
    {examples}

    Улучши следующее описание ресторана, сделай его более качественным и продающим:
    {input}

    Напиши улучшенное описание:
    """
)


llm = init_chat_model(os.environ['MODEL_NAME'], model_provider='ollama')
improve_chain = improve_prompt | llm | StrOutputParser()

def improve_node(state: State):
    response = improve_chain.invoke({"examples": "\n\n".join(examples), "input": state['messages']})
    return {'messages': state['messages'] + [response]}


builder = StateGraph(State)

builder.add_node("improve", improve_node)

builder.add_edge(START, 'improve')
builder.add_edge('improve', END)

graph = builder.compile()