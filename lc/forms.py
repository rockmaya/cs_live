from django import forms
from django.core.exceptions import ValidationError
from .models import LC, Bank

class LCForm(forms.ModelForm):
    bank_name = forms.CharField(
        label="Bank",
        widget=forms.TextInput(attrs={"placeholder": "Bank", "autocomplete": "off", "class": "bank-typeahead"})
    )

    swift_code = forms.CharField(
        label="Swift Code",
        required=False,  # Not required
        widget=forms.TextInput(attrs={"readonly": "readonly"})
    )


    opening_date = forms.DateField(
        widget=forms.TextInput(attrs={"class": "datepicker", "autocomplete": "off"})
    )
    maturity_date = forms.DateField(
        widget=forms.TextInput(attrs={"class": "datepicker", "autocomplete": "off"})
    )

    class Meta:
        model = LC
        fields = [
            "bank_name", "swift_code", "global_limit", "lc_no",
            "opening_date", "lc_amount", "maturity_date", "status"
        ]


    def __init__(self, *args, **kwargs):
        readonly = kwargs.pop("readonly", False)  # ONLY for Edit page
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["bank_name"].initial = self.instance.bank.name
            self.fields["swift_code"].initial = self.instance.swift_code

        if readonly:
            # Bank and Swift non-editable for Edit page
            style = "background-color:#e9ecef; cursor:not-allowed; pointer-events:none; user-select:none;"
            self.fields["bank_name"].widget.attrs["readonly"] = True
            self.fields["bank_name"].widget.attrs["style"] = style
            self.fields["swift_code"].widget.attrs["readonly"] = True
            self.fields["swift_code"].widget.attrs["style"] = style

    def clean_bank_name(self):
        """
        Validate bank field:
        - On edit (readonly) → return existing bank instance
        - On create → check Bank exists
        """
        if self.instance and self.instance.pk:
            # Prevent bank change on edit
            return self.instance.bank

        name = self.cleaned_data.get("bank_name")
        if not name:
            raise ValidationError("Bank is required")
        try:
            bank = Bank.objects.get(name=name)
        except Bank.DoesNotExist:
            raise ValidationError("Bank does not exist")
        return bank

    def clean(self):
        """
        Cross-field validation:
        - Maturity date cannot be before opening date
        """
        cleaned_data = super().clean()
        opening = cleaned_data.get("opening_date")
        maturity = cleaned_data.get("maturity_date")

        if opening and maturity:
            if maturity < opening:
                self.add_error("maturity_date", "Maturity date cannot be before opening date.")

        return cleaned_data
