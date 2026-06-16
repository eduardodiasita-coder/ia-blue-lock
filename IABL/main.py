import streamlit as st
import google.generativeai as genai

# 1. Configuração visual da página web
st.set_page_config(page_title="Blue Lock Ego Chat", page_icon="⚽", layout="centered")
st.title("⚽ Blue Lock Ego Chat")
st.write("Converse com a IA mais egoísta e fissurada no projeto Blue Lock!")

# 2. Configurar a Chave (Cérebro)
MINHA_CHAVE = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=MINHA_CHAVE)

# 3. Ler o arquivo de texto (Memória)
with open("bluelock.txt", "r", encoding="utf-8") as f:
    contexto_blue_lock = f.read()

# 4. Configurar as regras da IA
instrucoes_ia = f"""
Você é uma inteligência artificial que é fã fissurada e obcecada pelo anime/mangá Blue Lock.
Você sabe absolutamente tudo sobre a obra e responde de forma muito empolgada em português, usando gírias de futebol e falando sobre o ego dos jogadores.
Use estritamente as informações abaixo como sua base de conhecimento principal:
{contexto_blue_lock}
Se o usuário perguntar algo que não está no texto acima, use seu conhecimento geral sobre Blue Lock, mas mantenha sempre a personalidade de fã egoísta e empolgada.
"""

model = genai.GenerativeModel(
    model_name="gemini-3.5-flash",
    system_instruction=instrucoes_ia
)

# 5. Criar o histórico do chat na tela para não sumir
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar as mensagens antigas na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Caixa de entrada para o usuário digitar
if prompt := st.chat_input("Pergunte algo sobre Blue Lock..."):
    # Mostra o que você digitou
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Pede a resposta para a IA e mostra na tela
    with st.chat_message("assistant"):
        resposta = model.generate_content(prompt)
        st.markdown(resposta.text)
    st.session_state.messages.append({"role": "assistant", "content": resposta.text})