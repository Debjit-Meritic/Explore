from django.shortcuts import render, redirect
from django.http import JsonResponse

from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
client = OpenAI(
    api_key = os.environ['OPENAI_API_KEY']
)

from django.contrib import auth
from django.contrib.auth.models import User

from .models import Chat
from django.utils import timezone
# from langchain.globals import set_debug
from . import langgraph_agent

# set_debug(True)



def ask_openai(message):
    response = client.chat.completions.create(model = "gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an helpful assistant."},
        {"role": "user", "content": message},
    ])

    answer = response.choices[0].message.content.strip()
    return answer

# Create your views here.
def chatbot(request):
    chats = Chat.objects.filter(user=request.user.id)

    if request.method == 'POST':
        message = request.POST.get('message')
        responses = langgraph_agent.process_message(message)
        last_response = responses[-1].content if responses else "No response generated"

        chat = Chat(user=request.user, message=message, response=last_response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': last_response})
    return render(request, 'chatbot.html', {'chats': chats})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')