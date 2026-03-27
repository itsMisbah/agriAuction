from allauth.account.signals import user_signed_up, user_logged_in
from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken

@receiver(user_signed_up)
def assign_role(request, user, **kwargs):
    role = request.session.pop('selected_role', 'BUYER')

    if role not in ['FARMER', 'BUYER']:  
        role = 'BUYER'
        
    user.role = role
    user.save()

@receiver(social_account_added)
def assign_role_social(request, sociallogin, **kwargs):
    role = request.session.pop('selected_role', 'BUYER')
    if role not in ['FARMER', 'BUYER']:
        role = 'BUYER'
    sociallogin.user.role = role
    sociallogin.user.save()

@receiver(user_logged_in)
def save_jwt_on_login(sender, request, user, **kwargs):
    refresh = RefreshToken.for_user(user)
    # Session mein save 
    request.session['jwt_access'] = str(refresh.access_token)
    request.session['jwt_refresh'] = str(refresh)