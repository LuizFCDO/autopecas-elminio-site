// ========================================
// FUNCIONALIDADES DA PÁGINA DE PRODUTO
// ========================================

/**
 * Inicializa funcionalidades específicas da página de produto
 */
function initPaginaProduto() {
    // Controle de quantidade no formulário principal
    const quantidadeInput = document.querySelector('input[name="quantidade"]');
    if (quantidadeInput && !quantidadeInput.closest('.quantidade-controls')) {
        // Cria container para os controles
        const controlsContainer = document.createElement('div');
        controlsContainer.className = 'quantidade-controls';
        
        // Clona o input para manter suas propriedades
        const novoInput = quantidadeInput.cloneNode(true);
        novoInput.classList.remove('form-control');
        
        // Botão menos
        const btnMenos = document.createElement('button');
        btnMenos.type = 'button';
        btnMenos.className = 'btn-quantidade';
        btnMenos.innerHTML = '−';
        btnMenos.title = 'Diminuir quantidade';
        btnMenos.addEventListener('click', function() {
            const currentValue = parseInt(novoInput.value);
            if (currentValue > 1) {
                novoInput.value = currentValue - 1;
            }
        });

        // Botão mais
        const btnMais = document.createElement('button');
        btnMais.type = 'button';
        btnMais.className = 'btn-quantidade';
        btnMais.innerHTML = '+';
        btnMais.title = 'Aumentar quantidade';
        btnMais.addEventListener('click', function() {
            const currentValue = parseInt(novoInput.value);
            const max = parseInt(novoInput.getAttribute('max')) || 999;
            if (currentValue < max) {
                novoInput.value = currentValue + 1;
            }
        });
        
        // Garante que o novo input tenha o mesmo name
        novoInput.name = 'quantidade';
        novoInput.id = quantidadeInput.id;

        // Monta a estrutura
        controlsContainer.appendChild(btnMenos);
        controlsContainer.appendChild(novoInput);
        controlsContainer.appendChild(btnMais);

        // Substitui o input original pelo container
        quantidadeInput.parentNode.replaceChild(controlsContainer, quantidadeInput);

    }
}

// ========================================
// INICIALIZAÇÃO
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // Verifica se estamos na página de produto
    if (document.querySelector('.breadcrumb') || document.querySelector('form[action*="adicionar-ao-carrinho"]')) {
        initPaginaProduto();
    }
});
