// CORREÇÃO: Removido o http://127.0.0.1:5001
// Agora ele vai procurar a rota no próprio servidor do Render
const CONFIG = {
    apiUrl: '/salvar_cotacao'
};

// Máscara de Telefone (Mantida para sua conveniência)
const phoneInput = document.getElementById('phone');
if(phoneInput) {
    phoneInput.addEventListener('input', (e) => {
        let x = e.target.value.replace(/\D/g, '').match(/(\d{0,2})(\d{0,5})(\d{0,4})/);
        e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
    });
}

document.getElementById('contactForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const btn = document.getElementById('submitBtn');
    
    // CORREÇÃO: Certifique-se que esses IDs (name, email, phone...) existem no seu HTML
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
            alert("✅ Solicitação enviada com sucesso! Nossa equipe entrará em contato.");
            document.getElementById('contactForm').reset();
        } else {
            alert("❌ Erro ao salvar solicitação no servidor.");
        }
    } catch (error) {
        // Se cair aqui, é porque o servidor ainda está "acordando" ou o link está errado
        console.error("Erro de conexão:", error);
        alert("🚨 Erro de conexão! O servidor pode estar iniciando. Tente novamente em alguns segundos.");
    } finally {
        btn.disabled = false;
        btn.textContent = 'Solicitar Cotação';
    }
});
