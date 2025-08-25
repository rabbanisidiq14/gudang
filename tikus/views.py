from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AlertTikus

# Create your views here.
class AlertAPI(APIView):
    def post(self, request):
        pesan = request.data.get("pesan", "Tikus terdeteksi")
        AlertTikus.objects.create(pesan=pesan)
        return Response({"status": "Alert diterima", "pesan": pesan})
