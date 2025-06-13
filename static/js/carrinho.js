// ========================================
// FUNCIONALIDADES DO CARRINHO
// ========================================

/**
 * Atualiza o contador do carrinho na navbar
 */
function atualizarContadorCarrinho(quantidade) {
    const contador = document.querySelector('.nav-link .badge');
    if (contador) {
        contador.textContent = quantidade;
    } else if (quantidade > 0) {
        const carrinhoLink = document.querySelector('a[href*="carrinho"]');
        if (carrinhoLink) {
            const badge = document.createElement('span');
            badge.className = 'badge bg-secondary rounded-pill';
            badge.textContent = quantidade;
            carrinhoLink.appendChild(badge);
        }
    }
}

/**
 * Adiciona produto ao carrinho via AJAX
 */
function adicionarAoCarrinho(pecaId, csrfToken) {
    return fetch(`/adicionar-ao-carrinho/${pecaId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Atualiza contador do carrinho
            atualizarContadorCarrinho(data.quantidade_itens);
            
            // Mostra mensagem de sucesso
            showResponsiveMessage(
                '<i class="fas fa-check-circle me-2"></i>Produto adicionado ao carrinho!', 
                'success'
            );
        } else {
            showResponsiveMessage(
                '<i class="fas fa-exclamation-circle me-2"></i>Erro ao adicionar produto!', 
                'danger'
            );
        }
        return data;
    })
    .catch(error => {
        console.error('Erro:', error);
        showResponsiveMessage(
            '<i class="fas fa-exclamation-circle me-2"></i>Erro de conexão!', 
            'danger'
        );
        throw error;
    });
}

/**
 * Inicializa os botões de adicionar ao carrinho
 */
function initBotoesCarrinho() {
    const botoesAdicionar = document.querySelectorAll('.adicionar-carrinho');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                     document.querySelector('meta[name="csrf-token"]')?.content;
    
    botoesAdicionar.forEach(botao => {
        botao.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation(); // Evita que o clique no card seja acionado
            
            const pecaId = this.dataset.id;
            if (!pecaId) {
                console.error('ID da peça não encontrado');
                return;
            }
            
            // Desabilita o botão temporariamente
            const botaoOriginal = this.innerHTML;
            this.disabled = true;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            
            adicionarAoCarrinho(pecaId, csrfToken)
                .finally(() => {
                    // Reabilita o botão
                    this.disabled = false;
                    this.innerHTML = botaoOriginal;
                });
        });
    });
}

// ========================================
// FUNCIONALIDADES DA PÁGINA DO CARRINHO
// ========================================

/**
 * Controles de quantidade no carrinho
 */
function initControlesQuantidade() {
    // Botões de incrementar/decrementar
    const botoesIncremento = document.querySelectorAll('[data-action="increment"]');
    const botoesDecremento = document.querySelectorAll('[data-action="decrement"]');
    
    botoesIncremento.forEach(botao => {
        botao.addEventListener('click', function() {
            const input = this.parentNode.querySelector('input[type="number"]');
            const max = parseInt(input.getAttribute('max')) || 999;
            const currentValue = parseInt(input.value);
            
            if (currentValue < max) {
                input.value = currentValue + 1;
            }
        });
    });
    
    botoesDecremento.forEach(botao => {
        botao.addEventListener('click', function() {
            const input = this.parentNode.querySelector('input[type="number"]');
            const currentValue = parseInt(input.value);
            
            if (currentValue > 1) {
                input.value = currentValue - 1;
            }
        });
    });
}

// ========================================
// INICIALIZAÇÃO
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    initBotoesCarrinho();
    initControlesQuantidade();
});
