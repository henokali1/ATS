# duty_hour_log/forms.py
from django import forms
from .models import DutyHourLog, Initial

class DutyHourLogForm(forms.ModelForm):
    initial = forms.ModelChoiceField(
        queryset=Initial.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}), # Use form-select
        label="Initial (Controller)",
        required=False
    )
    ojti = forms.ModelChoiceField(
        queryset=Initial.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}), # Use form-select
        label="OJTI"
    )
    examiner = forms.ModelChoiceField(
        queryset=Initial.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}), # Use form-select
        label="Examiner"
    )
    trainee = forms.ModelChoiceField(
        queryset=Initial.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}), # Use form-select
        label="Trainee"
    )

    class Meta:
        model = DutyHourLog
        fields = [
            'op', 'date', 'start_time', 'finish_time', 'rating',
            'initial', 'ojti', 'examiner', 'trainee',
            'remarks'
        ]
        widgets = {
            # Add 'form-control' or 'form-select' to all widgets
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'finish_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'op': forms.Select(attrs={'class': 'form-select'}), # Use form-select
            'rating': forms.Select(attrs={'class': 'form-select'}), # Use form-select
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'op': 'Operation Type',
            'start_time': 'Start',
            'finish_time': 'Finish',
        }
        # Help texts are now added directly in the template for better control
        # help_texts = { ... } # Can remove this if handled in template