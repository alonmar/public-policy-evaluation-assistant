import streamlit as st
import uuid
from rag import rag

# import db

# Inicializar la base de datos
# db.init_db()

# Título de la aplicación
st.title("Public Policy Evaluation Assistant")

# Sección para hacer preguntas
st.header("Pregunta")
question = st.text_input("Escribe tu pregunta aquí:")

if st.button("Enviar pregunta"):
    if not question:
        st.error("No se proporcionó ninguna pregunta.")
    elif len(question) < 20:
        st.error("La pregunta debe tener al menos 20 caracteres.")
    else:
        with st.spinner("Procesando tu pregunta..."):
            conversation_id = str(uuid.uuid4())
            response = rag(question)
            result = {
                "conversation_id": conversation_id,
                "question": question,
                "response": response,
            }
            # db.save_conversation(conversation_id, question, answer)
        st.success("Pregunta enviada con éxito.")
        st.write("Resultado:")
        st.write(response["answer"])
        st.write("¿Te resultó útil esta respuesta?")
        col1, col2 = st.columns(2)
        if col1.button("👍 Sí"):
            st.success("Gracias por tu feedback positivo.")
            # db.save_feedback(conversation_id, "positive")
        if col2.button("👎 No"):
            st.error("Gracias por tu feedback negativo.")
            # db.save_feedback(conversation_id, "negative")
