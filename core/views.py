from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from .models import Peca, Categoria, Carrinho, ItemCarrinho, Pedido, ItemPedido
from .forms import PedidoForm
from urllib.parse import quote

def home(request):
    pecas_destaque = Peca.objects.filter(destaque=True)[:6]
    categorias = Categoria.objects.all()
    return render(request, 'core/home.html', {
        'pecas_destaque': pecas_destaque,
        'categorias': categorias
    })

def sobre(request):
    return render(request, 'core/sobre.html')

class CatalogoPecasView(ListView):
    model = Peca
    template_name = 'core/catalogo.html'
    context_object_name = 'pecas'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_slug = self.kwargs.get('categoria_slug')
        
        if categoria_slug:
            queryset = queryset.filter(categoria__slug=categoria_slug)
            
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(nome__icontains=q) | queryset.filter(codigo__icontains=q) | queryset.filter(codigos_alternativos__icontains=q)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        categoria_slug = self.kwargs.get('categoria_slug')
        
        if categoria_slug:
            context['categoria_atual'] = get_object_or_404(Categoria, slug=categoria_slug)
            
        return context

class PecaDetalheView(DetailView):
    model = Peca
    template_name = 'core/peca_detalhe.html'
    context_object_name = 'peca'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pecas_relacionadas'] = Peca.objects.filter(
            categoria=self.object.categoria
        ).exclude(id=self.object.id)[:4]
        return context

def get_carrinho(request):
    """Obtém ou cria um carrinho na sessão"""
    carrinho_id = request.session.get('carrinho_id')
    
    if carrinho_id:
        carrinho = Carrinho.objects.filter(id=carrinho_id).first()
        if carrinho:
            return carrinho
    
    # Cria um novo carrinho
    carrinho = Carrinho.objects.create()
    request.session['carrinho_id'] = str(carrinho.id)
    return carrinho

def adicionar_ao_carrinho(request, peca_id):
    peca = get_object_or_404(Peca, id=peca_id)
    carrinho = get_carrinho(request)
    
    # Verifica se o item já está no carrinho
    item, created = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho,
        peca=peca,
        defaults={'quantidade': 1}
    )
    
    # Se o item já existir, incrementa a quantidade
    if not created:
        item.quantidade += 1
        item.save()
    
    messages.success(request, f'{peca.nome} adicionado ao carrinho!')
    
    # Se for uma requisição AJAX, retorna JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'quantidade_itens': carrinho.quantidade_itens,
            'total': float(carrinho.total)
        })
    
    # Caso contrário, redireciona para a página do carrinho
    return redirect('carrinho')

def remover_do_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id)
    carrinho = get_carrinho(request)
    
    # Verifica se o item pertence ao carrinho atual
    if item.carrinho.id == carrinho.id:
        item.delete()
        messages.success(request, 'Item removido do carrinho!')
    
    return redirect('carrinho')

def atualizar_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id)
    carrinho = get_carrinho(request)
    
    # Verifica se o item pertence ao carrinho atual
    if item.carrinho.id == carrinho.id:
        quantidade = int(request.POST.get('quantidade', 1))
        
        if quantidade > 0:
            item.quantidade = quantidade
            item.save()
        else:
            item.delete()
    
    return redirect('carrinho')

def carrinho_view(request):
    carrinho = get_carrinho(request)
    return render(request, 'core/carrinho.html', {'carrinho': carrinho})

def gerar_mensagem_whatsapp(pedido):
    """Gera mensagem formatada para WhatsApp"""
    nome = pedido.nome
    
    # Cabeçalho da mensagem
    mensagem = f"Olá, me chamo *{nome}*.\n"
    mensagem += "Fiz o seguinte orçamento no site de vocês:\n\n"
    mensagem += "*Itens:*\nItem | *Código* | Quantidade | Preço Unitário | Preço Total\n"
    
    # Lista de itens
    for item in pedido.itens.all():
        mensagem += f"\n{item.peca.nome} | *{item.peca.codigo}* | {item.quantidade}x | "
        mensagem += f"R$ {item.preco:.2f} | R$ {item.subtotal:.2f}\n"
    
    # Observação
    if pedido.observacoes:
        mensagem += f"\n*Observação:*\n{pedido.observacoes}\n"
    
    # Total
    mensagem += f"\n*Total Geral: R$ {pedido.total:.2f}*"
    
    return mensagem


def checkout_view(request):
    carrinho = get_carrinho(request)
    
    if carrinho.itens.count() == 0:
        messages.warning(request, 'Seu carrinho está vazio!')
        return redirect('catalogo')
    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            # Cria o pedido
            pedido = form.save(commit=False)
            pedido.total = carrinho.total
            pedido.save()
            
            # Transfere os itens do carrinho para o pedido
            for item in carrinho.itens.all():
                ItemPedido.objects.create(
                    pedido=pedido,
                    peca=item.peca,
                    preco=item.peca.preco,
                    quantidade=item.quantidade
                )
            
            # Gera mensagem WhatsApp
            mensagem_whatsapp = gerar_mensagem_whatsapp(pedido)
            mensagem_encoded = quote(mensagem_whatsapp)
            whatsapp_url = f"https://wa.me/5564999888800?text={mensagem_encoded}"

            # Limpa o carrinho
            carrinho.itens.all().delete()

            # Limpa a sessão
            if 'carrinho_id' in request.session:
                del request.session['carrinho_id']

            # Armazena a URL do WhatsApp na sessão para usar no template
            request.session['whatsapp_url'] = whatsapp_url

            messages.success(request, 'Pedido realizado com sucesso!')
            return redirect('pedido_confirmado', pedido_id=pedido.id)
    else:
        form = PedidoForm()
    
    return render(request, 'core/checkout.html', {
        'carrinho': carrinho,
        'form': form
    })

def pedido_confirmado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Recupera URL do WhatsApp da sessão
    whatsapp_url = request.session.get('whatsapp_url', '')
    
    # Remove da sessão após usar
    if 'whatsapp_url' in request.session:
        del request.session['whatsapp_url']

    # Gera a mensagem novamente para o fallback
    mensagem_whatsapp = gerar_mensagem_whatsapp(pedido) if pedido else ""

    return render(request, 'core/pedido_confirmado.html', {
        'pedido': pedido,
        'whatsapp_url': whatsapp_url,
        'mensagem_whatsapp': mensagem_whatsapp
    })

