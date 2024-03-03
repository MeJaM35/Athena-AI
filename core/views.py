from django.shortcuts import render,redirect 
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from openai import OpenAI
client = OpenAI(
    # Defaults to os.environ.get("OPENAI_API_KEY")
    api_key='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'
)




def get_completion(prompt):
    query = client.chat.completions.create(
        model="gpt-3.5-turbo",
       messages=[ 
           {"role": "system", "content": "You are a helpful assistant."},
           {"role": "user", "content": prompt}],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    response = query.choices[0]
    return response



def index(request):
    context = {
        'msg': 'Brand Builder'
    }
    return render(request, 'core/index.html', context)


def prompt(request):
    context = {}
    if request.method == "POST":
        prompt = request.POST.get('prompt')
        response = get_completion(prompt)
        context['response'] = response

    
    return render(request, 'core/prompt.html', context)

def cards(request):
    context = {}

    return render(request, 'cards.html', context)

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        print(f"{email} {password}")

        

        user = authenticate(request, username=email, password=password)
        print(user)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.warning(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'core/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('index')



# Create your views here.
