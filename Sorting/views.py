from django.shortcuts import render, redirect
from .forms import MyForm

# Create your views here.
def my_view(request):
    context = {
        "title": "Mein Tiel",
        "Inhalt": "Das ist irgendwas",
    }
    return render(request, "home.html", context)

def form_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            return redirect("success_url")
    else:
        form =MyForm()
    return render(request, 'form_template.html', {'form': form})