from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import Subject,Note
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import SubjectForm, NoteForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def loginPage(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                return redirect('home')
        except :
            messages.error(request, "Cridential does not match")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Cridential does not match")
    context = {
        'page':page
    }
    return render(request, "Noteapp/signin_signup.html", context)
def signupPage(request):
    page = 'signup'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request, "An error occured durring registration")
    context = {
        'form':form,
        'page':page
    }
    return render(request, "Noteapp/signin_signup.html", context)

def logoutUser(request):
    logout(request)
    return redirect("login")

@login_required(login_url='login')
def home(request):
    print(request.user)
    q = request.GET.get("q") if request.GET.get("q") != None else ''
    subjects = Subject.objects.filter(user=request.user)
    print(subjects)
    Notes = Note.objects.filter(
        Q(user=request.user) & (
            Q(title__icontains=q)|
            Q(subject__name__icontains=q)  
        )                          
    )
    
    context = {
        'subjects':subjects,
        'notes':Notes
    }
    return render(request, "Noteapp/home.html", context)
def addSubject(request):
    form = SubjectForm()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('home')
    context = {
        'form':form,
    }
    return render(request, 'Noteapp/note_subject.html',context)

def deleteSubject(request,pk):
    subject = Subject.objects.get(id=pk)
    if request.method == "POST":
        subject.delete()
        return redirect("home")
    context = {
        "note":subject
    }
    return render(request, "Noteapp/deleteNote.html", context)

def createNote(request):
    form = NoteForm()
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('home')
    context = {

        'form':form,
    }
    return render(request, "Noteapp/note_subject.html", context)
def note(request,pk):
    subjects = Subject.objects.filter(user=request.user)
    note = Note.objects.get(id=pk)
    context = {
        "note":note,
        'subjects':subjects,
    }
    return render(request, "Noteapp/note.html",context)
def subject(request,pk):
    subjects = Subject.objects.filter(user=request.user)
    subject = Subject.objects.get(id=pk)
    notes = Note.objects.filter(subject=subject )
    context = {
        'subjects':subjects,
        "notes":notes,
        'subject':subject,
    }
    return render(request, "Noteapp/subject.html",context)

def createSubjectNote(request,subj):
    subject = Subject.objects.get(name=subj)
    if request.method == 'POST':
        if request.POST.get("title") != '':
            subject.note_set.create(
                title = request.POST.get("title"),
                subject = subj,
                note = request.POST.get("note"),
                user = request.user
            )
            return redirect("home")
    context = {

    }
    return render(request, "Noteapp/subject_note.html", context)

def deleteNote(request,pk):
    note = Note.objects.get(id=pk)
    if request.method == "POST":
        note.delete()
        return redirect("home")
    context = {
        "note":note
    }
    return render(request, "Noteapp/deleteNote.html", context)

def editNote(request,pk):
    note = Note.objects.get(id=pk)
    form = NoteForm(instance=note)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
        return redirect("home")
    context = {
        "form":form
    }
    return render(request, "Noteapp/note_subject.html", context)