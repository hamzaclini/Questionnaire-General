import streamlit as st
import pandas as pd
import base64
import datetime
import pymongo
import hmac
from time import sleep

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()

sex_mapping = {'male': 0, 'female': 1}
answers = {}






st.markdown(
        """<style>
        div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 20px;
                }
        </style>
                """, unsafe_allow_html=True)


st.markdown(
    """
    <style>
    .centered_button {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)




#slider_values = [1,2,3,4]
#slider_values = [1,2,3]
#slider_values = [1,2,3,4,5,6]
#slider_strings = ["Très insuffisant", "Insuffisant", "Satisfaisant", "Très satisfaisant"]
#slider_strings = ["Non", "Un peu", "Oui"]
#slider_strings = ["Pas du tout d'accord", "Plutôt pas d'accord", "Plutôt d'accord", "Assez d'accord", "Très d'accord", "Complètement d'accord"]

#def stringify(i:int = 0) -> str:
#    return slider_strings[i-1]

def empty():
    ph.empty()
    sleep(0.01)

def write_data(new_data):

    db = client.Questionnaire
    db.General.insert_one(new_data)

def user_input_values():
    st.write("### Questionnaire:")
    Quest_input = st.text_area("Nom de Questonnaire")
    #st.write(Quest_input)
    st.write("### Entrez les questions:")
    Comp_input = st.text_area("Questions")
    #st.write(Comp_input)
    Comp_list = [item.strip() for item in Comp_input.split("\n\n")]
    
    if(len(Comp_list)==1):
        Comp_list = [item.strip() for item in Comp_input.split("\n")]
        loop = 1
    else:
        loop = len(Comp_list)
    #st.write(len(Comp_list))
    #Comp_list = Comp_input.split(",")
    st.write("### Réponses suggérées:")
    Rep_input = st.text_area("Réponses")
    Rep_list = [item.strip() for item in Rep_input.split("\n")]
    return Quest_input, Comp_list, Rep_list, loop

    #st.write("### Enter Slider Values:")
    #slider_values = st.text_area("Slider Values", "Enter each value separated by a space")

    #st.write("### Enter Slider Strings:")
    #slider_strings = st.text_area("Slider Strings", "Enter each string on a new line")
    


def user_input_features(Questionnaire,Comp, slider_strings, loop):
        st.write(f"""
        # {Questionnaire}
        """)

        slider_values = [i for i in range(1, len(slider_strings) + 1)]
        #slider_strings = ["Très insuffisant", "Insuffisant", "Satisfaisant", "Très satisfaisant"]
        #slider_strings = ["Non", "Un peu", "Oui"]
        #slider_strings = ["Pas du tout d'accord", "Plutôt pas d'accord", "Plutôt d'accord", "Assez d'accord", "Très d'accord", "Complètement d'accord"]

        def stringify(i:int = 0) -> str:
            return slider_strings[i-1]


        st.sidebar.header('Informations')
        surname = st.sidebar.text_input("Nom")
        name = st.sidebar.text_input("Prénom")
        date = st.sidebar.date_input("Date de naissance", datetime.date(2010, 1, 1))
        sex = st.sidebar.selectbox('Sex',('Homme','Femme'))
        #st.write("""## Cet enfant se distingue des autres enfants de son âge de la manière suivante:""")
        if (loop == 1):
            param = Comp[0]
            Comp = Comp[1:]
            for i, question in enumerate(Comp, start=1):
                slider_output = st.select_slider(
                #f":red[{question}]",
                f"{question}",
                options=slider_values,
                value=1,
                format_func=stringify
                )
                answers[f"{param}{i}"] = slider_output
        else:
            for j in range(len(Comp)):
                Compin = [item.strip() for item in Comp[j].split("\n")]
                param = Compin[0]
                Compin = Compin[1:]
                for i, question in enumerate(Compin, start=1):
                    slider_output = st.select_slider(
                    f"{question}",
                    options=slider_values,
                    value=1,
                    format_func=stringify
                    )
                    answers[f"{param}{i}"] = slider_output



        user_data = {'Questionnaire': Questionnaire,
                     'lastName': surname,
                     'firstName': name,
                     'birthDate': date.isoformat(),
                     'sex': sex}
        answers_data = answers

        document = {
        "user": user_data,
        "answers": answers_data
        }
                
        return document


ph = st.empty()
placeholder = st.empty()
if not st.checkbox("Commance"):
    st.empty()
    st.session_state.Quest, st.session_state.Comp, st.session_state.Rep, st.session_state.loop = user_input_values()
else:
    st.empty()
    #st.write("")
    document = user_input_features(st.session_state.Quest, st.session_state.Comp, st.session_state.Rep, st.session_state.loop)
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        button = st.button('Enregisterez')
        st.image("clinicogImg.png", width=200)
    if button:
        write_data(document)
        st.write("""# Merci d'avoir participé(e) à ce questionnaire""")

#if not st.button('Continuer'):
#    Comp = user_input_values()
#else:
#    document = user_input_features(Comp)





    
        

     
     

    

     


     

