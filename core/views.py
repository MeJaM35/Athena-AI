from django.shortcuts import render,redirect 
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Brand, Instagram, AStory
from openai import OpenAI
import plotly.express as px
import random



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


@login_required(login_url='login')
def index(request):
    if not Brand.objects.filter(user=request.user).exists():
        return redirect('brand_form')
    stories = AStory.objects.filter(user=request.user)

    
    context = {
        'stories': stories
    }
    return render(request, 'core/index.html', context)

@login_required(login_url='login')
def prompt(request):
    if not Brand.objects.filter(user=request.user).exists():
        return redirect('brand_form')
    context = {}
    if request.method == "POST":
        q1 = request.POST.get('q1')
        q2 = request.POST.get('q2')
        q3 = request.POST.get('q3')

        # Fetch the user's brand
        br = Brand.objects.get(user=request.user)

        # Prepare the prompt
        prompt = f"""{br.name} is a brand situated in {br.address} with a strength of over {br.size} people.
        You recently had an interview with {br.name}. here's the manuscript of the same:
        Q1. What is your brand’s purpose?
        Ans. {q1}
        Q2. What is your Unique Selling Proposition (USP)?
        Ans. {q2}
        Q3. What emotions do you want your brand to evoke?
        Ans. {q3}

        Based on these responses build a brand story/advertisement."""

        # Get the response from the model
        response = get_completion(prompt)
        print(response)

        # Save the story in the database
        AStory.objects.create(
            user=request.user,
            brand=br,
            q1=q1,
            q2=q2,
            q3=q3,
            response=response
        )

        # Pass the response to the template
        context['response'] = response

    return render(request, 'core/prompt.html', context)



@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        
        # Get data from the form
        username = request.POST.get('username', user.username)
        first_name = request.POST.get('first_name', user.first_name)
        last_name = request.POST.get('last_name', user.last_name)
        email = request.POST.get('email', user.email)
        phone = request.POST.get('phone', user.phone)
        
        # Validate and update fields
        try:
            if email and User.objects.exclude(pk=user.pk).filter(email=email).exists():
                messages.error(request, "Email already in use.")
            elif username and User.objects.exclude(pk=user.pk).filter(username=username).exists():
                messages.error(request, "Username already in use.")
            else:
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.phone = phone
                user.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('profile')  # Redirect to a profile view
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    # Render the profile editing form
    context = {
        'user': request.user
    }
    return render(request, 'core/edit_profile.html', context)

@login_required(login_url='login')
def profile(request):
    if not Brand.objects.filter(user=request.user).exists():
        return redirect('brand_form')
    context = {}

    return render(request, 'core/profile.html', context)

def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        tel = request.POST.get('tel')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        confirm_password = request.POST.get('con_pass')
        
        # Server-side validation
        if not firstname or not lastname:
            messages.error(request, 'First Name and Last Name are required')
            return render(request, 'core/register.html')
            
        if not tel or len(tel) != 10 or not tel.isdigit():
            messages.error(request, 'Enter a valid 10-digit Contact Number')
            return render(request, 'core/register.html')
            
        if not email or '@' not in email or '.' not in email:
            messages.error(request, 'Enter a valid Email ID')
            return render(request, 'core/register.html')
            
        if not password:
            messages.error(request, 'Password is required')
            return render(request, 'core/register.html')
            
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'core/register.html')
            
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered')
            return render(request, 'core/register.html')
            
        # Create user
        user = User.objects.create_user(
            username=email,  # Using email as username
            email=email,
            password=password,
            first_name=firstname,
            last_name=lastname
        )
        
        # Create profile for additional fields if needed
        # profile = Profile.objects.create(user=user, phone_number=tel)
        
        # Authenticate user before login
        authenticated_user = authenticate(username=email, password=password)
        
        if authenticated_user:
            # Log user in with the specified backend
            login(request, authenticated_user)
            messages.success(request, 'Registration successful!')
            return redirect('prompt')  # Redirect to prompt page after signup
        else:
            messages.error(request, 'Authentication failed after registration. Please try logging in.')
            return redirect('login')
        
    return render(request, 'core/register.html')


def cards(request):
    if not Brand.objects.filter(user=request.user).exists():
        return redirect('brand_form')
    context = {}

    return render(request, 'cards.html', context)

