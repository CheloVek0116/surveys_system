from django.db import models
from django.utils.translation import gettext_lazy as _


class AnswerBase(models.Model):
    question = None
    user_id = models.IntegerField()

    class Meta:
        abstract = True


class TextAnswer(AnswerBase):
    question = models.ForeignKey(
        'surveys.TextQuestion', on_delete=models.CASCADE, related_name='text_answers')
    text = models.CharField(_('Ответ'), max_length=255)


class ChoiceAnswer(AnswerBase):
    question = models.ForeignKey(
        'surveys.ChoiceQuestion', on_delete=models.CASCADE, related_name='choice_answers')
    choice = models.ForeignKey('surveys.ChoiceAnswerOption', on_delete=models.CASCADE)


class MultipleChoiceAnswer(AnswerBase):
    question = models.ForeignKey(
        'surveys.MultipleChoiceQuestion', on_delete=models.CASCADE, related_name='multiple_choice_answers')
    choices = models.ManyToManyField('surveys.MultipleChoiceAnswerOption')
