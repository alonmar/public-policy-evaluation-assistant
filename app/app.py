import streamlit as st
import uuid
from rag import rag

# import db

# Initialize the database
# db.init_db()

# Application title
st.title("Public Policy Evaluation Assistant")

# Section to ask questions
st.header("Question")
question = st.text_input("Write your question here:")

if st.button("Submit question"):
    if not question:
        st.error("No question provided.")
    elif len(question) < 20:
        st.error("The question must be at least 20 characters long.")
    else:
        with st.spinner("Processing your question..."):
            conversation_id = str(uuid.uuid4())
            response = rag(question)
            result = {
                "conversation_id": conversation_id,
                "question": question,
                "response": response,
            }
            # db.save_conversation(conversation_id, question, answer)
        st.success("Question submitted successfully.")
        st.write("Result:")
        st.write(response["answer"])
        st.write("Did you find this answer useful?")
        col1, col2 = st.columns(2)
        if col1.button("👍 Yes"):
            st.success("Thank you for your positive feedback.")
            # db.save_feedback(conversation_id, "positive")
        if col2.button("👎 No"):
            st.error("Thank you for your negative feedback.")
            # db.save_feedback(conversation_id, "negative")
