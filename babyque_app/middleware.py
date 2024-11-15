from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from babyque_app.models import User  # Import your User model

class BlockedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the user_id from the session
        user_id = request.session.get('user_id')

        if user_id:
            try:
                # Fetch the user from the database using the user_id
                user = User.objects.get(id=user_id)

                # Check if the user is blocked
                if user.is_blocked:
                    logout(request)
                    messages.error(request, "Your account is blocked.")
                    return redirect('login')

            except User.DoesNotExist:
                # In case user_id is in session but user doesn't exist (should rarely happen)
                logout(request)
                messages.error(request, "User not found.")
                return redirect('login')

        # Continue processing the request
        return self.get_response(request)
