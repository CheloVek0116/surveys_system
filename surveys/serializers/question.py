from rest_framework import serializers

from surveys.models import (
    ChoiceAnswerOption,
    ChoiceQuestion,
    MultipleChoiceAnswerOption,
    MultipleChoiceQuestion,
    TextQuestion,
)
from surveys.serializers.answer import TextAnswerSerializer
from surveys.serializers.answer_option import (
    ChoiceAnswerOptionCreateSerializer,
    ChoiceAnswerOptionSerializer,
    MultipleChoiceAnswerOptionCreateSerializer,
    MultipleChoiceAnswerOptionSerializer,
)


class TextQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextQuestion
        fields = ('pk', 'name', 'question_type',)


class ChoiceQuestionSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()

    class Meta:
        model = ChoiceQuestion
        fields = ('pk', 'name', 'question_type', 'choices',)

    def get_choices(self, obj):
        return ChoiceAnswerOptionSerializer(
            obj.answer_options.all(), many=True).data

    def validate(self, obj):
        data = super().validate(obj)
        data['choices'] = self.validate_choices(self.initial_data['choices'])
        return data

    def validate_choices(self, value):
        choices = []
        for choice in value:
            serializer = ChoiceAnswerOptionCreateSerializer(data=choice)
            serializer.is_valid(raise_exception=True)
            choices.append(serializer.data)
        return choices

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        question = ChoiceQuestion.objects.create(**validated_data)
        for choice in choices:
            ChoiceAnswerOption.objects.create(**choice, question=question)
        return question


class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()

    class Meta:
        model = MultipleChoiceQuestion
        fields = ('pk', 'name', 'question_type', 'choices',)

    def get_choices(self, obj):
        return MultipleChoiceAnswerOptionSerializer(
            obj.answer_options.all(), many=True).data

    def validate(self, obj):
        data = super().validate(obj)
        data['choices'] = self.validate_choices(self.initial_data['choices'])
        return data

    def validate_choices(self, value):
        choices = []
        for choice in value:
            serializer = MultipleChoiceAnswerOptionCreateSerializer(data=choice)
            serializer.is_valid(raise_exception=True)
            choices.append(serializer.data)
        return choices

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        question = MultipleChoiceQuestion.objects.create(**validated_data)
        for choice in choices:
            MultipleChoiceAnswerOption.objects.create(**choice, question=question)
        return question


class TextQuestionWithAnswerSerializer(serializers.Serializer):
    answer = TextAnswerSerializer()
    question = TextQuestionSerializer()

    class Meta:
        fields = ('question', 'answer')


class ChoiceQuestionWithAnswerSerializer(serializers.Serializer):
    answer = ChoiceAnswerOptionSerializer()
    question = ChoiceQuestionSerializer()

    class Meta:
        fields = ('question', 'answer')


class MultipleChoiceQuestionWithAnswerSerializer(serializers.Serializer):
    answer = MultipleChoiceAnswerOptionSerializer(many=True)
    question = ChoiceQuestionSerializer()

    class Meta:
        fields = ('question', 'answer')
