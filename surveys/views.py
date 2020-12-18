from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from surveys.enums import QuestionTypes
from surveys.models import Survey
from surveys.serializers.question import (
    ChoiceQuestionSerializer,
    MultipleChoiceQuestionSerializer,
    TextQuestionSerializer,
)
from surveys.serializers.survey import (
    AnsweredSurveySerializer,
    SurveyResponseSerializer,
    SurveySerializer,
)


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, pk):
        print(request.data)
        return Response(status=status.HTTP_201_CREATED)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        survey = serializer.save()
        self.__create_questions(request.data['questions'], survey)
        return Response(
            self.serializer_class(survey).data,
            status=status.HTTP_201_CREATED
        )

    def __create_questions(self, questions, survey):
        for question in questions:
            question_serializer = {
                QuestionTypes.TEXT.name: TextQuestionSerializer,
                QuestionTypes.CHOICE.name: ChoiceQuestionSerializer,
                QuestionTypes.MULTIPLE_CHOICE.name: MultipleChoiceQuestionSerializer,
            }.get(question['question_type'])

            serializer = question_serializer(data=question)
            serializer.is_valid(raise_exception=True)
            serializer.save(survey=survey)


class ClientViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def retrieve(self, request, **kwargs):
        serializer_class = self.serializer_class
        user_id = request.query_params.get('user_id', -1)
        obj = self.get_object()
        if obj.is_already_answered(user_id):
            serializer_class = AnsweredSurveySerializer

        serializer = serializer_class(obj, context={'user_id': user_id})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def response(self, request, **kwargs):
        obj = self.get_object()
        user_id = request.query_params.get('user_id')
        if user_id is None:
            return Response("user_id mast be in query parameters", status=status.HTTP_400_BAD_REQUEST)
        data = {
            **request.data,
            'pk': obj.pk,
            'user_id': user_id,
        }
        serializer = SurveyResponseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        survey = serializer.save()

        serializer = AnsweredSurveySerializer(survey, context={'user_id': user_id})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False)
    def completed_list(self, request):
        user_id = request.query_params.get('user_id')
        queryset = list(filter(lambda x: x.is_already_answered(user_id), self.queryset))
        serializer = AnsweredSurveySerializer(queryset, context={'user_id': user_id}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
