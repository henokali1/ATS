# duty_hour_log/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import DutyHourLog
from .forms import DutyHourLogForm
from datetime import date
from django.core.paginator import Paginator
from django.contrib import messages

# List View (Read - All) & Create View Combined
def log_list(request):
    print("--- Entering log_list view ---") # DEBUG

    if request.method == 'POST':
        print("--- Handling POST request ---") # DEBUG
        form = DutyHourLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_list')
        else:
            # If form is invalid on POST, we still need pagination for the list below
            print("--- POST form invalid ---") # DEBUG
            pass # Let execution continue to pagination logic
    else: # GET request
        print("--- Handling GET request ---") # DEBUG
        form = DutyHourLogForm(initial={'date': date.today()})

    # --- Pagination Logic ---
    page_obj = None # Initialize page_obj to None
    try:
        log_list_all = DutyHourLog.objects.all().order_by('-date', '-start_time')       
        paginator = Paginator(log_list_all, 10) # Show 10 logs per page.

        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number) # Get the Page object for that number


    except Exception as e:
        # Log any unexpected errors during pagination
        print(f"--- ERROR during pagination setup: {e} ---") # DEBUG

    context = {
        'page_obj': page_obj, # Pass the potentially None or valid page_obj
        'form': form,
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