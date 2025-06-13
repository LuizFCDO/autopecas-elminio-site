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
        // Salva o elemento pai
        const parentElement = quantidadeInput.parentNode;
        
        // Cria container para os controles
        const controlsContainer = document.createElement('div');
        controlsContainer.className = 'quantidade-controls';
        
        // Remove o input do DOM temporariamente
        quantidadeInput.remove();
        
        // Remove classes do input
        quantidadeInput.classList.remove('form-control');
        
        // Botão menos
        const btnMenos = document.createElement('button');
        btnMenos.type = 'button';
        btnMenos.className = 'btn-quantidade';
        btnMenos.innerHTML = '−';
        btnMenos.title = 'Diminuir quantidade';
        btnMenos.addEventListener('click', function() {
            const currentValue = parseInt(quantidadeInput.value);
            if (currentValue > 1) {
                quantidadeInput.value = currentValue - 1;
            }
        });

        // Botão mais
        const btnMais = document.createElement('button');
        btnMais.type = 'button';
        btnMais.className = 'btn-quantidade';
        btnMais.innerHTML = '+';
        btnMais.title = 'Aumentar quantidade';
        btnMais.addEventListener('click', function() {
            const currentValue = parseInt(quantidadeInput.value);
            const max = parseInt(quantidadeInput.getAttribute('max')) || 999;
            if (currentValue < max) {
                quantidadeInput.value = currentValue + 1;
            }
        });
        
        // Monta a estrutura
        controlsContainer.appendChild(btnMenos);
        controlsContainer.appendChild(quantidadeInput);
        controlsContainer.appendChild(btnMais);
        
        // Adiciona o container ao pai
        parentElement.appendChild(controlsContainer);
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
