// ========================================
// FUNÇÕES PRINCIPAIS DE NOTIFICAÇÃO
// ========================================

/**
 * Mostra toast flutuante para dispositivos móveis
 */
function showMobileToast(message, type = 'info') {
    // Só mostra em mobile
    if (window.innerWidth > 768) return;
    
    const container = document.getElementById('mobileToastContainer');
    const toast = document.getElementById('mobileToast');
    
    if (!container || !toast) {
        console.error('Elementos de toast não encontrados');
        return;
    }
    
    const toastBody = toast.querySelector('.toast-body');
    const toastIcon = toast.querySelector('.fas');
    
    // Mostra o container
    container.style.display = 'block';
    
    // Atualiza conteúdo
    toastBody.innerHTML = message;
    
    // Atualiza ícone
    const iconClasses = {
        'success': 'fa-check-circle text-success',
        'danger': 'fa-exclamation-circle text-danger',
        'warning': 'fa-exclamation-triangle text-warning',
        'info': 'fa-info-circle text-primary'
    };
    
    toastIcon.className = `fas me-2 ${iconClasses[type] || iconClasses.info}`;
    
    // Mostra o toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 5000
    });
    
    bsToast.show();
    
    // Esconde o container quando o toast for fechado
    toast.addEventListener('hidden.bs.toast', function() {
        container.style.display = 'none';
    }, { once: true });
}

/**
 * Função auxiliar para mostrar mensagens responsivas
 */
function showResponsiveMessage(message, type = 'info') {
    if (window.innerWidth <= 768) {
        // Mobile: toast flutuante
        showMobileToast(message, type);
    } else {
        // Desktop: alert normal
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        const content = document.querySelector('.col-lg-9') || document.querySelector('main') || document.body;
        content.insertBefore(alertDiv, content.firstChild);
        
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 3000);
    }
}

// ========================================
// INICIALIZAÇÃO
// ========================================

/**
 * Converte alerts existentes em toasts no mobile
 */
function initMobileToasts() {
    if (window.innerWidth <= 768) {
        const alerts = document.querySelectorAll('.alert:not(.toast)');
        alerts.forEach(alert => {
            // Extrai o texto da mensagem
            const messageElement = alert.cloneNode(true);
            const closeButton = messageElement.querySelector('.btn-close');
            if (closeButton) closeButton.remove();
            
            const message = messageElement.innerHTML;
            
            // Determina o tipo
            let type = 'info';
            if (alert.classList.contains('alert-success')) type = 'success';
            else if (alert.classList.contains('alert-danger')) type = 'danger';
            else if (alert.classList.contains('alert-warning')) type = 'warning';
            
            // Esconde o alert original
            alert.style.display = 'none';
            
            // Mostra como toast
            showMobileToast(message, type);
        });
    }
}

// ========================================
// EVENT LISTENERS
// ========================================

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    initMobileToasts();
});

// Reajusta ao redimensionar a tela
window.addEventListener('resize', function() {
    const container = document.getElementById('mobileToastContainer');
    if (window.innerWidth > 768 && container) {
        container.style.display = 'none';
    }
});
