class MiddlewareIP:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')

        if lista_ip:
            request.ip_client = lista_ip.split(',')[-1].strip()
        else:
            request.ip_client = request.META.get('REMOTE_ADDR')

        response = self.get_response(request)

        return response