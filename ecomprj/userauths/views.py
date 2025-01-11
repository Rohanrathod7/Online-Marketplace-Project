from django.shortcuts import redirect,render
from userauths.forms import userRegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.conf import settings
from userauths.models import User, ContectUs

from django.http import JsonResponse

# User = settings.AUTH_USER_MODEL    #userauths.user we declared in setting


# Create your views here.
def register_view(request):

    if request.method == "POST":
        form = userRegisterForm(request.POST or None)  # take all the data from post request and and put it into form
        if form.is_valid():                                #if data is valid then save the form
            new_user = form.save()                          ## you can see user in admin panel
            username = form.cleaned_data.get("username")
            messages.success(request, f"hey {username}, Your Acccount Created Succesfully")  # flash massages
            new_user = authenticate(username = form.cleaned_data['email'],
                                    password = form.cleaned_data['password1']
            )
            print("User Register succesfully")
            login(request, new_user)
            return redirect("core:index")          # index page
                    
    else:
        form = userRegisterForm()  
        print("User Cannot Be Registered")

    context = {             # creating this dict to use userregisterform in template 
        'form': form        # assinig variable to key in dict
    }
    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request,f"Hey You are Alredy Loged in")
        return redirect("core:index")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email = email)
            user = authenticate(request, email= email, password = password)

            if user is not None:
                login(request, user)
                messages.success(request, "You logged in")
                return redirect("core:index")
            else:
                messages.warning(request, "User does not exist create an accont")

            
        except:
            messages.warning(request,f"User with {email} does not exist")
        
        
    return render(request, "userauths/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have Loged out")

    return redirect('userauths:sign-in')

def contectus(request):
    
    return render(request, "core/contect.html")

def ajx_contectus(request):
    name = request.GET["name"] 
    email = request.GET["email"]
    phone = request.GET["phone"]
    subject = request.GET["subject"]
    message = request.GET["message"]

    contact = ContectUs.objects.create(name = name, email = email, phone = phone, subject = subject, message = message)

    context = {
        "bool": True,
        "massage": "Your message has been sent",
    }

    messages.success(request, "Massage Submited.")

    return JsonResponse({'data': context})