# infrastructure/multitenancy/middleware.py
from django.http import JsonResponse


class TenantMiddleware:
    """
    Middleware responsável por extrair o Tenant-ID dos cabeçalhos HTTP
    e injetar o identificador no objeto 'request'.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Isola a validação apenas para as rotas de API
        if request.path.startswith('/api/'):
            tenant_id = request.headers.get('X-Tenant-ID')

            if not tenant_id:
                return JsonResponse(
                    {'error': 'O cabeçalho HTTP X-Tenant-ID é obrigatório.'},
                    status=400,
                )

            # Injeta o tenant_id no request para uso nas Views e Casos de Uso
            request.tenant_id = tenant_id

        return self.get_response(request)