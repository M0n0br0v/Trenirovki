import flet as ft

def main(page: ft.Page):

    text_display = ft.Text("")

    def on_text_change(e):
        text_display.value = e.control.value
        page.update()

    page.views.append(
        ft.View(
            controls=[
                text_display,
                ft.TextField(
                    value="",
                    hint_text="Введите текст",
                    multiline=True,
                    min_lines=10,
                    max_lines=30,
                    on_change=on_text_change
                )
            ]
        )
    )
    page.update()

ft.app(target=main)