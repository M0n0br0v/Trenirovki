import flet as ft

def main(page: ft.Page):
    page.title = "Trenirovki"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20
    
    def navigate_to_history(e):
        page.route = "/history"
        page.update()
    
    def navigate_to_results(e):
        page.route = "/results"
        page.update()
    
    def navigate_to_workout(e):
        page.route = "/workout"
        page.update()
    
    async def exit_app(e):
        await page.window.destroy()

    title = ft.Text(
        "Добро пожаловать в Trenirovki",
        size=28,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )
     
    create_btn = ft.ElevatedButton(
        content=ft.Text("Создать тренировку"),
        on_click=navigate_to_workout,
        width=250,
        height=50,
    )
    
    history_btn = ft.ElevatedButton(
        content=ft.Text("История тренировок"),
        on_click=navigate_to_history,
        width=250,
        height=50,
    )
    
    results_btn = ft.ElevatedButton(
        content=ft.Text("Посмотреть результаты"),
        on_click=navigate_to_results,
        width=250,
        height=50,
    )
    
    exit_btn = ft.ElevatedButton(
        content=ft.Text("Выйти!"),
        on_click=exit_app,
        width=250,
        height=50,
    )
    
    page.add(
        ft.Column(
            [
                title,
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                create_btn,
                history_btn,
                results_btn,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                exit_btn,
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    
    def route_change(e):
        print(f"Переход на: {page.route}")
    
    page.on_route_change = route_change

ft.app(target=main)