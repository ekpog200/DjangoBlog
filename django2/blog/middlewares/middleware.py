from django.db.models import F

from blog.models import UserPlatformStats


class DemoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.num_request = 0

    def stat(self, os_info):
        if "Windows" in os_info:
            UserPlatformStats.objects.all().update(win=F('win') + 1)
        elif "mac" in os_info:
            UserPlatformStats.objects.all().update(win=F('mac') + 1)
        elif "Iphone" in os_info:
            UserPlatformStats.objects.all().update(win=F('iphone') + 1)
        elif "Android" in os_info:
            UserPlatformStats.objects.all().update(win=F('android') + 1)
        else:
            UserPlatformStats.objects.all().update(win=F('other') + 1)

    def __call__(self, request):
        # тут вызывается ПЕРЕД вьюхой (сервер-клиент)
        if 'admin' not in request.path:
            self.stat(request.META['HTTP_USER_AGENT'])

        response = self.get_response(request)
        # тут вызывается ПОСЛЕ вьюхи(клиент-сервер)

        return response
