import streamlit as st
import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Пример страницы",
    page_icon="🏠",
    layout="wide",  # Это расширяет страницу на всю доступную ширину
    initial_sidebar_state="collapsed",  # Меньше места для сайдбара
)

# Проверка наличия df1 в session_state
if "df" not in st.session_state:
    st.warning("CSV файл не загружен. Пожалуйста, загрузите файл на главной странице.")
    df1 = None  # Устанавливаем df1 в None
else:
    df1 = st.session_state.df  # Если df существует, используем его

if df1 is not None:  # Продолжаем только если df1 не None

    user_input = st.number_input("Введите число", min_value=0, max_value=100, value=10)
    if st.button("Получить данные по конкретному банокмату"):
        st.write(f"Вы ввели число: {user_input}")
        col1, col2 = st.columns(2)
        with col1:
            try:
                data = df1[df1.DeviceID == user_input][["DeviceID", "work_time_per"]]
                styled_df = data.style.set_properties(**{"font-size": "30px"})
                st.dataframe(styled_df, width=600)
            except KeyError:
                st.error(f"Столбец 'DeviceID' не найден в DataFrame.")

        with col2:

            df2 = df1[df1.DeviceID == user_input].copy()
            df2["Date"] = pd.to_datetime(
                df2["Date"], format="%Y:%m:%d", errors="coerce"
            )
            df_errors = df2[df2["predicted_has_error"]]

            # Группировка по дате и подсчет количества ошибок в каждый день
            error_counts = df_errors.groupby(df_errors["Date"].dt.date).size()

            # Построение гистограммы
            fig, ax = plt.subplots(figsize=(15, 7))
            error_counts.plot(kind="bar", color="red")

            # Настройка графика
            plt.title("Количество ошибок по дням", fontsize=24)
            plt.xlabel("Дата", fontsize=12)
            plt.ylabel("Количество ошибок", fontsize=22)
            plt.xticks(rotation=45)
            plt.tight_layout()

            st.pyplot(fig)
