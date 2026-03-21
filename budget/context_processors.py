def admin_check(request):
    """Add is_admin to template context"""
    is_admin = False
    if request.user.is_authenticated:
        try:
            is_admin = hasattr(request.user, 'profile') and request.user.profile.is_admin
        except:
            is_admin = False
    return {'user_is_admin': is_admin}
