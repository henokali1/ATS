# duty_hour_log/forms.py
from django import forms
from .models import DutyHourLog, Initial

class DutyHourLogForm(forms.ModelForm):
    initial = forms.ModelChoiceField(
        queryset=Initial.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Initial (Controller)",
        required=False # Make optional in the form as it will be hidden
    )
    ojti = forms.ModelChoiceField(
        queryset=Initial.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="OJTI"
    )
    examiner = forms.ModelChoiceField(
        queryset=Initial.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Examiner/Assessor"
    )
    trainee = forms.ModelChoiceField( # NEW FIELD
        queryset=Initial.objects.filter(is_active=True),
        required=False, # Make optional
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Trainee"
    )

    class Meta:
        model = DutyHourLog
        fields = [
            'op', 'date', 'start_time', 'finish_time', 'rating',
            'initial', 'ojti', 'examiner', 'trainee', # Added trainee
            'remarks'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'finish_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'op': forms.Select(attrs={'class': 'form-control'}), # id will be 'id_op'
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'op': 'Operation Type',
            'start_time': 'Start',
            'finish_time': 'Finish',
        }
        help_texts = {
            'initial': 'Select for Solo operations.',
            'ojti': 'Select for OJT operations.',
            'examiner': 'Select for Assessment operations.',
            'trainee': 'Select for OJT or Assessment operations.',
        }