from django.contrib import admin

from surveys.models import (
    ChoiceAnswer,
    ChoiceAnswerOption,
    ChoiceQuestion,
    MultipleChoiceAnswer,
    MultipleChoiceAnswerOption,
    MultipleChoiceQuestion,
    Survey,
    TextAnswer,
    TextQuestion,
)


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    pass


@admin.register(TextQuestion)
class TextQuestionAdmin(admin.ModelAdmin):
    exclude = ('question_type',)


@admin.register(ChoiceQuestion)
class ChoiceQuestionAdmin(admin.ModelAdmin):
    exclude = ('question_type',)


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    exclude = ('question_type',)


@admin.register(TextAnswer)
class TextAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(ChoiceAnswer)
class ChoiceAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(MultipleChoiceAnswer)
class MultipleChoiceAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(ChoiceAnswerOption)
class ChoiceAnswerOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(MultipleChoiceAnswerOption)
class MultipleChoiceAnswerOptionAdmin(admin.ModelAdmin):
    pass
