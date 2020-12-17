from rest_framework import serializers

from surveys.models import ChoiceAnswerOption, MultipleChoiceAnswerOption


class ChoiceAnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceAnswerOption
        fields = ('pk', 'text',)
        extra_kwargs = {'pk': {'read_only': False}}


class MultipleChoiceAnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceAnswerOption
        fields = ('pk', 'text',)
        extra_kwargs = {'pk': {'read_only': False}}


class ChoiceAnswerOptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceAnswerOption
        fields = ('text',)


class MultipleChoiceAnswerOptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceAnswerOption
        fields = ('text',)