def loginUser(request):
    page = 'login'
    
    # Redirect authenticated users to the index page
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')

        # Validate input fields
        if not email or not password:
            messages.error(request, "Email and password are required.")
            return redirect('login')

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            
            # Redirect to the next page if it exists, otherwise index
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
        else:
            messages.warning(request, 'Invalid email or password.')

    # Context for rendering the login page
    context = {'page': page}
    return render(request, 'core/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def competitorDisplay(request):
    if not Brand.objects.filter(user=request.user).exists():
        return redirect('brand_form')
    brands = Brand.objects.all()

    context = {
        'brands': brands, 
    }
    return render(request, 'core/competitor.html', context)

@login_required
def analysis(request, pk):
    if not Brand.objects.filter(user=request.user).exists():
        return redirect('brand_form')
    br = Brand.objects.get(id=pk)
    ig = Instagram.objects.get(brand = br)

    my_br = Brand.objects.get(id=request.user.brand.id)
    my_ig = Instagram.objects.get(brand = my_br)



    totallikes = ig.tenthlikes+ig.eleventhlikes+ig.twelthlikes

    bar = px.bar(
        x=['Total Posts', 'Total Followers', 'Total likes'],
        y=[ig.totalposts, ig.totalfollows, totallikes],
        labels={'x': 'Brands', 'y': 'Counts'},
        title='Comparison of Posts, Followers, and Likes',
        color_discrete_sequence=['skyblue', 'orange', 'green']
    )
    bar = bar.to_html()

    pie = px.pie(
        values = [ig.tenthlikes, ig.eleventhlikes, ig.twelthlikes],
        names = ['tenth post', 'eleventh post', 'twelfth post'],
        title='likes',

    )

    pie = pie.to_html

    line = px.line(
    y=[10, 11, 12, 10, 11, 12], # Repeating post numbers for each brand
    x=[ig.tenthlikes, ig.eleventhlikes, ig.twelthlikes, my_ig.tenthlikes, my_ig.eleventhlikes, my_ig.twelthlikes],
    labels={'x': 'Post Number', 'y': 'Number of Likes'},
    title='Likes Trend Across Posts for Different Brands',
    color=[10, 11, 12, 10, 11, 12],  # Repeating brand names for each post
    )
    
    line = line.to_html()

    scatter = px.scatter(
    x=[ig.totalfollows, my_ig.totalfollows],
    y=[totallikes, my_ig.tenthlikes+my_ig.eleventhlikes+my_ig.twelthlikes],
    text=[br.name, my_br.name],  # Display brand names as labels
    labels={'x': 'Total Followers', 'y': 'Total Likes'},
    title='Relationship Between Total Followers and Total Likes',
    color=[br.name, my_br.name],  # Color points based on brand
    hover_name=[br.name, my_br.name],  # Show brand names on hover
    )

    scatter = scatter.to_html()




    context = {
        'ig': ig,
        'bar': bar, 
        'pie': pie,
        'line': line,
        'scatter': scatter,

    }

    return render(request, 'core/analysis.html', context)

@login_required
def brand_form_view(request):
    # If the user already has a brand, redirect them to dashboard (or another page)
    if Brand.objects.filter(user=request.user).exists():
        return redirect('dashboard')

    if request.method == "POST":
        # Manually retrieve form data from POST request
        name = request.POST.get("name")
        address = request.POST.get("address")
        size = request.POST.get("size")
        try:
            size = int(size) if size else -1
        except ValueError:
            size = -1  # Fallback in case of conversion error

        # Create the Brand object associated with the current user
        brand = Brand.objects.create(
            user=request.user,
            name=name,
            address=address,
            size=size
        )

        # Generate random Instagram data for this brand
        Instagram.objects.create(
            brand=brand,
            url=f"https://instagram.com/{name.replace(' ', '').lower()}",
            tag=f"#{name.replace(' ', '').lower()}",
            totalposts=random.randint(10, 500),
            totalfollows=random.randint(100, 10000),
            tenthlikes=random.randint(10, 500),
            eleventhlikes=random.randint(10, 500),
            twelthlikes=random.randint(10, 500),
            lastninereach=random.randint(100, 10000),
        )

        # Redirect to dashboard after successful submission
        return redirect('dashboard')

    return render(request, "core/forms.html")


# Create your views here.
