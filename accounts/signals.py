from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver

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