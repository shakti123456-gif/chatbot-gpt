from django.shortcuts import render
from langchain_community.document_loaders import CSVLoader
import pandas as pd
from .query_classification_intent import get_classification_intent
from .SQL_Query_QA import get_quantitative_answer
from .rag_system import rag
from .vectorIndexCreatorQA import vector_embeddings
from .multivector_system import multivector_QA
import json
from datetime import datetime
from django.core.cache import cache

def routing_layer(query, chat_history):
    t1=datetime.now()
    print("Current Time:", t1.strftime("%H:%M:%S.%f"))
    classification_type = get_classification_intent(query)
    cache.set('global_value', str(classification_type)+str(t1))
    print(classification_type)
    t2=datetime.now()
    print(t1,"--------------------",t2,"---------------",t2-t1)
    if classification_type:
        if "quantitative" in classification_type.lower():
            res = get_quantitative_answer(query)
            response_output = {'question': query, 'chat_history':[], 'answer': res}
            return response_output
        elif 'subjective' in classification_type.lower():
            res = rag(query, chat_history)
            return res
        else:
            print("else")