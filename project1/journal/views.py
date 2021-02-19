from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from journal.models import Journal
from journal.forms import NewJournalForm, EditJournalForm
from core.models import UserProfile
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import permissions
from journal.serializers import JournalSerializer


# Create your views here.
@login_required(login_url='/login/')
def journal(request):
    if (request.method == "GET" and "delete" in request.GET):
        id = request.GET["delete"]
        Journal.objects.filter(id=id).delete()
        return redirect("/journal/")
    table_data = Journal.objects.select_related().filter(user=request.user)

    context = {
    "table_data": table_data
    }
    return render(request, 'journal/journal.html', context)

def add(request):
    if (request.method == "POST"):
        if ("add" in request.POST):
            new_journal_form = NewJournalForm(request.POST)
            if (new_journal_form.is_valid()):
                description = new_journal_form.cleaned_data["description"]
                entry = new_journal_form.cleaned_data["entry"]
                user = User.objects.get(id=request.user.id)
                Journal(user=user, description=description, entry=entry).save()
                return redirect("/journal/")
            else:
                context = {
                    "form_data": new_journal_form
                }
                return render(request, 'journal/add.html', context)
        else:
            # Cancel
            return redirect("/journal/")

    else:
        context = {
            "form_data": NewJournalForm()
        }
        return render(request, 'journal/add.html', context)

def edit(request, id):
    if (request.method == "GET"):
        task = Journal.objects.get(id=id)
        form = EditJournalForm(instance=task)
        context = { "form_data" : form }
        return render(request, 'journal/edit.html', context)

    if (request.method == "POST"):
        if ("update" in request.POST):
            form = EditJournalForm(request.POST)
            if (form.is_valid()):
                task = form.save(commit=False)
                task.user = request.user
                task.id = id
                task.save()
                return redirect("/journal/")
            else:
                context = {
                    "form_data": form
                }
                return render(request, 'journal/add.html', context)
        else:
            #Cancel
            return redirect("/journal/")

class JournalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tasks to be viewed or edited.
    """
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    permission_classes = [permissions.IsAuthenticated]
