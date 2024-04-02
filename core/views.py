from django.shortcuts import render,redirect 
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Brand, Instagram
from openai import OpenAI
import plotly.express as px



client = OpenAI(
    # Defaults to os.environ.get("OPENAI_API_KEY")
    api_key='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'
)




def get_completion(prompt):
    query = client.chat.completions.create(
        model="gpt-3.5-turbo",
       messages=[ 
           {"role": "system", "content": "You are a Content Writer specializing in Brand Storytelling based on the interviews you have with a brand's CEO."},
           {"role": "user", "content": prompt}],
        max_tokens=1024,
        n=2,
        stop=None,
        temperature=1,
    )
    response = query.choices
    return response



def index(request):
    context = {
        'msg': 'Brand Builder'
    }
    return render(request, 'core/index.html', context)


def prompt(request):
    context = {}
    if request.method == "POST":

        q1 = request.POST.get('q1')
        q2 = request.POST.get('q2')
        q3 = request.POST.get('q3')

        br = Brand.objects.get(user = request.user)

        prompt =  f"""{br.name} is a brand situated in {br.address} with a strength of over {br.size} people.
        You recently had an interview with {br.name}. here's the manuscript of the same:
        Q1. What is your brand’s purpose?
        Ans. {q1}
        Q2. What is your Unique Selling Proposition (USP)?
        Ans. {q2}
        Q3. What emotions do you want your brand to evoke?
        Ans. {q3}

        Based on these responses build a brand story/advertisement. """


        response = get_completion(prompt)
        print(response)
        context['response'] = response

    
    return render(request, 'core/prompt.html', context)


def dashboard(request):
    context = {}
    if request.method == "POST":
        prompt = request.POST.get('prompt')
        response = get_completion(prompt)
        context['response'] = response

    return render(request, 'core/dashboard.html', context)

def profile(request):
    context = {}

    return render(request, 'core/profile.html', context)

def register(request):
    context = {}

    return render(request, 'core/register.html', context)

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


def competitorDisplay(request):
    brands = Brand.objects.all()

    context = {
        'brands': brands, 
    }
    return render(request, 'core/competitor.html', context)

def analysis(request, pk):
    br = Brand.objects.get(id=pk)
    ig = Instagram.objects.get(brand = br)

    bar = px.bar(
        y = [ig.tenthlikes, ig.eleventhlikes, ig.twelthlikes],
        x = [1, 2, 3],
        labels = {'x':'posts', 'y':'time'},
        title = "No of likes",
    )
    bar = bar.to_html()

    context = {
        'ig': ig,
        'bar': bar

    }

    return render(request, 'core/analysis.html', context)




# Create your views here.
