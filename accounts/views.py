from django.shortcuts import redirect, render

def select_role(request):
    return render(request, 'role_selection.html')

def get_role(request): 
    # GET request — pick role from URL, save in session, redirect to signup
    role = request.GET.get('role', 'BUYER')
    request.session['selected_role'] = role
    request.session.modified = True
    return redirect('account_signup')