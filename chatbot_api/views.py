from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from rest_framework.decorators import api_view
import json
from .multivector_system import multivector_QA
from .routing_layer_query_intent import routing_layer
from .multiple_database import rag_multiple_database
from .Generate_format_output import format_response
from django.core.cache import cache
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def chatbot_html(request):
    template = loader.get_template('chatbot.html')
    return HttpResponse(template.render())

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chatapp:chatbot_api')
        else:
            return render(request, 'login_page.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'Login_page.html')


def json_to_chathistory(history):
    res = []
    for each in history:
        res.append((each[0], each[1]))
    return res


# @api_view(['POST'])
# def chat(request):
#     #  return request
#     raw_data = request.body.decode('utf-8')
    
#     # Deserialize the JSON content
#     json_data = json.loads(raw_data)
    
#     chat_history = json_to_chathistory(json_data['chat_history'])
    
#     res = rag_multiple_database(json_data['input'], chat_history)
#     # res = multivector_QA(json_data['input'])
    
#     return JsonResponse(
#         {
#             "query": json_data['input'],
#             "result": res['answer'],
#             "chat_history": json_data['chat_history'],
#         }
#     )
    
# @api_view(['POST'])
# def chat(request):
#     #  return request
#     raw_data = request.body.decode('utf-8')
    
#     # Deserialize the JSON content
#     json_data = json.loads(raw_data)
    
#     chat_history = json_to_chathistory(json_data['chat_history'])
    
#     res = multivector_QA(json_data['input'], chat_history)
    
#     return JsonResponse(
#         {
#             "query": json_data['input'],
#             "result": res['answer'],
#             "chat_history": json_data['chat_history'],
#         }
#     )
from datetime import datetime
@api_view(['POST'])
# @login_required
def chat(request):
    if True:
        print("write this code ------------------------")
            # print(request.user)
            # raise Exception("This is an example exception raised in main.py")
            # return redirect('login_page')
        import time
        t1=datetime.now()
        start_time = time.time()
        raw_data = request.body.decode('utf-8')
        json_data = json.loads(raw_data)
        chat_history = json_to_chathistory(json_data['chat_history']) 
        res = routing_layer(json_data['input'], chat_history)
        t2=datetime.now()
        answer = ''
        if res:
            answer = format_response(res['answer'])
            answer = answer.strip().replace("```html", "").replace("```", "")
        else:
            answer = "Sorry, I couldn't find an answer for your query. Please try again or ask a different question."       
        end_time = time.time()
        # t3=datetime.now()
        elapsed_time = end_time - start_time
        elapsed_time_seconds = round(elapsed_time, 3)
        # print("elapsed_time_seconds",elapsed_time_seconds)
        return JsonResponse(
            {
                "query": json_data['input'],
                "result": answer,
                "chat_history": json_data['chat_history'],
            }
        )
    # except Exception as e:
    #     return JsonResponse({
    #         "query": "some internal issue in api",
    #         "error": str(e),
    #         "chat_history": "error",
    #     })
    
