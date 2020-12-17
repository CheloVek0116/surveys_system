from django.db import models
from django.utils.translation import gettext_lazy as _


class Survey(models.Model):
    name = models.CharField(_('Название теста'), max_length=255)
    start_date = models.DateField(_('Дата старта'))
    end_date = models.DateField(_('Дата окончания'))
    description = models.TextField(_('Описание'))

    def __str__(self):
        return f'Опрос "{self.name}"'

    def is_already_answered(self, user_id):
        text_questions = self\
            .textquestion_set\
            .filter(text_answers__user_id=user_id)
        choice_questions = self\
            .choicequestion_set\
            .filter(choice_answers__user_id=user_id)
        multiple_choice_questions = self\
            .multiplechoicequestion_set\
            .filter(multiple_choice_answers__user_id=user_id)

        return text_questions.exists() or choice_questions.exists() or multiple_choice_questions.exists()
