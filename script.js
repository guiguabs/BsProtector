<script>
    const CONFIG = {
        apiUrl: 'http://127.0.0.1:5001/salvar_cotacao'
    };

    // Máscara de Telefone
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
        
        const formData = {
            name: document.getElementById('name').value.trim(),
            email: document.getElementById('email').value.trim(),
            phone: document.getElementById('phone').value.trim(),
            "insurance-type": document.getElementById('insurance-type').value,
            message: document.getElementById('message').value.trim()
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
                // APENAS AVISO DE SUCESSO (Sem abrir WhatsApp)
                alert("✅ Solicitação enviada com sucesso! Nossa equipe entrará em contato.");
                document.getElementById('contactForm').reset();
            } else {
                alert("❌ Erro ao salvar solicitação.");
            }
        } catch (error) {
            alert("🚨 Erveifique se o servidor está ligado!");
        } finally {
            btn.disabled = false;
            btn.textContent = 'Solicitar Cotação';
        }
    });
</script>