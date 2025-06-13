from django.contrib import admin
from .models import Categoria, Peca, Carrinho, ItemCarrinho, Pedido, ItemPedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome',)

class ItemCarrinhoInline(admin.TabularInline):
    model = ItemCarrinho
    extra = 0

@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('id', 'criado_em', 'total', 'quantidade_itens')
    inlines = [ItemCarrinhoInline]
    readonly_fields = ('id', 'criado_em', 'atualizado_em')

@admin.register(Peca)
class PecaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'categoria', 'preco', 'destaque')
    list_filter = ('categoria', 'destaque')
    search_fields = ('nome', 'codigo', 'descricao')
    prepopulated_fields = {'slug': ('codigo',)}
    list_editable = ('preco', 'destaque')

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('peca', 'preco', 'quantidade', 'subtotal')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'total', 'status', 'criado_em')
    list_filter = ('status', 'criado_em')
    search_fields = ('nome', 'total', 'criado_em')
    readonly_fields = ('id', 'total', 'criado_em')
    inlines = [ItemPedidoInline]
