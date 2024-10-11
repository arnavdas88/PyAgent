from urllib.parse import urlparse, urlunparse
import click

class URL(click.ParamType):
    name = "url"

    def convert(self, value, param, ctx):
        if not isinstance(value, tuple):
            value = urlparse(value)
            if value.scheme not in ("ws", "wss"):
                self.fail(
                    f"invalid URL scheme ({value.scheme}). Only HTTP URLs are allowed",
                    param,
                    ctx,
                )
        return urlunparse(value)
