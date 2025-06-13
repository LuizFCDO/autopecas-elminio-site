from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

class Peca(models.Model):
    nome = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    codigo = models.CharField(max_length=50, unique=True)
    codigos_alternativos = models.CharField(max_length=500, blank=True, null=True, help_text='Códigos alternativos separados por vírgula')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='pecas')
    descricao = models.TextField()
    aplicacao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)    
    imagem = models.ImageField(upload_to='pecas/', blank=True, null=True)
    destaque = models.BooleanField(default=False)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('peca_detalhe', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.codigo)
        super().save(*args, **kwargs)
    
    def preco_parcelado(self, parcelas=3):
        """Retorna o valor da parcela em até 3x sem juros"""
        if parcelas <= 1:
            return self.preco
        return self.preco / parcelas
    
    class Meta:
        verbose_name = 'Peça'
        verbose_name_plural = 'Peças'
        ordering = ['-destaque', 'nome']

class Carrinho(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Carrinho {self.id}"
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())
    
    @property
    def quantidade_itens(self):
        return self.itens.count()

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    peca = models.ForeignKey(Peca, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    adicionado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantidade}x {self.peca.nome}"
    
    @property
    def subtotal(self):
        return self.peca.preco * self.quantidade
    
    class Meta:
        unique_together = ('carrinho', 'peca')

class Pedido(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('processando', 'Processando'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=200)
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Pedido {self.id}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    peca = models.ForeignKey(Peca, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantidade}x {self.peca.nome}"
    
    @property
    def subtotal(self):
        return self.preco * self.quantidade
