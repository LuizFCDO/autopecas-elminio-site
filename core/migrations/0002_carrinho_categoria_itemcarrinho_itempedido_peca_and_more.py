# Generated by Django 5.1.7 on 2025-05-24 14:16

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='ItemCarrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('adicionado_em', models.DateTimeField(auto_now_add=True)),
                ('carrinho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='core.carrinho')),
            ],
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantidade', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Peca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('codigo', models.CharField(max_length=50, unique=True)),
                ('descricao', models.TextField()),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estoque', models.PositiveIntegerField(default=0)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='pecas/')),
                ('destaque', models.BooleanField(default=False)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pecas', to='core.categoria')),
            ],
            options={
                'verbose_name': 'Peça',
                'verbose_name_plural': 'Peças',
                'ordering': ['-destaque', 'nome'],
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=20)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('processando', 'Processando'), ('concluido', 'Concluído'), ('cancelado', 'Cancelado')], default='pendente', max_length=20)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.AddField(
            model_name='itempedido',
            name='peca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.peca'),
        ),
        migrations.AddField(
            model_name='itemcarrinho',
            name='peca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.peca'),
        ),
        migrations.AddField(
            model_name='itempedido',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='core.pedido'),
        ),
        migrations.AlterUniqueTogether(
            name='itemcarrinho',
            unique_together={('carrinho', 'peca')},
        ),
    ]
