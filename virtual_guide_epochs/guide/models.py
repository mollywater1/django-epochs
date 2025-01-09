from django.db import models

class Era(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Material(models.Model):
    era = models.ForeignKey(Era, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='images/materials/', null=True, blank=True)

    def __str__(self):
        return self.title

class Lecture(models.Model):
    era = models.ForeignKey(Era, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    era = models.ForeignKey(Era, on_delete=models.CASCADE, related_name='quiz_questions')
    question = models.CharField(max_length=255,default='')
    option1 = models.CharField(max_length=255,default='')
    option2 = models.CharField(max_length=255,default='')
    option3 = models.CharField(max_length=255,default='')
    option4 = models.CharField(max_length=255,default='')
    correct_answer = models.CharField(max_length=255, default='')

    def correct_option(self):
        return self.correct_answer
    def __str__(self):
        return self.question


from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    xp = models.IntegerField(default=0)

    def __str__(self):
        return f"Profile of {self.user.username}"

