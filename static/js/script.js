const janelaChat = document.getElementById('chat-window');
const campoMensagem = document.getElementById('message-input');
const botaoEnviar = document.getElementById('send-btn');

function adicionarMensagem(texto, papel) {
    const elementoMensagem = document.createElement('p');
    elementoMensagem.classList.add('message', papel);
    const balao = document.createElement('span');
    balao.classList.add('bubble');
    balao.textContent = texto;
    elementoMensagem.appendChild(balao);
    janelaChat.appendChild(elementoMensagem);
    janelaChat.scrollTop = janelaChat.scrollHeight;
}

function mostrarIndicadorDigitando() {
    // Remove indicador existente, se houver
    const existente = document.querySelector('.typing');
    if (existente) existente.remove();

    const elementoDigitando = document.createElement('p');
    elementoDigitando.classList.add('message', 'assistant', 'typing');
    for (let i = 0; i < 3; i++) {
        const pontinho = document.createElement('span');
        pontinho.classList.add('dot');
        elementoDigitando.appendChild(pontinho);
    }
    janelaChat.appendChild(elementoDigitando);
    janelaChat.scrollTop = janelaChat.scrollHeight;
    return elementoDigitando;
}

async function enviarMensagem() {
    const texto = campoMensagem.value.trim();
    if (!texto) return;

  // Exibe mensagem do usuário
    adicionarMensagem(texto, 'user');
    campoMensagem.value = '';

  // Exibe indicador de digitando
    const indicador = mostrarIndicadorDigitando();

    try {
        const resposta = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: texto })
        });

    if (!resposta.ok) {
        throw new Error(`Erro HTTP: ${resposta.status}`);
    }

    const dados = await resposta.json();
    // Remove indicador e exibe resposta do bot
    indicador.remove();
    adicionarMensagem(dados.reply, 'assistant');
    } catch (erro) {
    console.error('Erro na requisição:', erro);
    indicador.remove();
    adicionarMensagem('Erro ao conectar ao servidor.', 'assistant');
    }
}

botaoEnviar.addEventListener('click', enviarMensagem);
campoMensagem.addEventListener('keydown', evento => {
    if (evento.key === 'Enter') enviarMensagem();
});
