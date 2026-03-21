from django import template

register = template.Library()

@register.simple_tag
def user_is_admin(user):
    """Safely check if user is an admin"""
    try:
        return hasattr(user, 'profile') and user.profile.is_admin
    except:
        return False
