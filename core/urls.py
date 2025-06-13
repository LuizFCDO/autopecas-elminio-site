from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    
    # Catálogo de peças
    path('catalogo/', views.CatalogoPecasView.as_view(), name='catalogo'),
    path('catalogo/<slug:categoria_slug>/', views.CatalogoPecasView.as_view(), name='catalogo_categoria'),
    path('peca/<slug:slug>/', views.PecaDetalheView.as_view(), name='peca_detalhe'),
    
    # Carrinho
    path('carrinho/', views.carrinho_view, name='carrinho'),
    path('adicionar-ao-carrinho/<int:peca_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover-do-carrinho/<int:item_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('atualizar-carrinho/<int:item_id>/', views.atualizar_carrinho, name='atualizar_carrinho'),
    
    # Checkout
    path('checkout/', views.checkout_view, name='checkout'),
    path('pedido-confirmado/<uuid:pedido_id>/', views.pedido_confirmado, name='pedido_confirmado'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)