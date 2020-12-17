from rest_framework import serializers

from surveys.enums import QuestionTypes
from surveys.models import (
    ChoiceAnswer,
    ChoiceAnswerOption,
    ChoiceQuestion,
    MultipleChoiceAnswer,
    MultipleChoiceQuestion,
    Survey,
    TextAnswer,
    TextQuestion,
)
from surveys.serializers.answer import (
    ChoiceQuestionResponseSerializer,
    MultipleChoiceQuestionResponseSerializer,
    TextQuestionResponseSerializer,
)
from surveys.serializers.question import (
    ChoiceQuestionSerializer,
    ChoiceQuestionWithAnswerSerializer,
    MultipleChoiceQuestionSerializer,
    MultipleChoiceQuestionWithAnswerSerializer,
    TextQuestionSerializer,
    TextQuestionWithAnswerSerializer,
)


class SurveySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = ('pk', 'name', 'start_date', 'end_date', 'description', 'questions',)

    def get_questions(self, obj):
        text_questions = obj.textquestion_set.all()
        choice_questions = obj.choicequestion_set.all()
        multiple_choice_questions = obj.multiplechoicequestion_set.all()

        return [
            *TextQuestionSerializer(text_questions, many=True).data,
            *ChoiceQuestionSerializer(choice_questions, many=True).data,
            *MultipleChoiceQuestionSerializer(multiple_choice_questions, many=True).data,
        ]


class AnsweredSurveySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = ('pk', 'name', 'start_date', 'end_date', 'description', 'questions',)

    def get_questions(self, obj):
        user_id = self.context.get('user_id')
        text_questions = obj.textquestion_set.all()
        choice_questions = obj.choicequestion_set.all()
        multiple_choice_questions = obj.multiplechoicequestion_set.all()

        text_questions_with_answers = self.__get_questions_with_answers(text_questions, user_id)
        choice_questions_with_answers = self.__get_questions_with_answers(choice_questions, user_id)
        multiple_choice_questions_with_answers = self.__get_questions_with_answers(multiple_choice_questions, user_id)

        return [
            *TextQuestionWithAnswerSerializer(
                text_questions_with_answers, many=True).data,
            *ChoiceQuestionWithAnswerSerializer(
                choice_questions_with_answers, many=True).data,
            *MultipleChoiceQuestionWithAnswerSerializer(
                multiple_choice_questions_with_answers, many=True).data,
        ]

    def __get_questions_with_answers(self, questions, user_id):
        questions_with_answers = []
        for question in questions:
            answer_model = {
                QuestionTypes.TEXT.value: TextAnswer,
                QuestionTypes.CHOICE.value: ChoiceAnswer,
                QuestionTypes.MULTIPLE_CHOICE.value: MultipleChoiceAnswer,
            }.get(question.question_type)
            answer = answer_model.objects.filter(user_id=user_id, question=question).first()

            data = {"question": question}
            if question.question_type == QuestionTypes.TEXT.value:
                data.update({"answer": answer})
            elif question.question_type == QuestionTypes.CHOICE.value:
                data.update({"answer": answer.choice})
            elif question.question_type == QuestionTypes.MULTIPLE_CHOICE.value:
                data.update({"answer": answer.choices})

            questions_with_answers.append(data)
        return questions_with_answers


class SurveyResponseSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(min_value=1)

    class Meta:
        model = Survey
        fields = ('pk', 'answers', 'user_id',)

    def validate(self, data):
        data = self.initial_data
        data['answers'] = self.validate_answers(data['answers'])
        return data

    def validate_answers(self, data):
        text_questions = []
        choice_questions = []
        multiple_choice_questions = []

        for answer in data:
            question_list = {
                QuestionTypes.TEXT.name: text_questions,
                QuestionTypes.CHOICE.name: choice_questions,
                QuestionTypes.MULTIPLE_CHOICE.name: multiple_choice_questions,
            }.get(answer['question_type'])

            if question_list is None:
                raise serializers.ValidationError("Unsupported question type")

            question_list.append(answer)

        text_questions = TextQuestionResponseSerializer(
            data=text_questions, many=True)
        choice_questions = ChoiceQuestionResponseSerializer(
            data=choice_questions, many=True)
        multiple_choice_questions = MultipleChoiceQuestionResponseSerializer(
            data=multiple_choice_questions, many=True)

        text_questions.is_valid(raise_exception=True)
        choice_questions.is_valid(raise_exception=True)
        multiple_choice_questions.is_valid(raise_exception=True)

        data = [
            *text_questions.validated_data,
            *choice_questions.validated_data,
            *multiple_choice_questions.validated_data,
        ]
        return data

    def save(self):
        user_id = self.validated_data['user_id']
        answers = self.validated_data['answers']

        for answer in answers:
            question_model, answer_model = {
                QuestionTypes.TEXT.name: (TextQuestion, TextAnswer),
                QuestionTypes.CHOICE.name: (ChoiceQuestion, ChoiceAnswer),
                QuestionTypes.MULTIPLE_CHOICE.name: (MultipleChoiceQuestion, MultipleChoiceAnswer),
            }.get(answer['question_type'])

            question = question_model.objects.get(pk=answer['pk'])

            if question.question_type == QuestionTypes.TEXT.value:
                answer = {
                    **answer['answer'],
                    'user_id': user_id,
                    'question': question,
                }
            elif question.question_type == QuestionTypes.CHOICE.value:
                answer = {
                    'choice': ChoiceAnswerOption.objects.get(**answer['answer']),
                    'user_id': user_id,
                    'question': question,
                }
            elif question.question_type == QuestionTypes.MULTIPLE_CHOICE.value:
                answer = {
                    'choices': [ChoiceAnswerOption.objects.get(**a) for a in answer['answer']],
                    'user_id': user_id,
                    'question': question,
                }

        return answer_model.objects.create(**answer)
