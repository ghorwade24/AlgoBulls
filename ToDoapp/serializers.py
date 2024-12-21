from rest_framework import serializers
from ToDoapp.models import toDoList
class ToDoSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = toDoList
        fields = ['id','user','status','todo_name']