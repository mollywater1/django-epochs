from django.core.management.base import BaseCommand
from guide.models import QuizQuestion, Era

class Command(BaseCommand):
    help = 'Загрузка вопросов для викторины про Древний Египет'

    def handle(self, *args, **kwargs):
        # Найти эпоху "Древний Египет"
        try:
            egypt = Era.objects.get(name="Древний Египет")
        except Era.DoesNotExist:
            self.stdout.write(self.style.ERROR('Эпоха "Древний Египет" не найдена!'))
            return

        # Список вопросов
        egypt_quiz = egypt_quiz = [
            {
                "question": "Какое из семи чудес света связано с Древним Египтом?",
                "options": ["Пирамида Хеопса", "Висячие сады Семирамиды", "Колосс Родосский", "Маяк на острове Фарос"],
                "correct": "Пирамида Хеопса"
            },
            {
                "question": "Какой бог был богом солнца в Древнем Египте?",
                "options": ["Ра", "Анубис", "Осирис", "Сет"],
                "correct": "Ра"
            },
            {
                "question": "Что использовали древние египтяне для письма?",
                "options": ["Папирус", "Кирпичи", "Каменные таблички", "Деревянные дощечки"],
                "correct": "Папирус"
            },
            {
                "question": "Кого из фараонов называли 'девочкой-царем'?",
                "options": ["Клеопатра", "Тутанхамон", "Хатшепсут", "Рамсес II"],
                "correct": "Хатшепсут"
            },
            {
                "question": "Какой город был столицей Древнего Египта в период Древнего царства?",
                "options": ["Фивы", "Мемфис", "Александрия", "Амарна"],
                "correct": "Мемфис"
            },
            {
                "question": "Какая фигура в Гизе сочетает в себе тело льва и голову человека?",
                "options": ["Сфинкс", "Осирис", "Анубис", "Тот"],
                "correct": "Сфинкс"
            },
            {
                "question": "Каким было главное предназначение пирамид?",
                "options": ["Храмы", "Гробницы для фараонов", "Места собраний", "Наблюдательные пункты"],
                "correct": "Гробницы для фараонов"
            },
            {
                "question": "Какой бог Древнего Египта был связан с загробным миром?",
                "options": ["Анубис", "Гор", "Ра", "Хнум"],
                "correct": "Анубис"
            },
            {
                "question": "Какая река была основой жизни в Древнем Египте?",
                "options": ["Нил", "Евфрат", "Тигр", "Иордан"],
                "correct": "Нил"
            }
        ]

        # Добавление вопросов в базу данных
        for q in egypt_quiz:
            QuizQuestion.objects.create(
                era=egypt,
                question=q["question"],
                option1=q["options"][0],
                option2=q["options"][1],
                option3=q["options"][2],
                option4=q["options"][3],
                correct_answer=q["correct"]
            )

        self.stdout.write(self.style.SUCCESS('Вопросы для викторины про Древний Египет успешно добавлены!'))
