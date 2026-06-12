import flet as ft

def main (page: ft.Page):
# region ==================== ПАРАМЕТРЫ СТРАНИЦЫ ====================
    page.title = 'Trenirovki' # Название окна приложения
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER # Горизонтальное выравнивание по центру
    page.vertical_alignment = ft.MainAxisAlignment.CENTER # Вертикальное выравнивание по центру
    page.padding = 20 # Отступ (вертикальный) между элементами экрана - 20 пунктов
# endregion
    
    def show_view(elements): # ==================== СМЕНА ЭКРАНОВ ====================
        """Очищает текущую страницу, добавляет на страницу элементы из параметров и обновляет страницу"""
        page.controls.clear()
        page.add(*elements)
        page.update()
    
    def main_view(): # ==================== MAIN_VIEW ====================
        async def exit_app(e): # Закрывает приложение (привяжем функцию к кнопке "Выйти")
            await page.window.destroy()
        # region ==================== ЭЛЕМЕНТЫ ИНТЕРФЕЙСА ====================
        to_history_btn = ft.Button( # Кнопка "История тренировок" - открывает экран HISTORY
            content = ft.Text("История тренировок"),
            width=250,
            height=50,
        )

        to_results_btn = ft.Button( # Кнопка "Посмотреть результаты" - открывает экран RESULTS
            content = ft.Text("Посмотреть результаты"),
            width=250,
            height=50,
        )

        to_workout_btn = ft.Button( # Кнопка "Создать тренировку" - открывает экран WORKOUT
            content = ft.Text("Создать тренировку"),
            on_click=lambda _: workout(),
            width=250,
            height=50,                            
        )

        exit_bnt = ft.Button(
            content = ft.Text("Выйти!"),
            on_click=exit_app,
            width = 250,
            height = 50,
        )
        # endregion
        main_content = ft.Column( # =================== СОДЕРЖИМОЕ ЭКРАНА ====================
            # Единственная группа (вертикальная колонка) элементов экрана MAIN
            [
                ft.Text("Добро пожаловать в Trenirovki", size = 28, weight = ft.FontWeight.BOLD),
                to_history_btn,
                to_results_btn,
                to_workout_btn,
                exit_bnt,
            ],
            spacing = 15, # Расстояние между элементами - 15 пунктов,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER # Горизонтальное выравнивание по центру
        )
        show_view([main_content]) # Показываем экран MAIN в конце функции main_view
    
    def workout(): # ==================== WORKOUT ====================
        # region ==================== WORKOUT.ПЕРЕМЕННЫЕ ====================
        gym = "Выберите спортзал" # Создаем переменную gym, в которую будем записывать значение, выбранное в selet_gym. Значение будет выводиться на форме workout.
        exercises_container = ft.Column(spacing=20) # Создаем пустой контейнер для списка упражнений.
        # endregion
        # region ==================== WORKOUT.ФУНКЦИИ ====================
        def toggle_exercise(exercise_index):
            """
            Функция изменяет значение "expand" для упражнения с соответствующим exercise_index.
            Должна быть привязана к кнопке "Свернуть/Развернуть" (в виде стрелочки) в области с результатами упражнений (смотри макет экрана).
            Справка: Данные из БД будем получать запросом в формате json и добавлять к ним значение "expand"=True.
            """
            exercises_data[exercise_index]["expand"] = not exercises_data[exercise_index]["expand"]
        # endregion
        # region ==================== WORKOUT.ЭЛЕМЕНТЫ ИНТЕРФЕЙСА ====================
        to_select_gym_btn = ft.Button(
            content = ft.Text(gym),
            # on_click=lambda _: select_gym(),
            width=250,
            height=50,
        )
        to_workout_type = ft.Button(
            content = ft.Text("Выберите тип тренировки"),
            # on_click=lambda _: workout_type(),
            width=250,
            height=50,
        )
        to_notes_btn = ft.Button(
            content = ft.Text("Добавить комментарий"),
            # on_click=lambda _: notes(),
            width=250,
            height=50,
        )
        mark_slider = ft.Slider( # Слайдер с оценкой от 2 до 5
            min=2,
            max=5,
            divisions=3,
            label="{value}",
            value=None
        )
        select_exerices_btn = ft.Button(
            content = ft.Text("Выбрать"),
            # on_click=lambda _: workout_type(),
            width=150,
            height=50,
        )
        edit_exercise_btn = ft.IconButton(
            icon=ft.Icons.EDIT,  # иконка карандаша
        icon_size=20,
        tooltip="Редактировать упражнения",  # всплывающая подсказка
        #on_click=lambda _:
        )
        # endregion
        
        workout_content = ft.Column( # ==================== WORKOUT.СОДЕРЖИМОЕ ЭКРАНА ====================
            [
                # TODO: заменить на текущую дату и день недели
                ft.Text("Сегодня четверг, 11.06.26", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Место тренировки", size=18),
                to_select_gym_btn,
                ft.Text("Тип тренировки",size=18),
                to_workout_type,
                ft.Text("Комментарий",size=18),
                to_notes_btn,
                # TODO: Добавить автоматический расчет времени тренировки
                ft.Text("Длительность тренировки: 00:00",size=18),
                ft.Row(
                    [
                        ft.Text("Оценка:",size=18),
                        mark_slider
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        ft.Container(width=150),
                        ft.Text("Упражнения", size=28),
                        select_exerices_btn
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                edit_exercise_btn,
                exercises_container
                # pass

            
            
            
            ],
            spacing = 15,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )
       
       
       
       
       
       
       
       
        show_view([workout_content]) # Показываем экран WORKOUT в конце функции WORKOUT





    # ==================== ВЫБИРАЕМ КАКОЙ ЭКРАН ЗАПУСТИТСЯ ПЕРВЫМ В ПРИЛОЖЕНИИ ====================
    main_view() # Показываем экран MAIN при запуске приложения

# ==================== ЗАПУСКАЕМ ПРИЛОЖЕНИЕ ====================
ft.app(target=main)