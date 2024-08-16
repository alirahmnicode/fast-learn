from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.forms import BaseModelForm
from django.views.generic import CreateView, DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from .forms import CourseEnrollForm

from courses.models import Course


class StudentRegistrationView(CreateView):
    template_name = "students/student/registration.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("students:student_course_list")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd["username"], password=cd["password1"])
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form) -> HttpResponse:
        self.course = form.cleaned_data["course"]
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("students:student_course_detail", args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "students/course/list.html"

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "students/course/detail.html"

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()

        if "module_id" in self.kwargs:
            # get current module
            context["module"] = course.modules.get(id=self.kwargs["module_id"])
        else:
            # get first module
            context["module"] = course.modules.all()[0]
        return context
