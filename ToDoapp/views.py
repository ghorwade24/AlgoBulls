from django.shortcuts import get_object_or_404, render,redirect
# from .models import register
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from ToDoapp.models import toDoList
from rest_framework.decorators import api_view,permission_classes
from .serializers import ToDoSeriallizer
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required
def todo(request):
   user_tasks = toDoList.objects.filter(user=request.user)

   if request.method == "POST":
        # Handle adding a new task
        if "task" in request.POST:
            task = request.POST.get("task")
            if task:
                new_task = toDoList(user=request.user, todo_name=task)
                new_task.save()
        elif "delete" in request.POST:  # DELETE logic
              task_id = request.POST.get("task_id")
              
              task_to_delete = get_object_or_404(toDoList, id=task_id, user=request.user)
              task_to_delete.delete()
        elif "update" in request.POST:  # UPDATE logic
              task_id = request.POST.get("task_id")
              new_task_name = request.POST.get("task")
              task_to_update = get_object_or_404(toDoList, id=task_id, user=request.user)
              task_to_update.todo_name = new_task_name
              task_to_update.save()
        elif "complete" in request.POST:
              task_id = request.POST.get("task_id")
              task_to_mark = toDoList.objects.get(id=task_id, user=request.user)
              task_to_mark.status = not task_to_mark.status  # Toggle completion status
              task_to_mark.save()
      
   return render(request ,'myapp/todo.html',{"user":request.user, "task":user_tasks})
@csrf_exempt
@permission_classes([AllowAny])
def register(request):
   if request.method == "POST":
      email = request.POST.get("email")
      username = request.POST.get("username")
      password = request.POST.get("Password")
    
      if len(password) < 5:
             return Response({"detail": "Password must be at least 5 characters."}, status=status.HTTP_400_BAD_REQUEST)
     # Check if username already exists
      if User.objects.filter(username=username).exists():
             return Response({"detail": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)
     # Create new user
      User.objects.create_user(username=username, email=email, password=password)
      return Response({"detail": "Registered successfully!"}, status=status.HTTP_201_CREATED)


@csrf_exempt
@permission_classes([AllowAny])
def login(request):
   if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('Home_page')  # Redirect to home page after login
        return Response({"detail": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)  # Log out the user
        return redirect('login_page') 

# Create Task (API)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_task(request):
    serializer = ToDoSeriallizer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # Associate task with the current user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update Task (API)
@csrf_exempt
@api_view(['PUT'])
def update_task(request, task_id):
    task = get_object_or_404(toDoList, id=task_id, user=request.user)
    serializer = ToDoSeriallizer(task, data=request.data, partial=True)  # Partial update
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Delete Task (API)
@api_view(['DELETE'])
def delete_task(request, task_id):
    task = get_object_or_404(toDoList, id=task_id, user=request.user)
    task.delete()
    return Response({'detail': 'Task deleted'}, status=status.HTTP_204_NO_CONTENT)