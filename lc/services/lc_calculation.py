from collections import defaultdict
from datetime import date

def compute_lc_metrics(lc_queryset):
    """
    Input: queryset of LC ordered by bank, opening_date
    Output: list of dicts with remaining_amount & matured_in
    """

    bank_remaining = defaultdict(lambda: None)
    result = []

    today = date.today()

    for lc in lc_queryset:
        bank_id = lc.bank_id

        # Remaining Amount
        if bank_remaining[bank_id] is None:
            # first LC for bank
            remaining = lc.global_limit - lc.lc_amount if lc.status == "Open" else lc.global_limit
        else:
            if lc.status == "Open":
                remaining = bank_remaining[bank_id] - lc.lc_amount
            else:
                remaining = bank_remaining[bank_id]

        bank_remaining[bank_id] = remaining

        # Matured In
        if lc.status == "Close":
            matured_in = "Matured"
        else:
            days = (lc.maturity_date - today).days
            matured_in = "Matured" if days < 0 else f"{days} Days"

        result.append({
            "lc": lc,
            "remaining_amount": remaining,
            "matured_in": matured_in,
        })

    return result
