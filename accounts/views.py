from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import render, redirect

@login_required
def change_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # after change, redirect to login
    else:
        form = SetPasswordForm(user=request.user)
    return render(request, 'accounts/password_change.html', {'form': form})
