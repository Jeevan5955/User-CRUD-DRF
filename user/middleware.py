from django.conf import settings

class CustomMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each response after the view is called
        return response
    
    def process_exception(self, request, exception):
        # This code is executed if an exception is raised
        # Logging or changing the response structure can be handled here
        if settings.DEBUG:
            print("Print exception occured :",exception)

        return None

