from nicegui import ui


def header_logo():
    # ui.icon("military_tech").props("outlined").classes('text-5xl').style('color: #6E93D6;')
    # ui.image('imgs/Logo - Light.png').classes('w-32')
    ui.label("PyAgent Admin").classes('text-5xl').style('color: #6E93D6; font-size: 200%; font-weight: 300')

def dark_header_logo():
    # ui.icon("military_tech").props("outlined").classes('text-5xl').style('color: #6E93D6;')
    # ui.image('imgs/Logo - Dark.png').classes('w-32')
    ui.label("PyAgent Admin").classes('text-5xl').style('color: #6E93D6; font-size: 200%; font-weight: 300')
