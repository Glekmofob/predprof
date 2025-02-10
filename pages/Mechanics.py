import streamlit as st
import pandas as pd
import json
import os

DATA_FILE = "mechanics.json"

st.title("Управление механиками")
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 90%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if "mechanics_data" not in st.session_state:
    st.session_state.mechanics_data = load_data()

# Добавляем колонку "В вызове" с типом bool, если её нет в данных
if not st.session_state.mechanics_data:
    df = pd.DataFrame(columns=["ID", "Номер механика", "ФИО механика", "Координата X базирования", "Координата Y базирования", "В вызове"])
else:
    df = pd.DataFrame(st.session_state.mechanics_data)
    if "В вызове" not in df.columns:
        df["В вызове"] = False  # По умолчанию ставим False

st.write("### Таблица механиков")
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

if st.button("Сохранить данные"):
    st.session_state.mechanics_data = edited_df.to_dict("records")
    save_data(st.session_state.mechanics_data)
    st.success("Данные сохранены!")