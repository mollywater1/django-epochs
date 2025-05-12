from django.db import models
from django.contrib.auth.models import User

# Эпоха (Греция, Рим, Египет, Месопотамия и т.п.)
class Era(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name

# Лекция в рамках эпохи
class Lecture(models.Model):
    era = models.ForeignKey(Era, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField()  # от 1 до 10

    class Meta:
        unique_together = ('era', 'order')
        ordering = ['era', 'order']

    def __str__(self):
        return f"{self.era.name} — Лекция {self.order}: {self.title}"

# Вопрос по конкретной лекции
class QuizQuestion(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='quiz_questions')
    question = models.CharField(max_length=255, default='')
    option1 = models.CharField(max_length=255, default='')
    option2 = models.CharField(max_length=255, default='')
    option3 = models.CharField(max_length=255, default='')
    option4 = models.CharField(max_length=255, default='')
    correct_answer = models.CharField(max_length=255, default='')

    def correct_option(self):
        return self.correct_answer

    def __str__(self):
        return f"Вопрос: {self.question}"

# Прогресс по каждой лекции
class LectureProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)
    quiz_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'lecture')

# Открыта ли мини-игра для всей эпохи
class MiniGameUnlock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    era = models.ForeignKey(Era, on_delete=models.CASCADE)
    unlocked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'era')

# Профиль пользователя (очки опыта и т.д.)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    xp = models.IntegerField(default=0)

    def __str__(self):
        return f"Профиль: {self.user.username}"
