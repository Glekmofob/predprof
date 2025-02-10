import streamlit as st
import pandas as pd
import json
import os

DATA_FILE = "atms.json"
DEFAULT_CSV_FILE = "Default_atm.csv"

st.title("Управление банкоматами")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_default_data():
    if os.path.exists(DEFAULT_CSV_FILE):
        df = pd.read_csv(DEFAULT_CSV_FILE,sep=';')
        default_data = []
        for index, row in df.iterrows():
            try: 
                atm = {
                    "ID": row[df.columns[0]],  
                    "Номер банкомата": str(row[df.columns[1]]),
                    "Адрес банкомата": row[df.columns[2]],
                    "Coordinates": [(row[df.columns[3]]), (row[df.columns[4]])],  
                }
                default_data.append(atm)
            except (ValueError, TypeError, IndexError) as e:
                st.error(f"Ошибка при обработке строки {index}: {e}. Убедитесь, что координаты X и Y являются числами, а также что CSV файл содержит необходимые столбцы.")
                return []

        return default_data
    else:
        st.error(f"Файл {DEFAULT_CSV_FILE} не найден!")
        return []

if "atm_data" not in st.session_state:
    st.session_state.atm_data = load_data()

if st.button("Загрузить данные по умолчанию"):
    default_data = load_default_data()
    if default_data:
        st.session_state.atm_data = default_data
        st.success("Данные по умолчанию загружены!")
    else:
        st.error("Не удалось загрузить данные по умолчанию.")

if not st.session_state.atm_data:
    df = pd.DataFrame(columns=["ID", "Номер банкомата", "Адрес банкомата", "Координаты X", "Координаты Y"])
else:
    data_for_df = []
    for atm in st.session_state.atm_data:
        row = {
            "ID": atm["ID"],
            "Номер банкомата": atm["Номер банкомата"],
            "Адрес банкомата": atm["Адрес банкомата"],
            "Координаты X": atm["Coordinates"][0],  
            "Координаты Y": atm["Coordinates"][1],  
        }
        data_for_df.append(row)
    df = pd.DataFrame(data_for_df)

st.write("### Таблица банкоматов")
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

if st.button("Сохранить данные"):
    updated_data = []
    for index, row in edited_df.iterrows():
        try:
            atm = {
                "ID": row["ID"],
                "Номер банкомата": row["Номер банкомата"],
                "Адрес банкомата": row["Адрес банкомата"],
                "Coordinates": [float(row["Координаты X"]), float(row["Координаты Y"])],  # [X, Y]
            }
            updated_data.append(atm)
        except (ValueError, TypeError) as e:
            st.error(f"Ошибка при обработке строки {index}: {e}. Убедитесь, что координаты X и Y являются числами.")
            st.stop() 

    st.session_state.atm_data = updated_data
    save_data(st.session_state.atm_data)
    st.success("Данные сохранены!")
