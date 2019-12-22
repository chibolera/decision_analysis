from django.shortcuts import render
from .models import AgentsLog, Budget, RateList, AgentsState
from .serializers import BudgetSerializer, AgentsSerializer, RateSerializer, StateSerializer
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from django.conf import settings
from .consumers import send_to_ws, send_to_front

class LogList(ListAPIView):
    serializer_class = AgentsSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self, *args, **kwargs):
        qs = AgentsLog.objects.all()

        return qs

class MainFunctional(GenericViewSet):

    serializer_class = AgentsSerializer
    permission_classes = (AllowAny, )
    queryset = RateList.objects.all()[300:660]

    def create(self, request):
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            day = data['day']
            test_case = data['test_case']
            if AgentsLog.objects.filter(day=day, test_case=test_case, name=data['name']).count() == 0:
                serializer.save()
                count = AgentsLog.objects.filter(day=day, test_case=test_case).count()
                if  count == 3:
                    rate = RateList.objects.get(id=360+int(day))
                    rate_serializer = RateSerializer(rate)
                    agents = AgentsLog.objects.filter(day=day, test_case=test_case).order_by('name')
                    agents.update(real_price = rate.usd)
                    for agent in agents:
                        if not data['from_government']:
                            if agent.status == 'buy':
                                send_to_ws(rate_serializer, agent.name, from_government=False, buy=True, seller=agent)
                            else:
                                send_to_ws(rate_serializer, agent.name, from_government=False)
                        else:
                            send_to_ws(rate_serializer, agent.name)
                    send_to_front(self.serializer_class(agents, many=True))
                return Response(serializer.data)
            else:
                return Response({'message':'already_exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request):
        excel_path = settings.MEDIA_ROOT + '/usd.xlsx'
        df = pd.read_excel(excel_path)
        for usd in df['USD'].values:
            RateList.objects.create(usd=usd)

        return Response({'message':'OK'})

    def get_rate(self, request, page):

        if page > 1:
            rate = RateList.objects.get(id=179+int(page))
            serializer = RateSerializer(rate)
            return Response(serializer.data)
        else:
            serializer = RateSerializer(self.queryset, many=True)
            return Response(serializer.data)


class AgentStateViewSet(GenericViewSet):

    serializer_class = StateSerializer
    permission_classes = (AllowAny, )

    def create(self, request):
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            day = data['day']
            test_case = data['test_case']
            states = AgentsState.objects.filter(day=day, test_case=test_case)
            if  states.count() == 3:
                for agent in states:
                    other_states = states.exclude(name=agent.name)
                    send_to_ws(self.serializer_class(other_states, many=True), agent.name, from_government=False)
                # send_to_front(self.serializer_class(agents, many=True))
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)