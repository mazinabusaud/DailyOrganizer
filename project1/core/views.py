from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from core.forms import JoinForm, LoginForm
import datetime
from tasks.models import Task
from budget.models import Budget
from journal.models import Journal

@login_required(login_url='/login/')
def home(request):
    tasks_db_completed = Task.objects.select_related().filter(user=request.user, is_completed=True).count()
    tasks_db_pending = Task.objects.select_related().filter(user=request.user, is_completed=False).count()
    budget_db_projected = Budget.objects.all().values_list('projected', flat=True).filter(user=request.user)
    budget_db_projected = list(budget_db_projected)
    budget_db_actual = Budget.objects.all().values_list('actual', flat=True).filter(user=request.user)
    budget_db_actual = list(budget_db_actual)
    row_tot = []
    total = Budget.objects.all().filter(user=request.user).values_list('projected').count()
    total_j = Journal.objects.all().filter(user=request.user).values_list('description').count()
    last_date = Journal.objects.latest('date')

    for rows in range(1, total+1):
        row_tot.append(rows)


    context = {
        "tasks_db_completed": tasks_db_completed,
        "tasks_db_pending": tasks_db_pending,
        "budget_db_projected": budget_db_projected,
        "budget_db_actual": budget_db_actual,
        "row_tot": row_tot,
        "total_j":total_j,
        "last_date":last_date
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # First get the username and password supplied
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)
            # If we have a user
            if user:
                #Check it the account is active
                if user.is_active:
                    # Log the user in.
                    auth_login(request,user)
                    # Send the user back to original page requested, or home page
                    next = request.POST.get('next', '/')
                    return HttpResponseRedirect(next)
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return render(request, 'core/login.html', {"login_form": LoginForm() } )
    else:
        return render(request, 'core/login.html', { "login_form": LoginForm() })

@login_required(login_url='/login/')
def logout(request):
    # Log out the user.
    auth_logout(request)
    # Return to homepage.
    return redirect("/")

def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
            # Encrypt the password
            user.set_password(user.password)
            # Save encrypted password to DB
            user.save()
            # Success! Redirect to home page.
            return redirect("/")
        else:
            # Form invalid, print errors to console
            print(join_form.errors)
            return render(request, 'core/join.html', { "join_form": join_form })
    else:
        return render(request, 'core/join.html', { "join_form": JoinForm() })
