from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .models import Era, Lecture, QuizQuestion, UserProfile, LectureProgress, MiniGameUnlock
import random

# Заглушка для случайных фактов
ERA_FACTS = {}

from guide.models import Lecture, LectureProgress

def home(request):
    eras = Era.objects.all()
    quizzes = QuizQuestion.objects.all()

    if request.user.is_authenticated:
        total = Lecture.objects.count()
        completed = LectureProgress.objects.filter(user=request.user, viewed=True).count()
        percent = int((completed / total) * 100) if total > 0 else 0
    else:
        total = completed = percent = 0

    return render(request, 'guide/home.html', {
        'eras': eras,
        'quizzes': quizzes,
        'total': total,
        'completed': completed,
        'percent': percent,
    })



@login_required
def era_detail(request, pk):
    era = get_object_or_404(Era, pk=pk)
    lectures = era.lectures.all()
    random_fact = random.choice(ERA_FACTS.get(era.name, ["Фактов пока нет."]))

    viewed_lectures = LectureProgress.objects.filter(user=request.user, lecture__in=lectures, viewed=True)
    progress_map = {lp.lecture_id: True for lp in viewed_lectures}

    unlock = MiniGameUnlock.objects.filter(user=request.user, era=era, unlocked=True).exists()

    return render(request, 'guide/era_details.html', {
        'era': era,
        'lectures': lectures,
        'random_fact': random_fact,
        'mini_game_unlocked': unlock,
        'progress_map': progress_map,
    })




from django.contrib import messages

from .models import MiniGameUnlock

from django.contrib import messages
from .models import LectureProgress, MiniGameUnlock

@login_required
def lecture_detail(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    user = request.user
    progress, _ = LectureProgress.objects.get_or_create(user=user, lecture=lecture)

    # Отмечаем просмотр
    if not progress.viewed:
        progress.viewed = True
        progress.save()

    questions = lecture.quiz_questions.all()

    if request.method == 'POST':
        correct = 0
        total = questions.count()
        for i, question in enumerate(questions):
            answer = request.POST.get(f'question_{i + 1}')
            if answer and answer.strip() == question.correct_answer.strip():
                correct += 1

        if correct == total:
            if not progress.quiz_completed:
                progress.quiz_completed = True
                progress.save()

                user.profile.xp += 10
                user.profile.save()

            messages.success(request, f"✅ Отлично! Ты ответил правильно на все {total} вопросов и получил 10 XP.")
        else:
            messages.warning(request, f"⚠️ Ты ответил правильно на {correct} из {total} вопросов. Попробуй ещё раз!")

    # Проверка мини-игры
    era_lectures = Lecture.objects.filter(era=lecture.era)
    viewed_count = LectureProgress.objects.filter(user=user, lecture__in=era_lectures, viewed=True).count()

    if viewed_count == era_lectures.count():
        MiniGameUnlock.objects.update_or_create(
            user=user,
            era=lecture.era,
            defaults={'unlocked': True}
        )

    # Список всех лекций этой эпохи + прогресс
    all_lectures = era_lectures.order_by('order')
    progress_map = {
        lp.lecture_id: lp.viewed
        for lp in LectureProgress.objects.filter(user=user, lecture__in=all_lectures)
    }

    return render(request, 'guide/lecture_detail.html', {
        'lecture': lecture,
        'questions': questions,
        'all_lectures': all_lectures,
        'progress_map': progress_map,
    })



@login_required
def quiz(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    questions = list(lecture.quiz_questions.all())

    if request.method == 'POST':
        correct = 0
        for i, question in enumerate(questions):
            selected = request.POST.get(f'question_{i+1}')
            if selected and selected.strip() == question.correct_answer.strip():
                correct += 1

        passed = correct == len(questions)
        progress, _ = LectureProgress.objects.get_or_create(user=request.user, lecture=lecture)
        if passed and not progress.quiz_completed:
            progress.quiz_completed = True
            progress.save()

        return render(request, 'guide/quiz_result.html', {
            'lecture': lecture,
            'correct': correct,
            'total': len(questions),
            'passed': passed,
        })

    return render(request, 'guide/quiz.html', {
        'lecture': lecture,
        'questions': questions
    })


@login_required
def profile_view(request):
    user = request.user
    completed, total, percent = calculate_progress(user)
    return render(request, 'guide/profile.html', {
        'profile': user.profile,
        'completed': completed,
        'total': total,
        'percent': percent,
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'guide/register.html', {'form': form})


@login_required
def mini_game(request, pk):
    era = get_object_or_404(Era, pk=pk)
    user = request.user
    lectures = era.lectures.all()

    # Проверка: все 10 лекций просмотрены?
    all_viewed = all(
        LectureProgress.objects.filter(user=user, lecture=lec, viewed=True).exists()
        for lec in lectures
    )

    unlock, _ = MiniGameUnlock.objects.get_or_create(user=user, era=era)
    if all_viewed and not unlock.unlocked:
        unlock.unlocked = True
        unlock.save()

    if not unlock.unlocked:
        return render(request, 'guide/mini_game_locked.html', {'era': era})

    # Награда XP за игру
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=user)
        profile.xp += 50
        profile.save()
        return redirect('era_detail', pk=era.pk)

    # Выбор шаблона мини-игры
    template_map = {
        "Древний Египет": 'guide/egypt_mini_game.html',
        "Античный Рим": 'guide/rome_mini_game.html',
        "Древняя Греция": 'guide/greece_mini_game.html',
        "Месопотамия": 'guide/mesopotamia_mini_game.html',
    }
    template_name = template_map.get(era.name, 'guide/default_mini_game.html')
    return render(request, template_name, {'era': era})


def calculate_progress(user):
    total_lectures = Lecture.objects.count()
    completed = LectureProgress.objects.filter(user=user, viewed=True).count()
    percent = int((completed / total_lectures) * 100) if total_lectures else 0
    return completed, total_lectures, percent
