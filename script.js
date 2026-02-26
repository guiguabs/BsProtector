const CONFIG = {
    apiUrl: '/salvar_cotacao' // Correção essencial para o Render
};

// Máscara de Telefone
const phoneInput = document.getElementById('phone');
if(phoneInput) {
    phoneInput.addEventListener('input', (e) => {
        let x = e.target.value.replace(/\D/g, '').match(/(\d{0,2})(\d{0,5})(\d{0,4})/);
        e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
    });
}

// Envio do Formulário
document.getElementById('contactForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const btn = document.getElementById('submitBtn');
    
    // Dados para o banco de dados
    const formData = {
        nome: document.getElementById('name').value.trim(),
        email: document.getElementById('email').value.trim(),
        telefone: document.getElementById('phone').value.trim(),
        tipo_seguro: document.getElementById('insurance-type').value,
        mensagem: document.getElementById('message').value.trim()
    };

    btn.disabled = true;
    btn.textContent = 'Enviando Dados...';

    try {
        const response = await fetch(CONFIG.apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            alert("✅ Solicitação enviada com sucesso!");
            document.getElementById('contactForm').reset();
        } else {
            alert("❌ Erro ao salvar dados.");
        }
    } catch (error) {
        alert("🚨 O servidor está iniciando. Aguarde 10 segundos e tente novamente.");
    } finally {
        btn.disabled = false;
        btn.textContent = 'Solicitar Cotação';
    }
});