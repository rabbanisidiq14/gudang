from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class PrediksiAPI(APIView):
    def post(self, request):
        suhu = float(request.data.get("suhu", 25))
        kelembapan = float(request.data.get("kelembapan", 60))

        if suhu > 30:
            umur = 5
        elif kelembapan > 80:
            umur = 7
        else:
            umur = 10

        return Response({"prediksi_umur_simpan": f"{umur} hari"})
