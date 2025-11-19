// script.js - VERSIÓN MEJORADA PARA EL NUEVO DISEÑO
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Portal de Suscripciones cargado');
    
    // Elementos del DOM
    const btnLoad = document.getElementById('btnLoad');
    const userIdInput = document.getElementById('userId');
    const statusDiv = document.getElementById('status');
    const dataSection = document.getElementById('subscriptionData');
    const apiStatus = document.getElementById('apiStatus');
    const userTags = document.querySelectorAll('.user-tag');

    // Verificar estado de la API al cargar
    checkAPIStatus();

    // Event Listeners
    btnLoad.addEventListener('click', loadSubscription);
    
    userIdInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            loadSubscription();
        }
    });

    // Quick user tags
    userTags.forEach(tag => {
        tag.addEventListener('click', function() {
            userIdInput.value = this.getAttribute('data-user');
            loadSubscription();
        });
    });

    async function checkAPIStatus() {
        try {
            const response = await fetch('http://127.0.0.1:8000/health');
            if (response.ok) {
                apiStatus.innerHTML = '<i class="fas fa-circle"></i><span>API Conectada</span>';
                apiStatus.classList.add('connected');
            }
        } catch (error) {
            apiStatus.innerHTML = '<i class="fas fa-circle"></i><span>API Desconectada</span>';
            apiStatus.style.color = 'var(--danger)';
        }
    }

    async function loadSubscription() {
        const userId = userIdInput.value.trim();
        
        console.log('🔄 Cargando usuario:', userId);

        if (!userId) {
            showStatus('Por favor ingresa un User ID', 'error');
            return;
        }

        showStatus('Cargando información de la suscripción...', 'loading');
        hideData();

        try {
            const apiUrl = `http://127.0.0.1:8000/subscription/${userId}`;
            console.log('🌐 Request a:', apiUrl);

            const response = await fetch(apiUrl);
            
            console.log('📡 Status:', response.status);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `Error ${response.status}`);
            }

            const subscription = await response.json();
            console.log('✅ Datos recibidos:', subscription);
            
            displaySubscriptionData(subscription);
            showStatus('Suscripción cargada correctamente!', 'success');
            
        } catch (error) {
            console.error('❌ Error:', error);
            showStatus(`Error: ${error.message}`, 'error');
            hideData();
        }
    }

    function displaySubscriptionData(subscription) {
        // Información básica
        document.getElementById('subUser').textContent = subscription.user_id;
        document.getElementById('subEmail').textContent = subscription.email;
        document.getElementById('subPlan').textContent = subscription.plan_type;
        document.getElementById('subPlanText').textContent = subscription.plan_type;
        
        // Estado con badge de color
        const statusElement = document.getElementById('subStatus');
        statusElement.textContent = subscription.status;
        statusElement.className = `status-badge status-${subscription.status}`;
        
        // Fechas formateadas
        document.getElementById('subTrial').textContent = 
            subscription.trial_ends_at ? 
            new Date(subscription.trial_ends_at).toLocaleString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            }) : 
            'No definido';
            
        document.getElementById('subNext').textContent = 
            subscription.next_billing_at ? 
            new Date(subscription.next_billing_at).toLocaleString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            }) : 
            'No definido';
        
        showData();
    }

    function showStatus(message, type) {
        statusDiv.innerHTML = type === 'loading' ? 
            `<div class="spinner"></div><span>${message}</span>` :
            `<span>${message}</span>`;
        
        statusDiv.className = `status-message ${type}`;
        statusDiv.style.display = 'flex';
        
        // Auto-ocultar mensajes de éxito
        if (type === 'success') {
            setTimeout(() => {
                statusDiv.classList.add('hidden');
            }, 3000);
        }
    }

    function showData() {
        dataSection.classList.remove('hidden');
    }

    function hideData() {
        dataSection.classList.add('hidden');
    }

    // Mensaje de bienvenida
    console.log('🚀 Usuarios disponibles: user_001, user_002, user_003, user_004');
});