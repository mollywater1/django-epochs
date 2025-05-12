from django.contrib import admin
from .models import Era, Lecture, QuizQuestion, LectureProgress, UserProfile, MiniGameUnlock

@admin.register(Era)
class EraAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'era', 'order')
    list_filter = ('era',)
    ordering = ('era', 'order')

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'lecture', 'correct_answer')
    list_filter = ('lecture__era',)

@admin.register(LectureProgress)
class LectureProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lecture', 'viewed', 'quiz_completed')
    list_filter = ('viewed', 'quiz_completed')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'xp')

@admin.register(MiniGameUnlock)
class MiniGameUnlockAdmin(admin.ModelAdmin):
    list_display = ('user', 'era', 'unlocked')
    list_filter = ('unlocked', 'era')
