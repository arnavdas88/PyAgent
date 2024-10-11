import typer, websockets
from typing import List, Annotated
from PyAgent.agent.utils import URL

app = typer.Typer(no_args_is_help=True)

@app.command()
def agent(
    url: Annotated[str, typer.Option(help = "Manager endpoint, the agent connects to.", envvar="MANAGER")], 
    token: Annotated[str, typer.Option(help = "The token lets the agent authenticate with the server.", envvar="TOKEN")], 
    tags: Annotated[List[str], typer.Option(help = "Tags are keywords that show up on the server and helps to categorize different agents.", envvar="TAGS", default_factory=list)], 
    cookies: Annotated[List[str], typer.Option(help = "Cookies are web-cookies used to connect to the server.", envvar="COOKIES", default_factory=list)]
    ):
    """Starts an agent and connects to the server"""

    import asyncio
    from PyAgent.agent.daemon import WebSocketDaemon

    client = WebSocketDaemon(url, token, tags, cookies)
    try:
        asyncio.run(client.connect())
    except KeyboardInterrupt as ex:
        print("Exiting Gracefully !")
    except websockets.InvalidStatusCode as ex:
        if ex.status_code == 404:
            print("Not a valid websocket endpoint !")
        pass
    except Exception as ex:
        pass

@app.command()
def serve(
    name:Annotated[str, typer.Option(help = "The name of a server to uniquely identify it, from the agent.", envvar="NAME")], 
    host:Annotated[str, typer.Option(help = "The host to serve on. For local development in localhost use 127.0.0.1. To enable public access, e.g. in a container, use all the IP addresses available with 0.0.0.0.", envvar="HOST")], 
    port:Annotated[int, typer.Option(help = "The port to serve on. You would normally have a termination proxy on top (another program) handling HTTPS on port 443 and HTTP on port 80, transferring the communication to your app.", envvar="PORT")]
    ):
    """Runs a PyAgent server"""
    import uvicorn
    from PyAgent.server import main

    main.SERVER = name

    try:
        uvicorn.run(main.app, host=host, port=port, )
    except KeyboardInterrupt as ex:
        print("Exiting Gracefully !")


def main() -> None:
    app()

if __name__ == "__main__":
    main()
