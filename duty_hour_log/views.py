# duty_hour_log/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import DutyHourLog, Initial # Import Initial
from .forms import DutyHourLogForm
from datetime import date
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse # For AJAX view
from django.views.decorators.http import require_POST # To ensure POST for save
from django.template.loader import render_to_string # To render the static row
import json # To parse request body
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_time

# List View (Read - All) - Modified for Inline Add
def log_list(request):
    # GET Request only for displaying the list and the add button
    log_list_all = DutyHourLog.objects.all().order_by('-date', '-start_time')
    paginator = Paginator(log_list_all, 10) # Show 10 logs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare data needed for the JS template row
    active_initials = list(Initial.objects.filter(is_active=True).values('id', 'code'))
    op_choices = [{'value': c[0], 'display': c[1]} for c in DutyHourLog.OP_CHOICES]
    rating_choices = [{'value': c[0], 'display': c[1]} for c in DutyHourLog.RATING_CHOICES]

    context = {
        'page_obj': page_obj,
        'active_initials_json': json.dumps(active_initials), # Pass initials as JSON
        'op_choices_json': json.dumps(op_choices), # Pass choices as JSON
        'rating_choices_json': json.dumps(rating_choices), # Pass choices as JSON
        'today_date': date.today().isoformat(), # Default date for new row
    }
    return render(request, 'duty_hour_log/log_list_inline.html', context) # Use a new template name

# New View to Save Inline Log Entry via AJAX
@require_POST # Ensures this view only accepts POST requests
def save_inline_log(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'errors': {'__all__': ['Invalid request format.']}}, status=400)

    # Instantiate the form with the received data
    form = DutyHourLogForm(data)

    if form.is_valid():
        try:
            new_log = form.save()
            # Render the static row HTML to send back to the client
            row_html = render_to_string(
                'duty_hour_log/partials/log_table_row_static.html', # A new partial template
                {'log': new_log}
            )
            return JsonResponse({
                'status': 'success',
                'new_row_html': row_html,
                'log_id': new_log.pk # Send back the ID if needed
            })
        except Exception as e:
            # Catch potential database errors during save
            return JsonResponse({'status': 'error', 'errors': {'__all__': [f'Error saving log: {e}']}}, status=500)
    else:
        # Form is invalid, return errors
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


# Detail View (Read - One) - NO CHANGES NEEDED
def log_detail(request, pk):
    log = get_object_or_404(DutyHourLog, pk=pk)
    # Link to the detail page is less critical if editing happens elsewhere, but keep it for now
    # Maybe add links from the static table row later if needed
    context = {'log': log}
    return render(request, 'duty_hour_log/log_detail.html', context)


# Update View - Keep for editing existing records via separate page
def log_update(request, pk):
    log_instance = get_object_or_404(DutyHourLog, pk=pk)
    if request.method == 'POST':
        form = DutyHourLogForm(request.POST, instance=log_instance)
        if form.is_valid():
            form.save()
            # Redirect back to list maybe? Or detail?
            return redirect('log_list') # Changed redirect target
    else: # GET request
        form = DutyHourLogForm(instance=log_instance)

    context = {'form': form, 'log_instance': log_instance, 'form_title': 'Edit Duty Log'}
    # Still uses the old log_form.html - this is for editing *existing* records
    return render(request, 'duty_hour_log/log_form.html', context)

# Delete View - Keep for deleting existing records via separate page/confirmation
def log_delete(request, pk):
    log_instance = get_object_or_404(DutyHourLog, pk=pk)
    if request.method == 'POST':
        log_instance.delete()
        return redirect('log_list')

    context = {'log': log_instance}
    return render(request, 'duty_hour_log/log_confirm_delete.html', context)

@require_POST # Or use require_http_methods(['POST']) or handle PATCH
def update_inline_log(request, pk):
    try:
        log_instance = DutyHourLog.objects.get(pk=pk)
    except DutyHourLog.DoesNotExist:
        return JsonResponse({'status': 'error', 'errors': {'__all__': ['Log entry not found.']}}, status=404)

    try:
        data = json.loads(request.body)
        new_finish_time_str = data.get('finish_time', '').strip()
        new_remarks = data.get('remarks', log_instance.remarks or '').strip() # Default to existing if not provided

        # --- Validation ---
        errors = {}
        new_finish_time = None

        if new_finish_time_str: # Only validate if a value was provided
            new_finish_time = parse_time(new_finish_time_str)
            if new_finish_time is None:
                errors['finish_time'] = ['Invalid time format. Use HH:MM.']
            elif log_instance.start_time and new_finish_time <= log_instance.start_time:
                 errors['finish_time'] = ['Finish time must be after start time.']
        # else: finish time is being cleared or left empty, which is allowed

        if errors:
             return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        # --- Update Instance ---
        log_instance.finish_time = new_finish_time # Assign None if cleared or invalid (though invalid caught above)
        log_instance.remarks = new_remarks
        log_instance.save(update_fields=['finish_time', 'remarks'])

        # --- Return Success Response ---
        return JsonResponse({
            'status': 'success',
            'log_id': log_instance.pk,
            'finish_time_display': log_instance.finish_time.strftime('%H:%M') if log_instance.finish_time else '...',
            'finish_time_value': log_instance.finish_time.strftime('%H:%M') if log_instance.finish_time else '',
            'remarks_display': log_instance.remarks[:30] + ('...' if len(log_instance.remarks) > 30 else ''), # Truncated for display
            'remarks_value': log_instance.remarks, # Full value for data attribute
            'can_edit_again': not bool(log_instance.finish_time) # True if finish_time is None/empty
        })

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'errors': {'__all__': ['Invalid request format.']}}, status=400)
    except Exception as e:
        # Log the exception e
        print(f"Error updating inline log {pk}: {e}") # Basic logging
        return JsonResponse({'status': 'error', 'errors': {'__all__': [f'An unexpected server error occurred.']}}, status=500)