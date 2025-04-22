# duty_hour_log/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import DutyHourLog, Initial

class DutyHourLogForm(forms.ModelForm):
    # ... (other fields like initial, ojti, examiner, trainee remain the same) ...
    initial = forms.ModelChoiceField(
        queryset=Initial.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}), # Smaller select for table
        label="Initial", # Shorter label
        required=False # Base requirement is False, validated in clean()
    )
    ojti = forms.ModelChoiceField(
        queryset=Initial.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        label="OJTI"
    )
    examiner = forms.ModelChoiceField(
        queryset=Initial.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        label="Examiner"
    )
    trainee = forms.ModelChoiceField(
        queryset=Initial.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        label="Trainee"
    )

    # Explicitly define finish_time to make it not required by the form
    finish_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control form-control-sm'}),
        required=False, # <<< MAKE FORM FIELD NOT REQUIRED
        label="Finish" # Short label
    )

    class Meta:
        model = DutyHourLog
        fields = [
            'op', 'date', 'start_time', 'finish_time', 'rating',
            'initial', 'ojti', 'examiner', 'trainee',
            'remarks'
        ]
        widgets = {
            # Define widgets for fields not explicitly declared above
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control form-control-sm'}),
            # 'finish_time' widget is defined above
            'op': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'rating': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'remarks': forms.Textarea(attrs={'rows': 1, 'class': 'form-control form-control-sm'}),
        }
        labels = {
            'op': 'Op',
            'start_time': 'Start',
            # 'finish_time' label defined above
            'rating': 'Rating',
            'initial': 'Initial',
            'trainee': 'Trainee',
            'ojti': 'OJTI',
            'examiner': 'Examiner',
        }

    def clean(self):
        cleaned_data = super().clean()
        op = cleaned_data.get('op')
        initial = cleaned_data.get('initial')
        ojti = cleaned_data.get('ojti')
        examiner = cleaned_data.get('examiner')
        trainee = cleaned_data.get('trainee')
        start_time = cleaned_data.get('start_time')
        finish_time = cleaned_data.get('finish_time') # Now might be None

        # --- Conditional Validation (based on op) ---
        # (This logic remains the same)
        if op == 'Solo':
            if not initial:
                self.add_error('initial', 'Initial is required for Solo operation.')
            if ojti: self.add_error('ojti', 'OJTI should not be selected for Solo.')
            if examiner: self.add_error('examiner', 'Examiner should not be selected for Solo.')
            if trainee: self.add_error('trainee', 'Trainee should not be selected for Solo.')
        elif op == 'OJT':
            if not ojti: self.add_error('ojti', 'OJTI is required for OJT operation.')
            if not trainee: self.add_error('trainee', 'Trainee is required for OJT operation.')
            if initial: self.add_error('initial', 'Initial should not be selected for OJT.')
            if examiner: self.add_error('examiner', 'Examiner should not be selected for OJT.')
        elif op == 'Assessment':
            # OJTI might be optional or required depending on exact workflow
            # if not ojti: self.add_error('ojti', 'OJTI is required for Assessment.')
            if not examiner: self.add_error('examiner', 'Examiner is required for Assessment.')
            if not trainee: self.add_error('trainee', 'Trainee/ATCO is required for Assessment.')
            if initial: self.add_error('initial', 'Initial should not be selected for Assessment.')
        elif not op:
             self.add_error('op', 'Operation Type is required.')

        # --- Time Validation (adjusted for optional finish_time) ---
        # Only validate if *both* start_time and finish_time are present
        if start_time and finish_time and start_time >= finish_time:
            self.add_error('finish_time', 'Finish time must be after start time.')

        # --- Ensure required base fields are present (Django usually handles this, but belt-and-suspenders) ---
        if not op: self.add_error('op', 'Operation Type cannot be empty.')
        if not cleaned_data.get('date'): self.add_error('date', 'Date cannot be empty.')
        if not start_time: self.add_error('start_time', 'Start Time cannot be empty.')
        if not cleaned_data.get('rating'): self.add_error('rating', 'Rating cannot be empty.')


        return cleaned_data