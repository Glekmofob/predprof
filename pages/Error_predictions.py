import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

options = ['ПроверкаСостоянияКлавиатуры', 'ПроверкаСостоянияКарт',
       'ОшибкаОбновления', 'ПроверкаЭнергоснабжения', 'ОшибкаПечати',
       'ОбновлениеПрограммногоОбеспечения', 'ТестированиеУстройства',
       'ПроверкаСостоянияСвязи', 'СостояниеУстройстваИзменено',
       'ПроверкаКассеты', 'ОбновлениеБезопасности',
       'ОшибкаВыдачиНаличности', 'ОшибкаТехническая',
       'СостояниеКартриджа', 'СостояниеПриемаКупюр',
       'ОшибкаЖесткогоДиска', 'ЗавершениеТранзакции',
       'ОтказВОбслуживании', 'УстановкаОбновлений', 'ПроверкаОбновлений',
       'СигнализацияОшибки', 'АварийноеВыключение',
       'ПроверкаСистемныхЛогов', 'ОбслуживаниеТребуется',
       'ОшибкаСинхронизацииДанных', 'ТестированиеСистемы',
       'ПроверкаСостоянияПечати', 'ОшибкаСети', 'ЗаменаКартриджа',
       'ПроблемаСоСвязью']

event = st.selectbox('Выберите опцию:', options)


user_input = st.number_input("Введите айди банкомата", min_value=1, max_value=100, value=10)
if st.button('Получить анализ для опр ивента'):

    with open('model.pkl', 'rb') as file:
        loaded_model  = pickle.load(file)
    new_data = pd.DataFrame({
        'datetime': pd.date_range(start='2023-04-11 10:00', periods=1243, freq='h')
    })
    new_data['year'] = new_data['datetime'].dt.year
    new_data['month'] = new_data['datetime'].dt.month
    new_data['day'] = new_data['datetime'].dt.day
    new_data['hour'] = new_data['datetime'].dt.hour
    new_data['minute'] = new_data['datetime'].dt.minute
    new_data['day_of_week'] = new_data['datetime'].dt.dayofweek
    new_data['season'] = ((new_data['month'] % 12 + 3) // 3)

    mas = ['ПроверкаСостоянияКлавиатуры', 'ПроверкаСостоянияКарт',
       'ОшибкаОбновления', 'ПроверкаЭнергоснабжения', 'ОшибкаПечати',
       'ОбновлениеПрограммногоОбеспечения', 'ТестированиеУстройства',
       'ПроверкаСостоянияСвязи', 'СостояниеУстройстваИзменено',
       'ПроверкаКассеты', 'ОбновлениеБезопасности',
       'ОшибкаВыдачиНаличности', 'ОшибкаТехническая',
       'СостояниеКартриджа', 'СостояниеПриемаКупюр',
       'ОшибкаЖесткогоДиска', 'ЗавершениеТранзакции',
       'ОтказВОбслуживании', 'УстановкаОбновлений', 'ПроверкаОбновлений',
       'СигнализацияОшибки', 'АварийноеВыключение',
       'ПроверкаСистемныхЛогов', 'ОбслуживаниеТребуется',
       'ОшибкаСинхронизацииДанных', 'ТестированиеСистемы',
       'ПроверкаСостоянияПечати', 'ОшибкаСети', 'ЗаменаКартриджа',
       'ПроблемаСоСвязью']

    new_data['EventType_encoded'] = mas.index(event)+1

    new_data['id'] = user_input 
    new_data_scaled = new_data[['year', 'month', 'day', 'hour', 'minute', 'day_of_week', 'season', 'EventType_encoded', 'id']]


    predictions_rf_1 = loaded_model.predict(new_data_scaled)
    new_data['predicted_has_error'] = predictions_rf_1
    data_show = new_data[['datetime', 'id', 'predicted_has_error']]
    st.dataframe(data_show, width= 800)