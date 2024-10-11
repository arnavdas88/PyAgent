from nicegui import ui


def sync_control(refreshable_obj):
    timer = ui.timer(1, refreshable_obj)

    ui.button(icon="sync_disabled", on_click=timer.deactivate).props('outline round').bind_visibility_from(timer, 'active', value=True)
    ui.button(icon="sync", on_click=timer.activate).props('outline round').bind_visibility_from(timer, 'active', value=False)
