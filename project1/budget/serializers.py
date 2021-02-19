from budget.models import Budget, BudgetCategory
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class BudgetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        user = UserSerializer()
        model = Budget
        fields = '__all__'

class BudgetCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BudgetCategory
        fields = '__all__'
