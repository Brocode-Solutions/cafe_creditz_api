class CafeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        def get_user_type():
            if request.user.is_authenticated:
                if hasattr(request.user, 'staff'):
                    return 'Staff'
                elif hasattr(request.user, 'owner'):
                    return 'Owner'
                elif hasattr(request.user, 'customer'):
                    return 'Customer'
            return None

        def get_cafe():
            if request.user.is_authenticated and hasattr(request.user, 'staff'):
                staff_profile = request.user.staff
                if staff_profile.cafe:
                    return staff_profile.cafe.id
            return None

        request.get_user_type = lambda: get_user_type()
        request.get_cafe = lambda: get_cafe()
        response = self.get_response(request)
        return response
