from typing import Dict

from fastapi import Request
from fastapi.responses import RedirectResponse

session_info: Dict[str, Dict] = {}


def is_authenticated(request: Request) -> bool:
    return session_info.get(request.session.get('id'), {}).get('authenticated', False)

def add_authentication_layer(failure_redirect="/login"):
    def authentication_wrapper(func):
        def authenticator(self, request: Request):
            if not is_authenticated(request):
                return RedirectResponse(failure_redirect)
            return func(self, request, session_info[request.session['id']])
        return authenticator
    return authentication_wrapper