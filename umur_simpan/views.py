from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import PrediksiForm, ProdukForm
from .models import PrediksiUmurSimpan, Produk

# Halaman input + riwayat prediksi
def halaman_prediksi(request):
    if request.method == "POST":
        form = PrediksiForm(request.POST)
        if form.is_valid():
            umur_hari, aw = form.bersihkan_dan_hitung()
            # simpan
            instance: PrediksiUmurSimpan = form.save(commit=False)
            instance.umur_hari = umur_hari
            instance.aw = aw
            instance.save()
            messages.success(
                request,
                f"Prediksi tersimpan: umur simpan ≈ {umur_hari} hari, aw = {aw:.2f}",
            )
            return redirect(reverse("halaman_prediksi"))
    else:
        form = PrediksiForm()

    riwayat = PrediksiUmurSimpan.objects.select_related("produk").order_by("-dibuat")[:20]
    return render(request, "umur_simpan/prediksi.html", {"form": form, "riwayat": riwayat})


# ===== CRUD Produk =====

class ProdukListView(ListView):
    model = Produk
    template_name = "umur_simpan/produk_list.html"
    context_object_name = "produk_list"
    paginate_by = 20
    ordering = ["-dibuat"]


class ProdukCreateView(CreateView):
    model = Produk
    form_class = ProdukForm
    template_name = "umur_simpan/produk_form.html"

    def get_success_url(self):
        messages.success(self.request, "Produk berhasil ditambahkan.")
        return reverse("produk_list")


class ProdukUpdateView(UpdateView):
    model = Produk
    form_class = ProdukForm
    template_name = "umur_simpan/produk_form.html"

    def get_success_url(self):
        messages.success(self.request, "Produk berhasil diperbarui.")
        return reverse("produk_list")


class ProdukDeleteView(DeleteView):
    model = Produk
    template_name = "umur_simpan/produk_confirm_delete.html"
    success_url = reverse_lazy("produk_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Produk berhasil dihapus.")
        return super().delete(request, *args, **kwargs)
