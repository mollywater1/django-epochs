from django.contrib import admin
from .models import Era, Material, Lecture, QuizQuestion

@admin.register(Era)
class EraAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'era')

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'era')

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'era', 'correct_option')
