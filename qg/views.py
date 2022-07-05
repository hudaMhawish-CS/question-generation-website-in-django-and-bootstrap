from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .QG import QG
from .models import NewUser
from .form import NewUserForm
# Create your views here.
def home_qg(request):

    return render(request,'qg/home_qg.html')

def references(request):

    return render(request,'qg/references.html')

def FAQ (request):

    return render (request, 'qg/FAQ.html')

def contact (request):

    return render (request, 'qg/contact.html')

def users (request):
    # board = get_object_or_404(Board, pk=board_id)
    # user = User.objects.first()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.save()
    else:
        form = NewUserForm()
    return render(request, 'qg/users.html', {'form': form})

def start (request):
    phase = ""
    if request.method=='POST':
        phase = request.POST.get("text",None)
    list_question = QG().sum(phase)
    context = {
        "list_question" : list_question,
        "phase": phase
    }
    return render (request, 'qg/start.html', context)