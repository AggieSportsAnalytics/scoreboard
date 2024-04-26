import app as st

st.title('Hello Streamlit!')

name = st.text_input("Enter your name", "")

if st.button('Greet'):
    st.write(f'Hello {name}, welcome to Streamlit!')

# To run the app, save this script as app.py and use the following command:
# streamlit run app.py
