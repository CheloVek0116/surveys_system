from django.db import models
from django.utils.translation import gettext_lazy as _


class AnswerOptionBase(models.Model):
    question = None
    text = models.CharField(_('Вариант ответа'), max_length=255)

    class Meta:
        abstract = True


class ChoiceAnswerOption(AnswerOptionBase):
    question = models.ForeignKey(
        'surveys.ChoiceQuestion', on_delete=models.CASCADE, related_name='answer_options')


class MultipleChoiceAnswerOption(AnswerOptionBase):
    question = models.ForeignKey(
        'surveys.MultipleChoiceQuestion', on_delete=models.CASCADE, related_name='answer_options')
