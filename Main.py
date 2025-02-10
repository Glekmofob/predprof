import streamlit as st
import sqlite3
import pandas as pd
import os
import spacy
from collections import Counter


st.title("Streamlit приложение для обслуживания банкоматов")

st.write(
    '<p style="font-size: 44px;">Выберите базу данных:</p>', unsafe_allow_html=True
)
st.write(
    '<p style="font-size: 20px;">Добавить свой csv файл:</p>', unsafe_allow_html=True
)
uploaded_file = st.file_uploader("", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=";")
    df["DeviceID"] = df.DeviceID.str[8:].astype(int)

    df = df[df["Value"].notna()]
    df = df[~(df["Value"].str.isdigit())]
    list = [
        "ВосстановлениеСвязи",
        "ВнесениеНаличных",
        "ВходПользователя",
        "ВыходПользователя",
        "ОжиданиеПользователя",
        "ОшибкаКарт",
        "ОшибкаПриемаКупюр",
        "ПерезагрузкаУстройства",
        "Предупреждение",
        "СбросНастроек",
    ]
    df = df[df.EventType.isin(list) == False]
    df[df.EventType == "ПроверкаСистемныхЛогов"]["Value"].replace(
        {"Ошибок не найдено": "Хорошо"}
    )

    data1 = {
        "log": [
            "Ошибка",
            "Отключено",
            "Техническая ошибка",
            "Техническое",
            "Слабый сигнал",
            "Проблемы",
            "Нет сигнала",
            "Нет денег",
            "Не удалось",
            "Закрыто на обслуживание",
            "Закрыто из-за проблем",
            "Ошибка: не удалось снять 500 рублей.",
            "Сбой работы: транзакция не завершена.",
            "Обработка не выполнена, сбой механизмов",
            "Сбой банкомата, отказ механизма",
            "Устройство отключено",
            "Механизм отключён",
            "Слабая связь",
            "Слабое подключение",
            "Сканирование невозможно, ошибка",
            "В банкомате нет денег",
            "Анализ не завершено, сбой системы",
            "Обработка не завершено, нет данных",
            "Ошибка: недостаточно средств на счете.",
            "Сбой системы: транзакция не закончена.",
            "Отключить банкомат",
            "Принудительное отключение",
            "Проблемы работы",
            "Проблемы обработки",
            "Проблемы оплаты",
            "Проблемы автомата",
            "Потеря пакетов",
            "Потеря данных",
            "Потеря информации",
            "Плохое соединение",
            "Плохой контакт",
            "Плохое",
            "Плохое, отключить",
        ],
        "has_error": [
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
        ],  # Метки для примера
    }
    df_lem = pd.DataFrame(data1)

    nlp = spacy.load("ru_core_news_sm")

    def tokenize_and_lemmatize(text):
        doc = nlp(text)
        return [token.lemma_ for token in doc if not token.is_punct]

    df_lem["lemmas"] = df_lem["log"].apply(tokenize_and_lemmatize)

    error_logs = df_lem[df_lem["has_error"]]["lemmas"]
    all_lemmas = [lemma for sublist in error_logs for lemma in sublist]
    lemma_counter = Counter(all_lemmas)

    common_error_lemmas = [lemma for lemma, count in lemma_counter.most_common(8)]

    def check_for_errors(text):
        tokens = tokenize_and_lemmatize(text)
        for token in tokens:
            if token in common_error_lemmas:
                return True
        return False

    df["predicted_has_error"] = df["Value"].apply(check_for_errors)

    df["time"] = df.Timestamp
    df["datetime"] = updated_df = df["time"].astype("datetime64[ns]")

    df["datetime"] = pd.to_datetime(df["datetime"])

    df["Date"] = df["datetime"].dt.date
    df = df.drop("time", axis=1)
    st.session_state.df = df


if st.button("Использовать стандартную:"):
    # db_path = os.path.join(os.path.dirname(__file__), 'Table.db')

    # conn = sqlite3.connect(db_path)

    # query = 'SELECT * FROM "atm_data";'

    # df = pd.read_sql(query, conn)

    # conn.close()
    with st.spinner("Загружаю базу...", show_time=True):
        df = pd.read_csv("final_verse.csv")
        df["DeviceID"] = df.DeviceID.str[8:].astype(int)
        # df['predicted_has_error'] = df['predicted_has_error'].replace({"Истина": 1, "Ложь": 0})
        df["time"] = df.Timestamp
        df["datetime"] = updated_df = df["time"].astype("datetime64[ns]")
        df["datetime"] = pd.to_datetime(df["datetime"])
        df["Date"] = df["datetime"].dt.date
        st.session_state.df = df
    st.success("Стандартная база загружена!")


if st.button("Получить данные по всем банкоматам"):
    df = st.session_state.df
    st.write(df)

user_input = st.number_input(
    "Айди конкретного банкомата", min_value=0, max_value=100, value=10
)
if st.button("Получить данные по конкретному банкомату"):
    df = st.session_state.df
    st.write(df[df.DeviceID == user_input])
