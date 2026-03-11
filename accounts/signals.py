from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def assign_role(request, user, **kwargs):
    role = request.session.pop('selected_role', 'BUYER')

    if role not in ['FARMER', 'BUYER']:  # sirf valid roles allow karo
        role = 'BUYER'
        
    user.role = role
    user.save()