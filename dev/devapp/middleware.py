import time
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

class AutoLogoutMiddleware:
    """
    Logs the user out server-side if they have been inactive for longer
    than INACTIVITY_TIMEOUT seconds. Works regardless of browser session
    restore behavior because the check is entirely server-side.
    """
    TIMEOUT = getattr(settings, 'INACTIVITY_TIMEOUT', 86400)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('_last_activity')
            now = time.time()

            if last_activity and (now - last_activity) > self.TIMEOUT:
                logout(request)
                return redirect(settings.LOGIN_URL)

            request.session['_last_activity'] = now

        return self.get_response(request)