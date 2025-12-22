from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .services.lc_export import export_lcs_to_excel
from .services.lc_calculation import compute_lc_metrics
from datetime import datetime

@login_required
def lc_create(request):
    return render(request, 'lc/lc_create.html')
    
@login_required
def lc_list(request):
    return render(request, 'lc/lc_list.html')  # placeholder


from django.shortcuts import render, redirect
from .forms import LCForm

@login_required
def lc_create(request):
    if request.method == "POST":
        form = LCForm(request.POST)
        if form.is_valid():
            lc = form.save(commit=False)
            lc.bank = form.cleaned_data["bank_name"]  # Bank instance
            lc.swift_code = lc.bank.swift_code
            lc.created_by = request.user
            lc.updated_by = request.user
            lc.save()
            return redirect("lc_list")
    else:
        form = LCForm()

    banks = Bank.objects.all()  # Pass all banks to template
    return render(request, "lc/lc_create.html", {"form": form, "banks": banks})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import LC
from .forms import LCForm

@login_required
def lc_edit(request, pk):
    lc = get_object_or_404(LC, pk=pk)

    if request.method == "POST":
        form = LCForm(request.POST, instance=lc, readonly=True)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.user
            obj.save()
            return redirect("lc_list")
    else:
        form = LCForm(instance=lc, readonly=True)  # ← important

    return render(request, "lc/lc_edit.html", {"form": form})





from django.http import JsonResponse
from .models import Bank

@login_required
def get_swift_code(request):
    bank_name = request.GET.get('bank_name')
    try:
        bank = Bank.objects.get(name=bank_name)
        swift_code = bank.swift_code
    except Bank.DoesNotExist:
        swift_code = ''
    return JsonResponse({'swift_code': swift_code})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import LC, Bank
from .services.lc_calculation import compute_lc_metrics

from django.core.paginator import Paginator

@login_required
def lc_list(request):
    lcs = LC.objects.select_related("bank", "created_by", "updated_by").order_by("bank_id", "opening_date")



    # Filters
    bank_id = request.GET.get("bank") or None
    status = request.GET.get("status") or None
    date_from = request.GET.get("date_from") or None
    date_to = request.GET.get("date_to") or None
    sort_by = request.GET.get("sort_by", "bank__name")  # default sort
    order = request.GET.get("order", "asc")
    lc_no = request.GET.get('lc_no', '').strip()
    if lc_no:
        lcs = lcs.filter(lc_no=lc_no)


    if bank_id:
        lcs = lcs.filter(bank_id=bank_id)
    if status:
        lcs = lcs.filter(status=status)
    if date_from:
        lcs = lcs.filter(maturity_date__gte=date_from)
    if date_to:
        lcs = lcs.filter(maturity_date__lte=date_to)

    lcs = lcs.order_by("bank_id", "opening_date")

        # Sorting
    if sort_by in ["opening_date", "maturity_date"]:
        if order == "desc":
            lcs = lcs.order_by(f"-{sort_by}")
        else:
            lcs = lcs.order_by(sort_by)
    else:
        lcs = lcs.order_by("bank__name", "opening_date")

    # Compute first, paginate later
    computed_lcs = compute_lc_metrics(lcs)

    paginator = Paginator(computed_lcs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "lc/lc_list.html",
        {
            "page_obj": page_obj,
            "banks": Bank.objects.all(),
        }
    )





@login_required
def lc_export(request):
    lcs = LC.objects.select_related(
        "bank", "created_by", "updated_by"
    )

    # Same filters as list
    bank_id = request.GET.get("bank")
    status = request.GET.get("status")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    if bank_id:
        lcs = lcs.filter(bank_id=bank_id)
    if status:
        lcs = lcs.filter(status=status)
    if date_from:
        lcs = lcs.filter(maturity_date__gte=date_from)
    if date_to:
        lcs = lcs.filter(maturity_date__lte=date_to)

    lcs = lcs.order_by("bank_id", "opening_date")

    computed_lcs = compute_lc_metrics(lcs)

    wb = export_lcs_to_excel(computed_lcs)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    filename = f"LC_List_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    wb.save(response)
    return response



from django.shortcuts import get_object_or_404
from django.contrib import messages

@login_required
def lc_edit(request, pk):
    lc = get_object_or_404(LC, pk=pk)

    if request.method == "POST":
        form = LCForm(request.POST, instance=lc)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.swift_code = obj.bank.swift_code
            obj.updated_by = request.user
            obj.save()
            return redirect("lc_list")
    else:
        form = LCForm(instance=lc)

    return render(
        request,
        "lc/lc_edit.html",
        {"form": form}
    )


@login_required
def lc_delete(request, pk):
    lc = get_object_or_404(LC, pk=pk)

    if request.method == "POST":
        lc.delete()
        return redirect("lc_list")

    return render(
        request,
        "lc/lc_confirm_delete.html",
        {"lc": lc}
    )


# views.py
from django.http import JsonResponse
from .models import LC

def lc_number_autocomplete(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        lcs = LC.objects.filter(lc_no__icontains=query).order_by('lc_no')[:10]
        results = [{'id': lc.id, 'text': lc.lc_no} for lc in lcs]
    return JsonResponse({'results': results})


# views.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import LC
from django.contrib.auth.decorators import user_passes_test, login_required

@login_required
@user_passes_test(lambda u: u.is_superuser)
def lc_undo_close(request, lc_id):
    lc = get_object_or_404(LC, id=lc_id)
    if lc.status != 'Closed':
        messages.error(request, "LC is not closed, cannot undo.")
        return redirect('lc_list')

    # Undo: set status back to 'Approved' (or 'New' depending on your workflow)
    lc.status = 'Open'
    lc.save()
    messages.success(request, f"LC {lc.lc_no} status undone. Edit/Delete now enabled.")
    return redirect('lc_list')



