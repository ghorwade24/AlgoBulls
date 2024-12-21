from django.db import models
from django.contrib.auth.models import User

#Create your models here
# class register(models.Model):
#     email = models.EmailField()
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     password = models.CharField(max_length=50)
#     created_date = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.user
    
class toDoList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    todo_name = models.CharField(max_length=1000)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.todo_name