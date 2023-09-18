import json
import openai
import streamlit as st
openai.api_key=st.secrets["openai_key"]


with open("meta.json","r") as f:
    meta=json.load(f)
        
fine_tuned_model_id=meta['fine_tuned_model_id']
system_message=meta['system_content']
chat_name=meta['chat_name']
client_name=meta['client_name']


if __name__=="__main__":

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_message}]

    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message(client_name):
            st.markdown(prompt)

        with st.chat_message(chat_name):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=fine_tuned_model_id,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
