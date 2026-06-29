import flet as ft
# ========================================
# 1. КЛАССЫ
# ========================================
class WorkoutState():
    """Хранит данные текущей тренировки"""
    def __init__(self):
        self.workout_type = None
        self.gym = None
        self.mark: int = 4
        self.notes = None
        self.exercises = []

class SelectExercisesView():
    """Формирует экран SelectExercise_View"""   
    def __init__(
        self,
        page: ft.Page,
        state: WorkoutState,
        exercises_data: list,
        on_confirm,
        on_cancel
    ):
        self.page = page
        self.state = state
        self.exercises_data = exercises_data                                                       # Данные тренировок из БД
      
        # Колбэки
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

    def select_exercise(self, exercise_name: str):
        """
        Добавляем или удаляем упражнение в state.exercises
        Args:
            exercise_name (str): В параметры принимаем название упражнения (при подключении БД начнем использовать ID)

        Returns:
            None
        """    
        is_selected = any(exercise_name == exercise["name"] for exercise in self.state.exercises)  # Проверяем, есть ли упражнение exercise_name в списке упражнений self.state.exercises
        if is_selected:                                                                            # Если есть - удаляем из списка
            self.state.exercises = [
                exercise for exercise in self.state.exercises if exercise["name"] != exercise_name
            ]
        else:
            exercise_to_add = None                                                                # Создаем пустую переменную, в которой будем хранить добавляемое упражнение
            for exercise in self.exercises_data:
                if exercise["name"] == exercise_name:
                    exercise_to_add = {
                        "name": exercise["name"],
                        "type": exercise["type"] if exercise["type"] else None
                    }
                    break      
        if exercise_to_add:
            self.state.exercises.append(exercise_to_add)                                           # Если exrcise_to_add заполнено, то добавляем его в список self.state.exercises
        self._refresh_ui()

    def _get_available_exercises(self):
        """Возвращает список упражнений, которые еще не добавлены в self.state.exercises"""
        selected_exercises = {                                                                     # Список уже выбранных упражнений
            exercise["name"] for exercise in self.state.exercises
        }
        return [
            exercise for exercise in self.exercises_data
            if exercise ["name"] not in selected_exercises
            and exercise["type"] == self.state.workout_type
            or exercise["type"] is None
        ]

    def _build_available_exercise_item(self, exercise_name: str) -> ft.Row:
        """Создает строку для одного одного упражнения c названием и кнопкой выбора"""
        return ft.Row(
            [
                ft.Container(
                    ft.Text(exercise_name, expand=True),
                    width = 180,
                    alignment=ft.Alignment.CENTER
                ),
                ft.IconButton(
                    icon=ft.Icons.ADD,
                    tooltip="Выбрать упражнение",
                    on_click=lambda _, name=exercise_name: self.select_exercise(name)
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def _build_available_section(self) -> ft.Column:
        """Строит нижнюю область экрана, в которой перечислены доступные к выбору упражнения с возможностью выбора каждого (смотри _build_exercise_item)"""
        available_exercises: list = self._get_available_exercises()
        return ft.Column(
            [
                ft.Text(
                    "Выберите упражнения" if available_exercises else "Нет упражнений данного типа",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),
                *[self._build_available_exercise_item(exercise["name"]) for exercise in available_exercises]
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def _move_up(self, index: int) -> None:
        """Увеличиваем порядок упражнения в списке выбранных на 1"""
        if index > 0: # Нельзя уменьшить индекс первого элемента
            self.state.exercises[index], self.state.exercises[index - 1] = \
            self.state.exercises[index - 1], self.state.exercises[index]
        self._refresh_ui()

    def _move_down(self, index: int):
        """Уменьшаем порядок упражнения в списке выбранных  на 1"""
        if index < len(self.state.exercises) - 1:
            self.state.exercises[index], self.state.exercises[index + 1] = \
            self.state.exercises[index + 1], self.state.exercises[index]
        self._refresh_ui()

    def _remove_selected(self, exercise_name: str):
        self.state.exercises = [
            exercise for exercise in self.state.exercises if exercise["name"] != exercise_name
        ]
        self._refresh_ui()

    def _build_selected_exercise_item(self, exercise_name: str, index: int) -> ft.Row:
        """Создает строку для одного одного упражнения с кнопками перемещения и добавления/удаления"""
        return ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.KEYBOARD_ARROW_UP,
                    on_click=lambda _, idx=index: self._move_up(idx)
                ),
                ft.IconButton(
                    icon=ft.Icons.KEYBOARD_ARROW_DOWN,
                    on_click=lambda _, idx=index: self._move_down(idx)
                ),
                ft.Container(
                    ft.Text(exercise_name, expand=True),
                    width=180
                ),    
                ft.IconButton(
                    icon=ft.Icons.DELETE,
                    tooltip="Убрать упражнение из списка",
                    on_click=lambda _, name=exercise_name: self._remove_selected(name)
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def _build_selected_section (self) -> ft.Column:
        """Строим верхнюю область, в которой перечислены выбранные упражнения в указанной последоватлеьности"""
        selected_exercises: list = self.state.exercises
        return ft.Column(
            [
                ft.Text(
                    "Выбранные упражнения:" if selected_exercises else "Нет выбранных упражнений",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),
                *[self._build_selected_exercise_item(exercise["name"], index) for index, exercise in enumerate(self.state.exercises)]
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def confirm(self, e) -> None:
        self.on_confirm(self.state.exercises)

    def cancel(self, e) -> None:
        self.on_cancel()

    def build(self) -> ft.View:
        content=ft.Column(
            [
                self._build_selected_section(),
                self._build_available_section(),
                ft.Row(
                    [
                        ft.Button(                                                                         # Кнопка "Записать"
                        content=ft.Text("Записать"),
                        on_click=self.confirm,
                        width=250,
                        height=50
                    ),
                        ft.Button(                                                                         # Кнопка "Отмена"
                            content=ft.Text("Отмена"),
                            on_click=self.cancel,
                            width=250,
                            height=50
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        return ft.View(
            route="/select_exercise",
            controls=[content]
        )

    def _refresh_ui(self):                                                                         # Обновляем интерфейс
        self.page.views[-1] = self.build()                                                         # Берем последний экран (текущий) из page.views и обновляем его

# ========================================
# 2. ТЕСТОВЫЕ ДАННЫЕ
# region ========================================
exercises_data = [
    {
        "name": "Жим лёжа",
        "type": "Push",
        "expanded": True,
        "sets": [
            {"weight": 80, "reps": 8, "extra": ""},
            {"weight": 80, "reps": 7, "extra": ""},
            {"weight": 75, "reps": 9, "extra": ""},
        ]
    },
    {
        "name": "Присед",
        "type": "Legs",
        "expanded": True,
        "sets": [
            {"weight": 100, "reps": 5, "extra": ""},
            {"weight": 100, "reps": 5, "extra": ""},
            {"weight": 95, "reps": 6, "extra": "добивочные"},
        ]
    },
    {
        "name": "Тяга штанги",
        "type": "Pull",
        "expanded": False,
        "sets": [
            {"weight": 60, "reps": 10, "extra": ""},
            {"weight": 60, "reps": 9, "extra": ""},
        ]
    },
    {
        "name": "Dragon flag",
        "type": None,
        "expanded": False,
        "sets": [
            {"weight": 0, "reps": 12, "extra": ""},
            {"weight": 0, "reps": 7, "extra": ""},
        ]
    },
    {
        "name": "Ягодичный мостик",
        "type": "Legs",
        "expanded": False,
        "sets": [
            {"weight": 100, "reps": 12, "extra": ""},
            {"weight": 200, "reps": 7, "extra": ""},
        ]
    },
    {
        "name": "Leg extension",
        "type": "Legs",
        "expanded": False,
        "sets": [
            {"weight": 70, "reps": 12, "extra": ""},
            {"weight": 60, "reps": 7, "extra": ""},
        ]
    },
]
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
workouts_data = [
    {
        "id": "1",
        "date": "07.06.26",
        "gym": "DDX",
        "type": "Push",
        "duration_minutes": "112",
        "mark": "4",
        "notes": None
    },
    {
        "id": "2",
        "date": "09.06.26",
        "gym": "DDX",
        "type": "Pull",
        "duration_minutes": "110",
        "mark": "4",
        "notes": None
    },
    {
        "id": "3",
        "date": "11.06.26",
        "gym": "DDX",
        "type": "Legs",
        "duration_minutes": "120",
        "mark": "4",
        "notes": None
    },
    {
        "id": "4",
        "date": "13.06.26",
        "gym": "Петроградец",
        "type": "Push",
        "duration_minutes": "100",
        "mark": "3",
        "notes": "Плохо покачался"
    },
]
# endregion
# ========================================
# 3. ТОЧКА ВХОДА
# ========================================
def main (page: ft.Page):
    # region ======================================== ПАРАМЕТРЫ СТРАНИЦЫ ========================================
    page.title = 'Trenirovki' # Название окна приложения
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER # Горизонтальное выравнивание по центру
    page.vertical_alignment = ft.MainAxisAlignment.CENTER # Вертикальное выравнивание по центру
    page.padding = 20 # Отступ (вертикальный) между элементами экрана - 20 пунктов
  
    def show_view(elements): # ======================================== СМЕНА ЭКРАНОВ ========================================
        """Очищает текущую страницу, добавляет на страницу элементы из параметров и обновляет страницу"""
        page.controls.clear()
        page.add(*elements)
        page.update()

    def show_view_for_classes(view) -> None:                                                    # TODO: После перехода на ООП удалить функцию show_view и переименовать текущую в show_view
        """Отображает экран для объектов ООП, работающих через ft.View, а не через page.add.controls"""
        page.views.clear()
        page.views.append(view)
        page.update()
    # endregion

    current_workout_state = WorkoutState()                                                         # Создаем объект класса WorkoutState для хранения состояния текущей тренировки

    def main_view():
        
        async def exit_app(e): # Закрывает приложение (привяжем функцию к кнопке "Выйти")
            await page.window.destroy()
        
        to_history_btn = ft.Button( # Кнопка "История тренировок" - открывает экран HISTORY
            content = ft.Text("История тренировок"),
            width=250,
            height=50,
            on_click=lambda _: history_view()
        ) 
        to_results_btn = ft.Button( # Кнопка "Посмотреть результаты" - открывает экран RESULTS
            content = ft.Text("Посмотреть результаты"),
            width=250,
            height=50,
        )
        to_workout_view_btn = ft.Button( # Кнопка "Создать тренировку" - открывает экран WORKOUT
            content = ft.Text("Создать тренировку"),
            on_click=lambda _: workout_view(),
            width=250,
            height=50,                            
        )
        exit_bnt = ft.Button(
            content = ft.Text("Выйти!"),
            on_click=exit_app,
            width = 250,
            height = 50,
        )
        main_view_content = ft.Column(
            [                                      # Единственная группа (вертикальная колонка) элементов экрана MAIN
                ft.Text("Добро пожаловать в Trenirovki", size = 28, weight = ft.FontWeight.BOLD),
                to_history_btn,
                to_results_btn,
                to_workout_view_btn,
                exit_bnt,
            ],
            spacing = 15, # Расстояние между элементами - 15 пунктов,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER # Горизонтальное выравнивание по центру
        )
        
        show_view([main_view_content]) # Показывает экран MAIN_VIEW в конце функции main_view  
   
    def workout_view():
        
        exercises_container = ft.Column(spacing=10)                                                # Создаем пустой контейнер для списка упражнений.
        
        def select_exercise(exercise_index):                                                       # Сворачивает и разворачивает группы строк одного упражнения
            """
            Функция изменяет значение "expand" для упражнения с соответствующим exercise_index.
            Должна быть привязана к кнопке "Свернуть/Развернуть" (в виде стрелочки) в области с результатами упражнений (смотри макет экрана).
            Справка: Данные из БД будем получать запросом в формате json и добавлять к ним значение "expand"=True.
            """
            exercises_data[exercise_index]["expanded"] = not exercises_data[exercise_index]["expanded"]
            update_exercises_container()
        def build_exercises_card(exercise, exercise_index):                                        # Формирует группу строк для одного упражнения
            
            expand_icon = ft.Icon(                                    # Иконка для сворачивания
                ft.Icons.ARROW_DROP_DOWN if exercise["expanded"] else ft.Icons.ARROW_RIGHT
            )
            expand_btn = ft.Container(                                # Кнопка для сворачивания
                content=expand_icon,
                on_click=lambda _, idx=exercise_index: select_exercise(idx),
                padding=5,
            )
            exercise_header = ft.Row(                                 # Заголовок
                [
                    ft.Text(exercise["name"]),
                    expand_btn
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            )
            exercise_table_headers = ft.Row(                          # Заголовки колонок
                [
                    ft.Container(
                        ft.Text(
                            "Вес (кг)",
                            weight=ft.FontWeight.BOLD
                        ),
                        width=90,
                        alignment=ft.Alignment.CENTER
                    ),
                    ft.Container(
                        ft.Text(
                            "Повторы",
                            weight=ft.FontWeight.BOLD
                        ),
                        width=90,
                        alignment=ft.Alignment.CENTER
                    ),
                    ft.Container(
                        ft.Text(
                            "Доп.",
                            weight=ft.FontWeight.BOLD
                        ),
                        width=90,
                        alignment=ft.Alignment.CENTER
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )   
            
            # Формируем таблицу с результатами упражнения (строки с весом, основными и дополнительными повторениями)
            set_rows = []                                             # Создаем пустой массив строк для упражнения.
            for set in exercise["sets"]:
                set_row = ft.Row(
                    [
                        ft.Text(set["weight"], width=90, text_align=ft.TextAlign.CENTER),
                        ft.Text(set["reps"], width=90, text_align=ft.TextAlign.CENTER),
                        ft.Text(set["extra"], width=90, text_align=ft.TextAlign.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
                set_rows.append(set_row) # Добавляем строку в массив строк для упражнения.
            if exercise["expanded"] == False: # Свернутое состояние
                return ft.Container(content=exercise_header)  
            else:                             # Развернутое состояние
                return ft.Container(
                    content=ft.Column(
                        [
                            exercise_header,
                            exercise_table_headers,
                            ft.Column(
                                set_rows,
                                spacing=5, 
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=5,
                    alignment=ft.Alignment.CENTER
                )             
        def update_exercises_container():                                                          # Обновляет контейнер с упражнениями
            exercises_container.controls.clear()                                                   # Очищаем контейнер с упражнениями
            for index, exercise in enumerate(exercises_data):                                      # Перебираем все упражнения в массиве exercises_data
                exercise_card = build_exercises_card(exercise, index) # Формируем карточку упражнения
                exercises_container.controls.append(exercise_card)    # Добавляем карточку упражнения в контейнер
            page.update()                                                                          # Обновляем страницу
        def show_select_exercises_view() -> None:
            """Открывает экран выбора упражнений"""
            def on_confirm(selected_exercises):
                current_workout_state.exercises = selected_exercises
                update_exercises_container()    
                workout_view()
            
            def on_cancel():
                workout_view()

            select_exercises_view = SelectExercisesView(
                page = page,
                state = current_workout_state,
                exercises_data = exercises_data,
                on_confirm = on_confirm,
                on_cancel = on_cancel
            )
            show_view_for_classes(select_exercises_view.build())

        to_select_gym_view_btn = ft.Button(
            content = ft.Text("Выберите спортзал") if not current_workout_state.gym else ft.Text(current_workout_state.gym),
            on_click=lambda _: select_gym_view(),
            width=250,
            height=50,
        )
        to_select_workout_type_view_btn = ft.Button(
            content = ft.Text("Выберите тип тренировки") if not current_workout_state.workout_type else ft.Text(current_workout_state.workout_type),
            on_click=lambda _: select_workout_type_view(),
            width=250,
            height=50,
        )
        to_notes_btn = ft.Button(
            content = ft.Text("Добавить комментарий"),
            # on_click=lambda _: notes(),
            width=250,
            height=50,
        )
        mark_slider = ft.Slider(                                                                   # Слайдер с оценкой от 2 до 5
            min=2,
            max=5,
            divisions=3,
            label="{value}",
            value=None
        )
        select_exercise_btn = ft.IconButton(
            icon=ft.Icons.EDIT,
            on_click=lambda _: show_select_exercises_view(),
            width=150,
            height=50
        )
        close_btn = ft.Button(
            content=ft.Text("Завершить тренировку"),
            on_click=lambda _: main_view(),
            width=250,
            height=50
        )
        to_results_btn = ft.Button(                                                                # Кнопка "Посмотреть результаты" - открывает экран RESULTS
            content = ft.Text("Посмотреть результаты"),
            width=250,
            height=50,
        )
        workout_content = ft.Column(
            [
                ft.Text(
                    "Сегодня четверг, 11.06.26",
                    size=28,
                    weight=ft.FontWeight.BOLD), # TODO: заменить на текущую дату и день недели
                ft.Text("Место тренировки", size=18),
                to_select_gym_view_btn,
                ft.Text("Тип тренировки",size=18),
                to_select_workout_type_view_btn,
                ft.Text("Комментарий",size=18),
                to_notes_btn,
                ft.Text("Длительность тренировки: 00:00",size=18),                                 # TODO: Добавить автоматический расчет времени тренировки
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
                        ft.Text(
                            "Упражнения",
                            size=28,
                            weight=ft.FontWeight.BOLD),
                        select_exercise_btn
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                exercises_container,
                to_results_btn,
                close_btn,
                ft.Divider(color=ft.Colors.TRANSPARENT)
            ],
            spacing = 10,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            scroll = ft.ScrollMode.ADAPTIVE,                                                       # Добавляем вертикальную прокрутку, если элементов на экране больше, чем помещается на экране.
            expand=True
        )
        update_exercises_container()
        show_view([workout_content])                                                               # Показываем экран WORKOUT в конце функции WORKOUT
    
    def select_workout_type_view():
       
        def select_workout_type(e):                                                                # Функция получает workout_type из кнопки (параметр data) и открывает WORKOUT
            current_workout_state.workout_type = e.control.data                                    # Получаем значение типа тренировки из кнопки, на которую нажали
            workout_view()                                                                         # TODO добавить функционал возврата на RESULTS # Возвращаемся на экран workout
        
        type_btn_push = ft.Button(
            content = ft.Text("PUSH"),
            data = "Push", # Присваиваем кнопке значение типа тренировки
            on_click=select_workout_type,
            width=250,
            height=50,
        )
        type_btn_pull = ft.Button(
            content = ft.Text("PULL"),
            data = "Pull", # Присваиваем кнопке значение типа тренировки
            on_click=select_workout_type,
            width=250,
            height=50,
        )
        type_btn_legs = ft.Button(
            content = ft.Text("LEGS"),
            data = "Legs", # Присваиваем кнопке значение типа тренировки
            on_click=select_workout_type,
            width=250,
            height=50,
        )
        back_btn = ft.Button(
            content = ft.Text("Назад"),
            on_click=lambda _: workout_view(),
            width=250,
            height=50,
        )
        workout_type_content = ft.Column(
            [
                type_btn_push,
                type_btn_pull,
                type_btn_legs,
                back_btn,
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        show_view([workout_type_content])       
    
    def select_gym_view():
       
        def select_gym(e):
            current_workout_state.gym = e.control.data
            workout_view() # TODO добавить функционал возврата на RESULTS # Возвращаемся на экран workout
        def build_gyms_list():                                       # Формирует список элементов таблицы Gyms
            gyms_list = []
            for gym in gyms_data:
                gym_btn = ft.Button(
                    content=ft.Text(gym["name"]),
                    data=gym["name"],
                    on_click=select_gym,
                    width=250,
                    height=50)
                gyms_list.append(gym_btn)
            return gyms_list
        
        select_gym_content = ft.Column(
            [*build_gyms_list()],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        show_view([select_gym_content])
   
    def history_view():

        workouts_container = ft.Column(spacing=10)

        def build_workouts_card(workout): 
            return ft.Row(
                [
                    ft.Container(ft.Text(workout["date"]), width=90, alignment=ft.Alignment.CENTER),
                    ft.Container(ft.Text(workout["type"]), width=90, alignment=ft.Alignment.CENTER),
                    ft.Container(ft.Text(workout["mark"]), width=90, alignment=ft.Alignment.CENTER),
                    ft.Container(ft.Text(workout["gym"]), width=120, alignment=ft.Alignment.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
            
        def update_workouts_container():
            workouts_container.controls.clear()
            workouts_container.controls.append(workouts_container_headers)
            for workout in workouts_data:
                workout_card = build_workouts_card(workout)
                workouts_container.controls.append(workout_card)
            page.update()

        back_list_btn=ft.Button(
            content = ft.Text("Назад"),
            width=250,
            height=50,
            #on_click= # TODO
        )
        forward_list_btn=ft.Button(
            content = ft.Text("Далее"),
            width=250,
            height=50,
            #on_click= # TODO
        )
        close_btn=ft.Button(
            content = ft.Text("Закрыть"),
            width=250,
            height=50,
            on_click=lambda _: main_view()
        )       
        workouts_container_headers=ft.Row(
            [
                ft.Container(
                    ft.Text(
                        "Дата",
                        weight=ft.FontWeight.BOLD
                    ),
                    width=90,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Container(
                    ft.Text(
                        "Тип",
                        weight=ft.FontWeight.BOLD
                    ),
                    width=90,
                    alignment=ft.Alignment.CENTER
                ),
                ft.Container(
                    ft.Text(
                        "Оценка",
                    weight=ft.FontWeight.BOLD
                    ),
                    width=90,
                    alignment=ft.Alignment.CENTER
                ),
                ft.Container(
                    ft.Text(
                        "Зал",
                    weight=ft.FontWeight.BOLD
                    ),
                    width=120,
                    alignment=ft.Alignment.CENTER
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        history_view_content = ft.Column(
            [
                ft.Row(
                    [
                        back_list_btn,
                        ft.Container(width=150),
                        forward_list_btn,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                workouts_container,
                close_btn
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )

        update_workouts_container()
        show_view([history_view_content])
    
    main_view()                                                                                    # Запускаем функцию main_view() при старте приложения (показываем экран MAIN_VIEW).

ft.app(target=main)                                                                                # Запускаем приложение Flet и передаем в него функцию main() как точку входа.
