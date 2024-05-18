'''import streamlit as st
from backend import response  # Importing your backend function

def main():
    st.title("Campus Whiz")

    user_query = st.text_input("Ask your question here:")

    if st.button("Submit"):
        if user_query:
            answer = response(user_query)
            st.text_area("Answer:", answer)
        else:
            st.warning("Please enter a question.")

            

if __name__ == "__main__":
    main()'''

import streamlit as st
from backend import response  # Importing your backend function


st.title("Campus Whiz")

# CSS to style the chat bubbles
st.markdown("""
<style>
/* Chat container */
.container {
    display: flex;
    flex-direction: column;
    margin-bottom: 10px;
}

/* User message */
.user {
    background-color: #1E2761;
    color: white;
    border-radius: 10px;
    padding: 10px;
    margin-right: 30%;
    align-self: flex-start;
}

/* Chatbot message */
.chatbot {
    background-color: #7A2048 ;
    color: white;
    border-radius: 10px;
    padding: 10px;
    margin-left: 30%;
    align-self: flex-end;
}

/* Input bar */
.input-bar {
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: #f1f1f1;
    padding: 10px;
    border-top: 2px solid #dedede;


}
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "history" not in st.session_state:
    st.session_state.history = []
    #st.session_state.history=[('who is the hod of cs department','HOD of cs department is Mrs.Rejimol Robinson R R')]

if "last_entered_query" not in st.session_state:
    st.session_state.last_entered_query = ""

# Display previous queries and responses
for query,response_text in st.session_state.history:
    if query:
        st.markdown(f'<div class="container user">{query}</div>', unsafe_allow_html=True)
    if response_text:
        st.markdown(f'<div class="container chatbot">{response_text}</div>', unsafe_allow_html=True)

# Input bar for user query
user_query = st.text_input("Ask your question here:", key="user_query", help="Press Enter to submit")

if st.button("Submit") or (user_query and st.session_state.last_entered_query != user_query):
    if user_query:
        st.session_state.last_entered_query = user_query
        st.session_state.history.append((user_query, None))
        answer = response(user_query,  history=any)
        st.session_state.history.append((None, answer))
        st.markdown(f'<div class="container chatbot">{answer}</div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter a question.")






