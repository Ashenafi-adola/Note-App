from django.urls import path
from .import views
urlpatterns = [
    path("", views.loginPage, name="login"),
    path("signup/", views.signupPage, name="signup"),
    path("logout/", views.logoutUser, name="logoutUser"),
    path("home/", views.home, name="home"),
    path("addsubject/", views.addSubject, name="addsubject"),
    path("createNote/", views.createNote, name="createNote"),
    path("deleteNote/<int:pk>", views.deleteNote, name="deleteNote"),
    path("deleteSubject/<int:pk>", views.deleteSubject, name="deleteSubject"),
    path("editNote/<int:pk>", views.editNote, name="editNote"),
    path("createSubjectNote/<str:subj>", views.createSubjectNote, name="createSubjectNote"),

    path("note/<int:pk>", views.note, name="note"),
    path("subject/<int:pk>", views.subject, name="subject"),
]