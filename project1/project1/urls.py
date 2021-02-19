"""project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from core import views as core_views
from tasks import views as tasks_views
from budget import views as budget_views
from journal import views as journal_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'tasks', tasks_views.TaskViewSet)
router.register(r'users', tasks_views.UserViewSet)
router.register(r'task-categories', tasks_views.CategoryViewSet)
router.register(r'budget',budget_views.BudgetViewSet)
router.register(r'budget-categories', budget_views.CategoryViewSet)
router.register(r'journal',journal_views.JournalViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('tasks/', tasks_views.tasks, name='tasks'),
    path('tasks/add/', tasks_views.add, name='tasks_add'),
    path('tasks/edit/<int:id>/', tasks_views.edit, name='tasks_edit'),
    path('budget/', budget_views.budget, name='budget'),
    path('budget/add/',budget_views.add, name='budget_add'),
    path('budget/edit/<int:id>/', budget_views.edit, name='budget_edit'),
    path('journal/', journal_views.journal, name='journal'),
    path('journal/add/', journal_views.add, name='journal_add'),
    path('journal/edit/<int:id>/', journal_views.edit, name='journal_edit'),
    path('about/', core_views.about, name='about'),
    path('login/', core_views.login, name='login'),
    path('logout/', core_views.logout, name='logout'),
    path('join/', core_views.join, name='join'),
    path('api/v1/', include(router.urls)),
    path('api-auth/v1/', include('rest_framework.urls', namespace='rest_framework'))


]
