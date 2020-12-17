from rest_framework import serializers

from surveys.models import (
    ChoiceQuestion,
    MultipleChoiceQuestion,
    TextAnswer,
    TextQuestion,
)
from surveys.serializers.answer_option import (
    ChoiceAnswerOptionSerializer,
    MultipleChoiceAnswerOptionSerializer,
)


class TextAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextAnswer
        fields = ('pk', 'text')


class TextQuestionResponseSerializer(serializers.ModelSerializer):
    answer = TextAnswerSerializer()

    class Meta:
        model = TextQuestion
        fields = ('pk', 'answer', 'question_type',)
        extra_kwargs = {'pk': {'read_only': False}}



class ChoiceQuestionResponseSerializer(serializers.ModelSerializer):
    answer = ChoiceAnswerOptionSerializer()

    class Meta:
        model = ChoiceQuestion
        fields = ('pk', 'answer', 'question_type',)
        extra_kwargs = {'pk': {'read_only': False}}


class MultipleChoiceQuestionResponseSerializer(serializers.ModelSerializer):
    answer = MultipleChoiceAnswerOptionSerializer(many=True)

    class Meta:
        model = MultipleChoiceQuestion
        fields = ('pk', 'answer', 'question_type',)
        extra_kwargs = {'pk': {'read_only': False}}
