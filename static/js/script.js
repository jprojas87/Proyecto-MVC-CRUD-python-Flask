// Confirmación de eliminación
function confirmDelete(userId) {
    if (confirm('⚠️ ¿Estás seguro de que deseas eliminar esta cuenta?\\n\\nEsta acción es PERMANENTE y no se puede deshacer.')) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/web/users/${userId}/delete`;
        document.body.appendChild(form);
        form.submit();
    }
}

// Auto-hide alerts después de 5 segundos
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});

// Validación de formularios
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.user-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const email = form.querySelector('input[type="email"]');
            if (email && !validateEmail(email.value)) {
                e.preventDefault();
                alert('❌ Por favor ingresa un email válido');
                email.focus();
                return false;
            }
        });
    });
});

function validateEmail(email) {
    const re = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    return re.test(email);
}

// Agregar animación de carga en formularios
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '⏳ Procesando...';
            }
        });
    });
});