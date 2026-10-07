import flet as ft
from typing import Optional
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

class NotesView():
    """Экран для ввода комментария"""
    def __init__(
        self,
        page: ft.Page,
        notes: Optional[str],
        on_save,
        on_cancel
    ):
        self.page = page
        self.notes = notes
        self.on_save = on_save
        self.on_cancel = on_cancel

    def _save_notes(self, e):
        self.on_save(self.notes)

    def _cancel_notes(self, e):
        self.on_cancel()

    def _change_notes(self, e):
        self.notes=e.control.value

    def build(self) -> ft.View:
        content=ft.Column(
            [
                ft.Text(
                    "Комментарий:",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),
                ft.TextField(
                    value=self.notes if self.notes else "",
                    hint_text="Введите комментарий",
                    multiline=True,
                    min_lines=10,
                    max_lines=30,
                    on_change=self._change_notes
                ),
                ft.Button(
                    content=ft.Text("Сохранить"),
                    on_click=self._save_notes,
                    width=250,
                    height=50
                ),
                ft.Button(
                    content=ft.Text("Отмена"),
                    on_click=self._cancel_notes,
                    width=250,
                    height=50
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        return ft.View(
            route="/notes",
            controls=[content],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def _refresh_ui(self):
        self.page.views[-1] = self.build()

class SelectExercisesView():
    """Формирует экран Select_Exercise_View"""
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
        else:                                                                                      # Создаем пустую переменную, в которой будем хранить добавляемое упражнение
            for exercise in self.exercises_data:
                if exercise["name"] == exercise_name:
                    self.state.exercises.append ({
                        "name": exercise["name"],
                        "type": exercise["type"] if exercise["type"] else None,
                        "sets": []
                    })
                    break                                                                          # Если exrcise_to_add заполнено, то добавляем его в список self.state.exercises
        self._refresh_ui()

    def _get_available_exercises(self) -> list:
        """Возвращает список упражнений, которые еще не добавлены в self.state.exercises"""
        selected_exercises = {                                                                     # Список уже выбранных упражнений
            exercise["name"] for exercise in self.state.exercises
        }
        return [
            exercise for exercise in self.exercises_data
            if exercise ["name"] not in selected_exercises
            and (exercise["type"] == self.state.workout_type
            or exercise["type"] is None)
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

class GymDataView():
    """Формирует экран Gym_Data_View"""
    def __init__(
        self,
        page: ft.Page,
        gym_data: Optional[dict],
        on_save,
        on_cancel
    ):
        self.page = page
        self.is_new = gym_data is None
        self.gym_data = gym_data if gym_data else {"name":"", "notes":""}                          # Данные спортзала из БД
        self.name = self.gym_data["name"]
        self.notes = self.gym_data["notes"]

        # Колбэки
        self.on_save = on_save
        self.on_cancel = on_cancel

    def _change_name(self, e):
        self.name=e.control.value

    def _save_gym_data(self, e):
        self.gym_data["name"] = self.name
        self.gym_data["notes"] = self.notes
        self.on_save()

    def _cancel(self, e):
        self.on_cancel()

    def show_notes_view(self, e):

        def _on_save_notes(notes: str):
            self.notes = notes
            self._refresh_ui()

        def _on_cancel_notes():
            self._refresh_ui()

        notes_view = NotesView(
            page=self.page,
            notes=self.notes,
            on_save=_on_save_notes,
            on_cancel=_on_cancel_notes
        )
        self.page.views.clear()
        self.page.views.append(notes_view.build())
        self.page.update()

    def build(self) -> ft.View:
        content=ft.Column(
            [
                ft.Text(                         # Заголовок "Название спортзала:"
                    "Название спортзала:",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),
                ft.TextField(                    # Название спортзала
                    value=self.gym_data["name"]
                    if self.gym_data["name"]
                    else "",
                    hint_text="Введите название спортзала",
                    on_change=self._change_name
                ),
                ft.Text(                         # Заголовок "Комментарий"   
                    "Комментарий:",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Container(                         # Комментарий
                    content=ft.Text(self.notes),
                    on_click=self.show_notes_view,
                    width=250,
                    height=50
                ),
                ft.Button(                       # Кнопка "Сохранить"
                    content=ft.Text("Сохранить"),
                    on_click=self._save_gym_data,
                    width=250,
                    height=50
                ),
                ft.Button(                       # Кнопка "Отмена"
                    content=ft.Text("Отмена"),
                    on_click=self._cancel,
                    width=250,
                    height=50
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        return ft.View(
            route="/gym_data",
            controls=[content],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def _refresh_ui(self) -> None:                                                                 # Обновляем интерфейс
        self.page.views[-1] = self.build() 

class MainView():
    def __init__(
        self,
        page: ft.Page,
        history_view,   #TODO: убрать колбеки функция, когда все перепишу на классы
        workout_view
    ):
        self.page = page
        self.history_view = history_view
        self.workout_view = workout_view

    async def exit_app(self, e): # Закрывает приложение (привяжем функцию к кнопке "Выйти")
        await self.page.window.destroy()

    def build(self):
        to_history_btn = ft.Button( # Кнопка "История тренировок"
            content = ft.Text("История тренировок"),
            width=250,
            height=50,
            on_click=self.history_view
        ) 
        to_results_btn = ft.Button( # Кнопка "Посмотреть результаты"
            content = ft.Text("Посмотреть результаты"),
            width=250,
            height=50,
        )
        to_workout_view_btn = ft.Button( # Кнопка "Создать тренировку"
            content = ft.Text("Создать тренировку"),
            on_click=self.workout_view,
            width=250,
            height=50                          
        )
        exit_bnt = ft.Button(
            content = ft.Text("Выйти!"),
            on_click=self.exit_app,
            width = 250,
            height = 50
        )
        content = ft.Column(
            [
                ft.Text("Добро пожаловать в Trenirovki", size = 28, weight = ft.FontWeight.BOLD),
                to_history_btn,
                to_results_btn,
                to_workout_view_btn,
                exit_bnt,
            ],
            spacing = 15, # Расстояние между элементами - 15 пунктов,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )
        return ft.View(
            route="/main_view",
            controls=[content],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

class WorkoutView():
    def __init__(
            self,
            page: ft.Page,
            state,
            exercises_data,
            select_gym_view,
            select_workout_type_view,
            show_select_exercises_view,
            show_main_view,
            show_exercise_view
    ):
        self.page = page
        self.state = state
        self.exercises_data = exercises_data
        self.exercises_container = ft.Column(spacing=10)
        self.select_gym_view = select_gym_view
        self.select_workout_type_view = select_workout_type_view
        self.show_select_exercises_view = show_select_exercises_view
        self.show_main_view = show_main_view
        self.show_exercise_view = show_exercise_view

    def add_set(self, exercise_set: dict, exercise: dict) -> None:
        for ex in self.state.exercises:
            if ex == exercise:
                ex["sets"].append({
                    "set_number": len(ex.sets),
                    "weight": exercise_set["weight"],
                    "reps": exercise_set["reps"],
                    "extra": exercise_set["extra"]
                })

    def toggle_exercise(self, exercise_index):                                                       # Сворачивает и разворачивает группы строк одного упражнения
        """
        Функция изменяет значение "expand" для упражнения с соответствующим exercise_index.
        Должна быть привязана к кнопке "Свернуть/Развернуть" (в виде стрелочки) в области с результатами упражнений (смотри макет экрана).
        Справка: Данные из БД будем получать запросом в формате json и добавлять к ним значение "expand"=True.
        """
        self.exercises_data[exercise_index]["expanded"] = not self.exercises_data[exercise_index]["expanded"]
        self.update_exercises_container()
    
    def build_exercise_card(self, exercise, exercise_index):                                        # Формирует группу строк для одного упражнения
        expand_icon = ft.Icon(                                    # Иконка для сворачивания
            ft.Icons.ARROW_DROP_DOWN if exercise["expanded"] else ft.Icons.ARROW_RIGHT
        )
        expand_btn = ft.Container(                                # Кнопка для сворачивания
            content=expand_icon,
            on_click=lambda _, idx=exercise_index: self.toggle_exercise(idx),
            padding=5,
        )
        exercise_header = ft.Row(                                 # Заголовок
            [
                ft.Button(
                    content = ft.Text(exercise["name"]),
                    on_click = lambda _, exercise=exercise: self.show_exercise_view(exercise),
                    width=250,
                    height=50
                ),
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
        set_rows = []
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
                        ),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=5,
                alignment=ft.Alignment.CENTER
            )             

    def update_exercises_container(self):                                                          # Обновляет контейнер с упражнениями
        self.exercises_container.controls.clear()                                                   # Очищаем контейнер с упражнениями
        for index, exercise in enumerate(self.exercises_data):                                      # Перебираем все упражнения в массиве exercises_data
            exercise_card = self.build_exercise_card(exercise, index) # Формируем карточку упражнения
            self.exercises_container.controls.append(exercise_card)    # Добавляем карточку упражнения в контейнер
        self.page.update()

    def build(self) -> ft.View: 
        to_select_gym_view_btn = ft.Button(
            content = ft.Text("Выберите спортзал") if not self.state.gym else ft.Text(self.state.gym),
            on_click=self.select_gym_view,
            width=250,
            height=50
        )
        to_select_workout_type_view_btn = ft.Button(
            content = ft.Text("Выберите тип тренировки") if not self.state.workout_type else ft.Text(self.state.workout_type),
            on_click=self.select_workout_type_view,
            width=250,
            height=50,
        )
        to_notes_btn = ft.Button(
            content = ft.Text("Добавить комментарий"),
            # on_click=lambda _: notes(),
            width=250,
            height=50
        )
        mark_slider = ft.Slider(
            min=2,
            max=5,
            divisions=3,
            label="{value}",
            value=None
        )
        select_exercise_btn = ft.IconButton(
            icon=ft.Icons.EDIT,
            on_click=self.show_select_exercises_view,
            width=150,
            height=50
        )
        close_btn = ft.Button(
            content=ft.Text("Завершить тренировку"),
            on_click=self.show_main_view,
            width=250,
            height=50
        )
        to_results_btn = ft.Button(                                                                # Кнопка "Посмотреть результаты" - открывает экран RESULTS
            content = ft.Text("Посмотреть результаты"),
            width=250,
            height=50,
        )

        workout_view_content = ft.Column(
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
                ft.Row(    # Надпись "Упражнения" и кнопка "Выбрать упражнения"
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
                self.exercises_container,
                to_results_btn,
                close_btn,
                ft.Divider(color=ft.Colors.TRANSPARENT)
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            scroll = ft.ScrollMode.ADAPTIVE,                                                       # Добавляем вертикальную прокрутку, если элементов на экране больше, чем помещается на экране.
            expand=True
        )
        return ft.View(
            [workout_view_content],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

class HistoryView():
    def __init__(
        self,
        page: ft.Page,
        workouts_data,
        show_main_view
    ):
        self.page = page
        self.workouts_data = workouts_data
        self.workouts_container = ft.Column(spacing=10)
        self.show_main_view = show_main_view
        self.workouts_container_headers=ft.Row(
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

    def build_workout_card(self, workout) -> ft.Row:
            return ft.Row(
                [
                    ft.Container(ft.Text(workout["date"]), width=90, alignment=ft.Alignment.CENTER),
                    ft.Container(ft.Text(workout["type"]), width=90, alignment=ft.Alignment.CENTER),
                    ft.Container(ft.Text(workout["mark"]), width=90, alignment=ft.Alignment.CENTER),
                    ft.Container(ft.Text(workout["gym"]), width=120, alignment=ft.Alignment.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
            
    def update_workouts_container(self):
        self.workouts_container.controls.clear()
        self.workouts_container.controls.append(self.workouts_container_headers)
        for workout in self.workouts_data:
            workout_card = self.build_workout_card(workout)
            self.workouts_container.controls.append(workout_card)
        self.page.update()

    def build(self):
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
            on_click=self.show_main_view
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
            self.workouts_container,
            close_btn
        ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
        return ft.View(
                [history_view_content],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

class SelectGymView():
    def __init__(
        self,
        page: ft.Page,
        state: WorkoutState,
        gyms_data: list[dict],
        show_workout_view,
        show_gym_data_view
    ):
        self.page = page
        self.state = state
        self.gyms_data = gyms_data
        self.show_workout_view = show_workout_view
        self.show_gym_data_view = show_gym_data_view

    def select_gym(self, e):
        self.state.gym = e.control.data
        self.show_workout_view() # TODO добавить функционал возврата на RESULTS # Возвращаемся на экран workout

    def edit_gym_data(self, e):
        self.show_gym_data_view(e.control.data)

    def _build_gym_item(self, gym: dict) -> ft.Row:
        return ft.Row(
            [
                ft.Container(     # Пустой контейнер для выравнивания
                    width=150,
                    height=50
                ),
                ft.Button(
                    content=ft.Text(gym["name"]),
                    data=gym["name"],
                    on_click=self.select_gym,
                    width=250,
                    height=50
                ),
                ft.IconButton(
                    icon=ft.Icons.EDIT,
                    data=gym,
                    on_click=self.edit_gym_data,
                    width=150,
                    height=50
                ) 
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def _build_gyms_list(self):                                       # Формирует список элементов таблицы Gyms
        return ft.Column(
            [
                *[self._build_gym_item(gym) for gym in self.gyms_data]
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def build(self):
        back_btn = ft.Button(
            content = ft.Text("Назад"),
            on_click=self.show_workout_view,
            width=250,
            height=50
        )
        select_gym_view_content = ft.Column(
            [
                self._build_gyms_list(),
                back_btn
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        return ft.View(
            route="/select_gym_view",
            controls=[select_gym_view_content],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

class SelectWorkoutTypeView():
    def __init__(
        self,
        page: ft.Page,
        state: WorkoutState,
        show_workout_view
    ):
        self.page = page
        self.state = state
        self.show_workout_view=show_workout_view

    def select_workout_type(self, e):                                                                # Функция получает workout_type из кнопки (параметр data) и открывает WORKOUT
        self.state.workout_type = e.control.data                                    # Получаем значение типа тренировки из кнопки, на которую нажали
        self.show_workout_view()                                                                         # TODO добавить функционал возврата на RESULTS # Возвращаемся на экран workout
    
    def build(self):
        type_btn_push = ft.Button(
            content = ft.Text("Push"),
            data = "Push", # Присваиваем кнопке значение типа тренировки
            on_click=self.select_workout_type,
            width=250,
            height=50,
        )
        type_btn_pull = ft.Button(
            content = ft.Text("Pull"),
            data = "Pull", # Присваиваем кнопке значение типа тренировки
            on_click=self.select_workout_type,
            width=250,
            height=50,
        )
        type_btn_legs = ft.Button(
            content = ft.Text("Legs"),
            data = "Legs", # Присваиваем кнопке значение типа тренировки
            on_click=self.select_workout_type,
            width=250,
            height=50,
        )
        back_btn = ft.Button(
            content = ft.Text("Назад"),
            on_click=self.show_workout_view,
            width=250,
            height=50,
        )
        workout_type_view_content = ft.Column(
            [
                type_btn_push,
                type_btn_pull,
                type_btn_legs,
                back_btn,
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        return ft.View(
                route="/select_workout_type_view",
                controls=[workout_type_view_content],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

class ExerciseView():
    def __init__(
        self,
        page: ft.Page,
        state: WorkoutState,
        exercise: dict,
        show_workout_view
    ):
        self.page = page
        self.state = state
        self.exercise = exercise
        self.show_workout_view = show_workout_view

    def get_exercise_number(self):
        for index, exercise in enumerate(self.state.exercises):
            if exercise is self.exercise:
                return index + 1

    def build(self):
        back_btn = ft.Button(
            content=ft.Text("Тренировка"),
            on_click=self.show_workout_view,
            width=250,
            height=50
        )
        exercise_view_content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Упражнение №" + str(self.get_exercise_number())),
                        ft.Text(self.exercise["name"])
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                back_btn
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        return ft.View(
            route="/exercise_view",
            controls=[exercise_view_content],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

# ========================================
# 2. ТЕСТОВЫЕ ДАННЫЕ
# region =================================
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
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.update()

    def show_view_for_classes(view) -> None:                                                       # TODO: После перехода на ООП удалить функцию show_view и переименовать текущую в show_view
        """Отображает экран для объектов ООП, работающих через ft.View, а не через page.add.controls"""
        page.views.clear()
        page.views.append(view)
        page.update()
    # endregion

    current_workout_state = WorkoutState()                                                         # Создаем объект класса WorkoutState для хранения состояния текущей тренировки

    def show_main_view() -> None:
            main_view = MainView(
                page=page,
                workout_view=show_workout_view,
                history_view=show_history_view
            )
            page.views.clear()
            page.views.append(main_view.build())
            page.update()

    def show_workout_view():
        workout_view = WorkoutView(
            page=page,
            state=current_workout_state,
            exercises_data=exercises_data,
            select_gym_view = show_select_gym_view,
            select_workout_type_view = show_select_workout_type_view,
            show_select_exercises_view = show_select_exercises_view,
            show_main_view = show_main_view,
            show_exercise_view = show_exercise_view
        )
        workout_view.update_exercises_container()
        page.views.clear()
        page.views.append(workout_view.build())
        page.update()

    def show_select_exercises_view() -> None:
        def on_confirm(selected_exercises):
            current_workout_state.exercises = selected_exercises  
            show_workout_view()
        
        def on_cancel():
            show_workout_view()

        select_exercises_view = SelectExercisesView(
            page = page,
            state = current_workout_state,
            exercises_data = exercises_data,
            on_confirm = on_confirm,
            on_cancel = on_cancel
        )
        page.views.clear()
        page.views.append(select_exercises_view.build())
        page.update()

    def show_gym_data_view(gym):
        def on_save():
            show_select_gym_view()

        def on_cancel():
            show_select_gym_view()

        gym_data_view = GymDataView(
            page = page,
            gym_data = gym,
            on_save=on_save,
            on_cancel=on_cancel
        )
        page.views.clear()
        page.views.append(gym_data_view.build())
        page.update()

    def show_select_workout_type_view():
        select_workout_type_view = SelectWorkoutTypeView(
            page = page,
            state = current_workout_state,
            show_workout_view = show_workout_view
        )
        page.views.clear()
        page.views.append(select_workout_type_view.build())
        page.update()

    def show_history_view():
        history_view = HistoryView(
            page = page,
            workouts_data = workouts_data,
            show_main_view=show_main_view
        )
        history_view.update_workouts_container()
        page.views.clear()
        page.views.append(history_view.build())
        page.update()

    def show_select_gym_view():
        select_gym_view = SelectGymView(
            page = page,
            state=current_workout_state,
            gyms_data=gyms_data,
            show_workout_view=show_workout_view,
            show_gym_data_view=show_gym_data_view
        )
        page.views.clear()
        page.views.append(select_gym_view.build())
        page.update()

    def show_exercise_view(exercise):
        exercise_view = ExerciseView(
            page = page,
            state = current_workout_state,
            exercise = exercise,
            show_workout_view = show_workout_view
        )
        page.views.clear()
        page.views.append(exercise_view.build())
        page.update()

    show_main_view()

ft.app(target=main)