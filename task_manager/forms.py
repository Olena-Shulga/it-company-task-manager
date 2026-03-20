from datetime import date
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Task, TaskType


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


class WorkerForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position"
        )
