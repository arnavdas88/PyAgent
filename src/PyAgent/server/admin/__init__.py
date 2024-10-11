from nicegui import app, ui, events

import uuid

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from PyAgent.server.admin.components.theme import frame
from PyAgent.server.admin.components import logo
from PyAgent.server.admin.web.utils import sync_control
from PyAgent.server.admin.sessions import is_authenticated, session_info, add_authentication_layer

USERS = [('', ''), ('johndoe', 'password'), ('janedoe', 'password')]


class Admin:
    def __init__(self, app, manager):
        self.manager = manager

        ui.page('/')(self.gui_clients)
        ui.page('/login')(self.login)

        ui.run_with(
            app,
            mount_path='/admin',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
            storage_secret='aR42C^2gi#YlLqZWKvwp!h17',  # NOTE setting a secret is optional but allows for persistent storage per user
        )
    
    async def login(self, request: Request):
        def try_login() -> None:  # local function to avoid passing username and password as arguments
            if (username.value, password.value) in USERS:
                session_info[request.session['id']] = {'username': username.value, 'authenticated': True}
                ui.navigate.to('/')
            else:
                ui.notify('Wrong username or password', color='negative')

        if is_authenticated(request):
            return RedirectResponse('/')

        request.session['id'] = str(uuid.uuid4())  # NOTE this stores a new session ID in the cookie of the client

        with ui.card().classes('absolute-center w-96'):
            with ui.row().classes('center items-center m-auto'):
                logo.header_logo()
            username = ui.input('Username').on('keydown.enter', try_login).classes("w-80 m-auto")
            password = ui.input('Password').props('type=password').on('keydown.enter', try_login).classes("w-80 m-auto")
            ui.button('Log in', on_click=try_login).classes("w-60 m-auto")

    @add_authentication_layer(failure_redirect="/admin/login")
    def gui_clients(self, request: Request, session):
        with frame("Agents"):
            ui.query('body').classes('bg-gradient-to-t from-gray-100 to-gray-200')

            with ui.row().classes('w-full py-12 my-12'):
                with ui.column().classes('w-full px-12 mx-12'):

                    with ui.row().classes("w-full"):
                        with ui.row().classes("w-full"):
                            ui.label('Active Connections').classes("text-2xl text-gray-600")
                            ui.space()
                            sync_control(self.manager.render.refresh)
                        ui.separator()
                        self.manager.render()