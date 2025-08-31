from django.urls import path
from .views import (
    halaman_prediksi,
    ProdukListView, ProdukCreateView, ProdukUpdateView, ProdukDeleteView
)

urlpatterns = [
    # Halaman prediksi (input user)
    path("prediksi/", halaman_prediksi, name="halaman_prediksi"),

    # CRUD Produk
    path("produk/", ProdukListView.as_view(), name="produk_list"),
    path("produk/tambah/", ProdukCreateView.as_view(), name="produk_tambah"),
    path("produk/<int:pk>/ubah/", ProdukUpdateView.as_view(), name="produk_ubah"),
    path("produk/<int:pk>/hapus/", ProdukDeleteView.as_view(), name="produk_hapus"),
]
