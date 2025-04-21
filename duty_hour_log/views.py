# duty_hour_log/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import DutyHourLog
from .forms import DutyHourLogForm
from datetime import date # <--- Import date

# Optional: If you want success messages
# from django.contrib import messages

# List View (Read - All) & Create View Combined
def log_list(request):
    # Handle form submission (POST request)
    if request.method == 'POST':
        form = DutyHourLogForm(request.POST)
        if form.is_valid():
            form.save()
            # Optional: Add a success message
            # messages.success(request, 'Duty hour log created successfully!')
            # Redirect back to the SAME view (log_list) to show the updated list
            # and prevent form resubmission on refresh (Post/Redirect/Get pattern)
            return redirect('log_list')
        # If form is invalid, the request proceeds to the GET section below,
        # and the 'form' variable containing errors will be passed to the template.
        # *** NOTE: We DON'T set initial data here, to preserve user input on error ***
    else: # Handle initial page load (GET request)
        # --- MODIFIED LINE ---
        # Create a form instance with the 'date' field pre-filled with today's date
        form = DutyHourLogForm(initial={'date': date.today()})
        # --- END MODIFICATION ---

    # Fetch all logs for display (always needed, for GET or POST)
    logs = DutyHourLog.objects.all().order_by('-date', '-start_time') # Added ordering for consistency

    context = {
        'logs': logs,
        'form': form, # Pass the form (empty/initial or with errors) to the template
    }
    return render(request, 'duty_hour_log/log_list.html', context)

# Detail View (Read - One) - NO CHANGES NEEDED
def log_detail(request, pk):
    log = get_object_or_404(DutyHourLog, pk=pk)
    context = {'log': log}
    return render(request, 'duty_hour_log/log_detail.html', context)

# Update View - NO CHANGES NEEDED
def log_update(request, pk):
    log_instance = get_object_or_404(DutyHourLog, pk=pk)
    if request.method == 'POST':
        form = DutyHourLogForm(request.POST, instance=log_instance)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Duty hour log updated successfully!')
            return redirect('log_detail', pk=log_instance.pk) # Redirect to detail view
    else: # GET request
        form = DutyHourLogForm(instance=log_instance) # No initial date needed here, uses instance data

    # Use the existing log_form.html template, but provide a different title
    context = {'form': form, 'log_instance': log_instance, 'form_title': 'Edit Duty Log'}
    return render(request, 'duty_hour_log/log_form.html', context)

# Delete View - NO CHANGES NEEDED
def log_delete(request, pk):
    log_instance = get_object_or_404(DutyHourLog, pk=pk)
    if request.method == 'POST':
        log_instance.delete()
        # messages.success(request, 'Duty hour log deleted successfully!')
        return redirect('log_list') # Redirect to list view after deletion

    context = {'log': log_instance}
    return render(request, 'duty_hour_log/log_confirm_delete.html', context)