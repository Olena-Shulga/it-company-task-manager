from datetime import date
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Task, TaskType, Position


def validate_deadline(value):
    today = date.today()
    if value < today:
        raise forms.ValidationError("Deadline date cannot be in the past.")
    return value

class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    task_type = forms.ModelChoiceField(queryset=TaskType.objects.all(),widget=forms.RadioSelect)

    class Meta:
        model = Task
        fields = "__all__"

    def clean_deadline(self):
        return validate_deadline(self.cleaned_data["deadline"])


class TaskSearchForm(forms.Form):
    name = forms.CharField(
            max_length=255,
            required=False,
            label="",
            widget=forms.TextInput(
                attrs={"placeholder": "Search by name"}
            )
        )
    priority = forms.ChoiceField(
        choices=(
            ("", "----------"),
            ("U", "Urgent"),
            ("H", "High"),
            ("M", "Medium"),
            ("L", "Low"),
        ),
        required=False,
        label="Priority",
        widget=forms.Select,
    )
    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        required=False,
        widget=forms.Select,
    )


class WorkerForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position"
        )


class WorkerUpdateForm(forms.ModelForm):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    position = forms.ModelChoiceField(queryset=Position.objects.all(), widget=forms.RadioSelect)

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "first_name",
            "last_name",
            "position",
        ]

    template_name = "task_manager/worker_form.html"


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
            max_length=255,
            required=False,
            label="",
            widget=forms.TextInput(
                attrs={"placeholder": "Search by username"}
            )
        )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        label="Position:",
        widget=forms.Select,
    )


class SearchForm(forms.Form):
    name = forms.CharField(
            max_length=255,
            required=False,
            label="",
            widget=forms.TextInput(
                attrs={"placeholder": "Search by name"}
            )
        )
