# FUR.IA Chatbot
> Ao avaliador: Está commitado o `.env` com a minha API KEY para fins de testes, favor desconsiderar os passos de criar conta e inserir api key, após o período de avaliação o arquivo será removido do repositório.

O FUR.IA chatbot é um projeto de fã para a organização FURIA e‑sports. Desenvolvido em Python e JavaScript, ele conversa em português com fãs de CS:GO, usando a API de IA Gemini, modelo da Google, para gerar respostas descontraídas e condizentes, e serve tudo por meio de um servidor Flask.

<div align="center">
    <img src="https://github.com/arthurantonello/chatbot-furia/blob/87b2c96226c435c0b88f22e65dcd6f71bb7988e5/static/img/tela_chatbot.png" alt="Tela do formulário pronto" width="900" height="430"/><br>
    <a href="https://chatbot-furia.up.railway.app/" target="_blank">Link para o projeto hospedado</a><br>
    <a href="https://www.youtube.com/watch?v=7eBeU9yoLA4&ab_channel=Arthur" target="_blank">Vídeo demonstração do Chatbot em funcionamento e estruturação</a>
    
</div>


## Funcionalidades
- Interação em tempo real: chat web com interface responsiva.
- Google Gemini (gemini-1.5-flash): gera respostas em PT-BR com temperatura zero e segurança alta.
- Persona Pro Player: voltado ao CS:GO, usa gírias, ensina táticas (como recoil), usa expressões de torcida, etc.
- Indicador de digitação: animação de três pontinhos enquanto a IA pensa.
- Histórico de conversa: sliding window de até 20 trocas para manter contexto sem estourar tokens.

## Estrutura do Projeto
- `fur_ia.py`: Servidor Flask e integração com Gemini
- `static/`
    - `css/style.css`: Estilos da interface de chat
    - `js/script.js`: Lógica front-end (fetch, histórico e typing)
    - `landing.html`: Interface de chat (HTML)
- `.env`: Variáveis de ambiente (não commitado)
- `requirements.txt`: Dependências do projeto
- `README.md`: Documentação do projeto

## Pré-requisitos
- Python 3.8+
- Conta Google com acesso à Gemini API e API Key
- Variáveis de ambiente no arquivo `.env`:
    ```
    GEMINI_API_KEY=seu_api_key_aqui
    ```
- (Opcional) pipenv ou virtualenv para gestão de dependências

## Instalação e Configuração
Clone o repositório:
```
git clone https://github.com/arthurantonello/chatbot-furia.git
cd furia-chatbot
```
### Instalando dependências:
```
pip install -r requirements.txt
```
Crie o arquivo `.env` na raiz com sua chave:
```
GEMINI_API_KEY=SEU_TOKEN_GEMINI
```

## Como Executar
Inicie o backend:
```
python fur_ia.py
```
Abra o navegador em `http://localhost:5000` para acessar a landing page.
Digite sua mensagem e pressione Enter ou clique em Enviar.

## Funcionalidades

### API do Backend
- GET /: serve o arquivo landing.html.
- POST /api/chat
- Request: { "message": "texto do usuário" }
- Response: { "reply": "resposta gerada pela IA" }
- Processa o histórico completo e retorna uma resposta em streaming concatenada.

### Front-end (static/landing.html + script.js)

- HTML/CSS: container fixo, scroll interno no chat e barra de input fixa.
- JavaScript (script.js):
  - Captura eventos de clique e Enter.
  - Adiciona mensagens ao DOM (user e assistant).
  - Mostra indicador de digitação enquanto aguarda resposta.
  - Fetch para /api/chat e tratamento de erros.

## Próximos Passos
- Perfil de usuário: memorização de preferências (role, estilo de jogo).
- RAG: integrar base de dados táticos para dicas detalhadas.
- Multimídia: adicionar diagramas de granadas e GIFs no chat.
- Deploy: empacotar em Docker e publicar em Cloud Run ou Heroku.

> <i>FUR.IA — o coach virtual que entende de jogo e vibra com você!</i>
