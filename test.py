import flet as ft

gyms_data = [
    {
        "id": 1,
        "name": "DDX",
        "notes": "Hype",
    },
    {
        "id": 2,
        "name": "Петроградец",
        "notes": "Alma Mater",
    },
    {
        "id": 3,
        "name": "LifeGym (Первоуральск)",
        "notes": "Помню с кем ползали",
    },
]

def main (page: ft.Page):
# region ======================================== ПАРАМЕТРЫ СТРАНИЦЫ ========================================
    page.title = 'Trenirovki' # Название окна приложения
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER # Горизонтальное выравнивание по центру
    page.vertical_alignment = ft.MainAxisAlignment.CENTER # Вертикальное выравнивание по центру
    page.padding = 20 # Отступ (вертикальный) между элементами экрана - 20 пунктов
# endregion
    def show_view(elements): # ======================================== СМЕНА ЭКРАНОВ ========================================
        """Очищает текущую страницу, добавляет на страницу элементы из параметров и обновляет страницу"""
        page.controls.clear()
        page.add(*elements)
        page.update() 
    

    def select_gym(): # ________________________________________ SELECT_GYM ________________________________________
        def build_gyms_list(): # Формирует список элементов таблицы Gyms
            gyms_list = []
            for gym in gyms_data:
                gym_btn = ft.Button(content=ft.Text(gym["name"]), width=250, height=50)
                gyms_list.append(gym_btn)
            return gyms_list
        
        select_gym_content = ft.Column([*build_gyms_list()], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        show_view([select_gym_content])
    select_gym()

ft.app(target=main)