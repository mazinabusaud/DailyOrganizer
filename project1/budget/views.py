from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from budget.models import Budget, BudgetCategory
from budget.forms import NewBudgetForm, EditBudgetForm
from core.models import UserProfile
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import permissions
from budget.serializers import BudgetSerializer, BudgetCategorySerializer
# Create your views here.
@login_required(login_url='/login/')
def budget(request):
    # Create some default categories if there aren't any.
    if (not BudgetCategory.objects.all()):
        BudgetCategory.objects.create(category="Food")
        BudgetCategory.objects.create(category="Clothing")
        BudgetCategory.objects.create(category="Housing")
        BudgetCategory.objects.create(category="Education")
        BudgetCategory.objects.create(category="Entertainment")
        BudgetCategory.objects.create(category="Other")

    if (request.method == "GET" and "delete" in request.GET):
        id = request.GET["delete"]
        Budget.objects.filter(id=id).delete()
        return redirect("/budget/")
    table_data = Budget.objects.select_related().filter(user=request.user)
    budget_db_projected = Budget.objects.all().values_list('projected', flat=True).filter(user=request.user)
    budget_db_projected = list(budget_db_projected)
    budget_db_actual = Budget.objects.all().values_list('actual', flat=True).filter(user=request.user)
    budget_db_actual = list(budget_db_actual)
    count1 = 0
    count2 = 0
    for items in budget_db_projected:
        count1 += items
    for items in budget_db_actual:
        count2 += items
    fin_count = count1-count2
    context = {
        "table_data": table_data,
        "fin_count": fin_count
    }
    return render(request, 'budget/budget.html', context)

def add(request):
    if (request.method == "POST"):
        if ("add" in request.POST):
            new_budget_form = NewBudgetForm(request.POST)
            if (new_budget_form.is_valid()):
                description = new_budget_form.cleaned_data["description"]
                category = new_budget_form.cleaned_data["category"]
                projected = new_budget_form.cleaned_data["projected"]
                actual = new_budget_form.cleaned_data["actual"]
                user = User.objects.get(id=request.user.id)
                Budget(user = user, description=description, category=category, projected=projected, actual=actual).save()
                return redirect("/budget/")
            else:
                context = {
                    "form_data": new_budget_form
                }
                return render(request, 'budget/add.html', context)
        else:
            # Cancel
            return redirect("/budget/")

    else:
        context = {
            "form_data": NewBudgetForm()
        }
        return render(request, 'budget/add.html', context)

def edit(request, id):
    if (request.method == "GET"):
        task = Budget.objects.get(id=id)
        form = EditBudgetForm(instance=task)
        context = { "form_data" : form }
        return render(request, 'budget/edit.html', context)

    if (request.method == "POST"):
        if ("update" in request.POST):
            form = EditBudgetForm(request.POST)
            if (form.is_valid()):
                task = form.save(commit=False)
                task.user = request.user
                task.id = id
                task.save()
                return redirect("/budget/")
            else:
                context = {
                    "form_data": form
                }
                return render(request, 'budget/add.html', context)
        else:
            #Cancel
            return redirect("/budget/")

class BudgetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tasks to be viewed or edited.
    """
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Task Categories to be viewed or edited.
    """
    queryset = BudgetCategory.objects.all()
    serializer_class = BudgetCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
