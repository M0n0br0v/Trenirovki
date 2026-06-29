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
            