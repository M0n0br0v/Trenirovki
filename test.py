import flet as ft

def main(page: ft.Page):
    page.title = "Таблица подходов"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    
    # ==================== ТЕСТОВЫЕ ДАННЫЕ ====================
    exercises_data = [
        {
            "name": "Жим лёжа",
            "expanded": True,
            "sets": [
                {"weight": 80, "reps": 8, "extra": ""},
                {"weight": 80, "reps": 7, "extra": ""},
                {"weight": 75, "reps": 9, "extra": ""},
            ]
        },
        {
            "name": "Присед",
            "expanded": True,
            "sets": [
                {"weight": 100, "reps": 5, "extra": ""},
                {"weight": 100, "reps": 5, "extra": ""},
                {"weight": 95, "reps": 6, "extra": "добивочные"},
            ]
        },
        {
            "name": "Тяга штанги",
            "expanded": False,
            "sets": [
                {"weight": 60, "reps": 10, "extra": ""},
                {"weight": 60, "reps": 9, "extra": ""},
            ]
        },
    ]
    
    exercises_container = ft.Column(spacing=10)
    
    def toggle_exercise(exercise_index):
        exercises_data[exercise_index]["expanded"] = not exercises_data[exercise_index]["expanded"]
        update_exercises_list()
    
    def build_exercise_card(exercise, exercise_index):
        
        # Иконка для сворачивания
        expand_icon = ft.Icon(
            ft.Icons.ARROW_DROP_DOWN if exercise["expanded"] else ft.Icons.ARROW_RIGHT,
            size=24,
        )
        
        # Заголовок
        header = ft.Row(
            [
                ft.Text(exercise["name"]),
                expand_icon
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
        
        header_btn = ft.Container(
            content=header,
            on_click=lambda _, idx=exercise_index: toggle_exercise(idx),
            padding=5,
        )
        
        # Заголовки колонок
        table_headers = ft.Row(
            [
                ft.Container(ft.Text("Вес (кг)", weight=ft.FontWeight.BOLD), width=90, alignment=ft.Alignment.CENTER),
                ft.Container(ft.Text("Повторы", weight=ft.FontWeight.BOLD), width=90, alignment=ft.Alignment.CENTER),
                ft.Container(ft.Text("Доп.", weight=ft.FontWeight.BOLD), width=90, alignment=ft.Alignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        # Строки подходов
        set_rows = []
        for set_data in exercise["sets"]:
            set_row = ft.Row(
                [
                    ft.Container(ft.Text(str(set_data["weight"]), text_align=ft.TextAlign.CENTER), width=90, alignment=ft.Alignment.CENTER),
                    ft.Container(ft.Text(str(set_data["reps"]), text_align=ft.TextAlign.CENTER), width=90, alignment=ft.Alignment.CENTER),
                    ft.Container(ft.Text(set_data["extra"], text_align=ft.TextAlign.CENTER), width=90, alignment=ft.Alignment.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            set_rows.append(set_row)
        
        # Свёрнутое состояние
        if not exercise["expanded"]:
            return ft.Container(
                content=ft.Column([header_btn]),
                padding=10,
                border=ft.Border.all(1, ft.Colors.TRANSPARENT),
                border_radius=10,
                margin=ft.Margin.only(bottom=10),
            )
        
        # Развёрнутое состояние
        return ft.Container(
            content=ft.Column(
                [
                    header_btn,
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    table_headers,
                    ft.Column(set_rows, spacing=5),
                ],
                spacing=5,
            ),
            padding=10,
            border=ft.Border.all(1, ft.Colors.TRANSPARENT),
            border_radius=10,
            margin=ft.Margin.only(bottom=10),
        )
    
    def update_exercises_list():
        exercises_container.controls.clear()
        for idx, exercise in enumerate(exercises_data):
            exercises_container.controls.append(build_exercise_card(exercise, idx))
        page.update()
    
    update_exercises_list()
    
    page.add(
        ft.Column(
            [
                exercises_container,
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)