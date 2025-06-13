from .models import Carrinho

class CarrinhoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Código executado antes da view
        carrinho_id = request.session.get('carrinho_id')
        
        if carrinho_id:
            try:
                carrinho = Carrinho.objects.get(id=carrinho_id)
                request.session['carrinho_quantidade'] = carrinho.quantidade_itens
            except Carrinho.DoesNotExist:
                request.session['carrinho_quantidade'] = 0
        else:
            request.session['carrinho_quantidade'] = 0
            
        response = self.get_response(request)
        
        # Código executado após a view
        return response