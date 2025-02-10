import streamlit as st
import json
import os
from streamlit.components.v1 import html

DATA_FILE = "atms.json"
ROUTE_FILE = "route.json"
MECHANICS_FILE = "mechanics.json"

st.title("Карта банкоматов и управление механиками")


# Загрузка данных о банкоматах
def load_atm_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


# Загрузка данных о механиках
def load_mechanics_data():
    if os.path.exists(MECHANICS_FILE):
        with open(MECHANICS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


# Сохранение данных о механиках
def save_mechanics_data(data):
    with open(MECHANICS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Сохранение маршрута
def save_route(route_data):
    with open(ROUTE_FILE, "w", encoding="utf-8") as file:
        json.dump(route_data, file, ensure_ascii=False, indent=4)


# Загрузка маршрута
def load_route():
    if os.path.exists(ROUTE_FILE):
        with open(ROUTE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


# Инициализация данных
atm_data = load_atm_data()
mechanics_data = load_mechanics_data()
route_data = load_route()

# Инициализация маршрута в session_state
if "route_data" not in st.session_state:
    st.session_state.route_data = route_data
if "selected_mechanic_id" not in st.session_state:
    st.session_state.selected_mechanic_id = None


# Функция для удаления банкомата из маршрута
def remove_atm_from_route(atm_id_to_remove):
    st.session_state.route_data = [
        atm for atm in st.session_state.route_data if atm["ID"] != atm_id_to_remove
    ]
    save_route(st.session_state.route_data)
    st.success(f"Банкомат {atm_id_to_remove} удален из маршрута!")


# Функция для добавления банкомата в маршрут
def add_atm_to_route(selected_atm):
    if selected_atm["Coordinates"] not in [
        item["Coordinates"] for item in st.session_state.route_data
    ]:
        st.session_state.route_data.append(
            {
                "ID": selected_atm["ID"],
                "Номер банкомата": selected_atm["Номер банкомата"],
                "Адрес банкомата": selected_atm["Адрес банкомата"],
                "Coordinates": selected_atm["Coordinates"],
            }
        )
        save_route(st.session_state.route_data)
        st.success(f"Банкомат {selected_atm['ID']} добавлен в маршрут!")
    else:
        st.warning(f"Банкомат {selected_atm['ID']} уже добавлен в маршрут!")


# Отрисовка интерфейса для управления банкоматами
def draw_atm_management_interface():
    st.write("### Добавить банкомат в маршрут")
    available_atm_ids = [""] + [
        atm["ID"]
        for atm in atm_data
        if atm["ID"] not in [r["ID"] for r in st.session_state.route_data]
    ]
    selected_atm_id = st.selectbox(
        "Выберите ID банкомата для добавления в маршрут:", options=available_atm_ids
    )
    if selected_atm_id:
        selected_atm = next(
            (atm for atm in atm_data if atm["ID"] == selected_atm_id), None
        )
        if selected_atm:
            st.success(
                f"Выбран банкомат для добавления: {selected_atm['Номер банкомата']}, {selected_atm['Адрес банкомата']}"
            )
            add_atm_to_route(selected_atm)
            st.rerun()

    st.write("### Удалить банкомат из маршрута")
    atm_to_remove = st.selectbox(
        "Выберите ID банкомата для удаления:",
        options=[""] + [atm["ID"] for atm in st.session_state.route_data],
    )
    if atm_to_remove:
        if st.button(f"Удалить {atm_to_remove} из маршрута"):
            remove_atm_from_route(atm_to_remove)
            st.rerun()


# Отрисовка интерфейса для управления механиками
def draw_mechanics_management_interface():
    st.write("### Управление механиками")

    # Доступные механики (не в вызове)
    available_mechanics = [m for m in mechanics_data if not m.get("В вызове", False)]
    st.write("#### Доступные механики:")

    if available_mechanics:
        mechanic_names = [
            f"{m['ФИО механика']} (ID: {m['ID']})" for m in available_mechanics
        ]
        selected_mechanic = st.selectbox(
            "Выберите механика для назначения:", [""] + mechanic_names
        )

        if selected_mechanic:
            mechanic_id = selected_mechanic.split("(ID: ")[1][:-1]
            st.write(f"Выбран механик ID: {mechanic_id}")
            st.session_state.selected_mechanic_id = mechanic_id

        else:
            st.session_state.selected_mechanic_id = None

    else:
        st.info("Нет доступных механиков.")
        st.session_state.selected_mechanic_id = None

    # Механики в вызове
    busy_mechanics = [m for m in mechanics_data if m.get("В вызове", False)]
    st.write("#### Механики в вызове:")
    if busy_mechanics:
        for mechanic in busy_mechanics:
            st.write(f"- {mechanic['ФИО механика']} (ID: {mechanic['ID']})")
    else:
        st.info("Нет механиков в вызове.")

    # Кнопка "Отправить в маршрут"
    if st.button("Отправить в маршрут"):
        if (
            st.session_state.selected_mechanic_id is not None
            and st.session_state.route_data
        ):
            # Очистить маршрут
            st.session_state.route_data = []
            save_route(st.session_state.route_data)
            st.success("Маршрут очищен!")

            # Поменять позицию "В вызове" на True
            for mechanic in mechanics_data:
                if str(mechanic["ID"]) == st.session_state.selected_mechanic_id:
                    mechanic["В вызове"] = True
                    break
            save_mechanics_data(mechanics_data)
            st.success(
                f"Механик {st.session_state.selected_mechanic_id} отправлен в маршрут!"
            )
            st.rerun()

        else:
            st.warning(
                "Выберите механика и сформируйте маршрут, прежде чем отправлять в маршрут!"
            )


# Главное меню
menu = st.sidebar.selectbox(
    "Выберите действие:", ["Управление банкоматами", "Управление механиками"]
)

if menu == "Управление банкоматами":
    draw_atm_management_interface()
elif menu == "Управление механиками":
    draw_mechanics_management_interface()

# Отображение текущего маршрута
st.write("### Текущий маршрут:")
if st.session_state.route_data:
    for atm in st.session_state.route_data:
        st.write(f"- {atm['Номер банкомата']}, {atm['Адрес банкомата']}")
else:
    st.info("Маршрут пока пуст.")


# Отображение карты банкоматов
if not atm_data:
    st.warning(
        "Нет данных о банкоматах. Пожалуйста, добавьте данные на странице 'Управление банкоматами'."
    )
else:
    # Check if either mechanic is not selected OR route is empty
    if st.session_state.selected_mechanic_id is None or not st.session_state.route_data:
        route_coordinates = []  # Empty route_coordinates

        js_code = f"""
        <div id="map" style="width: 100%; height: 500px;"></div>
        <script src="https://api-maps.yandex.ru/2.1/?apikey=YOUR_API_KEY&lang=ru_RU"></script>
        <script>
            ymaps.ready(function () {{
                const map = new ymaps.Map("map", {{
                    center: [55.751244, 37.618423],
                    zoom: 10,
                }});
                const atmData = {json.dumps(atm_data)};

                atmData.forEach(atm => {{
                    if (atm.Coordinates && atm.Coordinates.length === 2) {{
                        const marker = new ymaps.Placemark(
                            atm.Coordinates,
                            {{
                                balloonContent: `<b>Номер банкомата:</b> ${{atm["Номер банкомата"]}}<br><b>Адрес:</b> ${{atm["Адрес банкомата"]}}`
                            }}
                        );
                        map.geoObjects.add(marker);
                    }} else {{
                        console.error('Некорректные координаты для банкомата:', atm);
                    }}
                }});
            }});
        </script>
        """
        html(js_code, width=700, height=600)

    else:  # Both mechanic and route are selected
        # Получаем координаты базирования из mechanics.json
        selected_mechanic = next(
            (
                m
                for m in mechanics_data
                if str(m["ID"]) == st.session_state.selected_mechanic_id
            ),
            None,
        )
        if selected_mechanic:
            base_x = float(selected_mechanic["Координата X базирования"])
            base_y = float(selected_mechanic["Координата Y базирования"])
            base_coordinates = [base_y, base_x]  # Yandex Maps: [широта, долгота]
            mechanic_name = selected_mechanic["ФИО механика"]
        else:
            st.warning("Механик не найден!")
            base_coordinates = [55.751244, 37.618423]  # Москва по умолчанию
            mechanic_name = "Неизвестный механик"

        route_coordinates = [
            atm["Coordinates"] for atm in st.session_state.route_data
        ]  # Используем st.session_state.route_data

        # Добавляем координаты базирования в начало маршрута, если маршрут не пуст
        if route_coordinates:
            route_coordinates = [base_coordinates] + route_coordinates

        js_code = f"""
        <div id="map" style="width: 100%; height: 500px;"></div>
        <script src="https://api-maps.yandex.ru/2.1/?apikey=19f74819-3ae0-4303-903f-5b69a4b3c2d7&lang=ru_RU"></script>
        <script>
            ymaps.ready(function () {{
                const map = new ymaps.Map("map", {{
                    center: [55.751244, 37.618423],
                    zoom: 10,
                }});
                const atmData = {json.dumps(atm_data)};
                const routeData = {json.dumps(st.session_state.route_data)};
                const routeCoordinates = {json.dumps(route_coordinates)};
                const baseCoordinates = {json.dumps(base_coordinates)};
                const mechanicName = "{mechanic_name}";

                // Function to add a single ATM marker with custom balloon content
                function addAtmMarker(coords, balloonContent) {{
                    const marker = new ymaps.Placemark(
                        coords,
                        {{
                            balloonContent: balloonContent
                        }}
                    );
                    map.geoObjects.add(marker);
                }}

                // Show only route points
                if (baseCoordinates) {{
                    addAtmMarker(baseCoordinates, `<b>Место базирования механика:</b><br> ${{mechanicName}}`);
                }}

                for (let i = 1; i < routeCoordinates.length; i++) {{
                    const atm = routeData[i - 1]; // Adjust index because base coordinate is prepended
                    if (atm && atm.Coordinates) {{
                        addAtmMarker(atm.Coordinates, `<b>Номер банкомата:</b> ${{atm["Номер банкомата"]}}<br><b>Адрес:</b> ${{atm["Адрес банкомата"]}}`);
                    }}
                }}

                // Add route to map
                ymaps.route(routeCoordinates, {{
                    mapStateAutoApply: true,
                    routingMode: 'auto'
                }}).then(function (route) {{
                    map.geoObjects.add(route);
                    map.setBounds(route.getBounds(), {{
                        checkZoomRange: true,
                        zoomMargin: 5
                    }});
                }});
            }});
        </script>
        """
        html(js_code, width=700, height=600)
