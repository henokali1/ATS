# duty_hour_log/models.py
from django.db import models
from django.contrib.auth.models import User

class Initial(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text="Unique code/identifier for the Initial (e.g., 'JDS')")
    full_name = models.CharField(max_length=100, blank=True, null=True, help_text="Optional full name associated with the initial")
    is_active = models.BooleanField(default=True, help_text="Mark if this initial is currently active")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Initial"
        verbose_name_plural = "Initials"
        ordering = ['code']

class DutyHourLog(models.Model):
    OP_CHOICES = [
        ('', '---------'), # Add a blank choice
        ('Solo', 'Solo'),
        ('OJT', 'OJT'),
        ('Assessment', 'Assessment'),
    ]
    RATING_CHOICES = [
        ('ADC', 'Aerodrome Control (ADC)'),
        ('APP', 'Approach Control Procedural (APP)'),
        ('APS', 'Approach Control Surveillance (APS)'),
        ('ATCA', 'Area Control Procedural (ATCA)'),
    ]

    op = models.CharField(
        max_length=20,
        choices=OP_CHOICES,
        verbose_name="Operation Type"
    )
    date = models.DateField()
    start_time = models.TimeField(verbose_name="Start Time")
    finish_time = models.TimeField(verbose_name="Finish Time")
    rating = models.CharField(
        max_length=10,
        choices=RATING_CHOICES
    )
    initial = models.ForeignKey(
        Initial,
        on_delete=models.PROTECT,
        verbose_name="Initial (Controller)", # For Solo operations
        related_name='duty_logs_as_primary',
        null=True, # Made optional
        blank=True  # Made optional
    )
    ojti = models.ForeignKey(
        Initial,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="OJTI",
        related_name='duty_logs_as_ojti',
        help_text="Select for OJT operations."
    )
    examiner = models.ForeignKey(
        Initial,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Examiner/Assessor",
        related_name='duty_logs_as_examiner',
        help_text="Select for Assessment operations."
    )
    trainee = models.ForeignKey( # NEW FIELD
        Initial,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Trainee",
        related_name='duty_logs_as_trainee',
        help_text="Select for OJT or Assessment operations."
    )
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        person_str = ""
        if self.op == 'Solo' and self.initial:
            person_str = f"Initial: {self.initial.code}"
        elif self.op == 'OJT' and self.trainee:
            person_str = f"Trainee: {self.trainee.code}"
            if self.ojti:
                person_str += f", OJTI: {self.ojti.code}"
        elif self.op == 'Assessment' and self.trainee:
            person_str = f"Trainee: {self.trainee.code}"
            if self.examiner:
                person_str += f", Examiner: {self.examiner.code}"
        else: # Fallback or if fields are not set as expected
            if self.initial: person_str += f"I: {self.initial.code} "
            if self.trainee: person_str += f"T: {self.trainee.code} "
            if self.ojti: person_str += f"O: {self.ojti.code} "
            if self.examiner: person_str += f"E: {self.examiner.code} "


        return f"{self.date} - {self.op} - {person_str.strip()} ({self.start_time} - {self.finish_time})"

    class Meta:
        ordering = ['-date', '-start_time']
        verbose_name = "Duty Hour Log"
        verbose_name_plural = "Duty Hour Logs"