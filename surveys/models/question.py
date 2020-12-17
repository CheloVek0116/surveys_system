from django.db import models
from django.utils.translation import gettext_lazy as _

from surveys.enums import QuestionTypes


class QuestionBase(models.Model):
    survey = models.ForeignKey('surveys.Survey', on_delete=models.CASCADE, verbose_name=_('Опрос'))
    name = models.CharField(_('Вопрос'), max_length=255)
    question_type = models.CharField(_('тип вопроса'), choices=QuestionTypes.choices(), max_length=255)

    class Meta:
        abstract = True


class TextQuestion(QuestionBase):
    def __str__(self):
        return f'Текстовый опрос "{self.name}"'

    def save(self, **kwargs):
        self.question_type = QuestionTypes.TEXT.value
        super().save(**kwargs)


class ChoiceQuestion(QuestionBase):
    def __str__(self):
        return f'Вопрос с выбором "{self.name}"'

    def save(self, **kwargs):
        self.question_type = QuestionTypes.CHOICE.value
        super().save(**kwargs)


class MultipleChoiceQuestion(QuestionBase):
    def __str__(self):
        return f'Вопрос с выбором нескольких вариантов "{self.name}"'

    def save(self, **kwargs):
        self.question_type = QuestionTypes.MULTIPLE_CHOICE.value
        super().save(**kwargs)
