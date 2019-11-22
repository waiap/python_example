"""Base API app."""
from pathlib import Path
import configparser
import os

from aiohttp import web
from aiohttp_session import SimpleCookieStorage
from aiohttp_session import setup as setup_aiohttp_session
from cleo import Application
from cleo import Command
import aiohttp
import aiohttp_jinja2
import jinja2
import pygogo

from .routes import setup_routes

PROJ_DIR = Path(__file__).parent


async def setup_aiohttp_client(app):
    """Setup aiohttp client session."""
    app['http_session'] = aiohttp.ClientSession()


def get_app(config='config.ini', debug=False):  # pragma: nocover
    """Get app."""
    app = web.Application()
    app['config'] = configparser.ConfigParser()
    app['config'].read(config)
    app['logger'] = pygogo.Gogo(
        __name__,
        low_formatter=pygogo.formatters.structured_formatter,
        verbose=debug).get_logger()
    app.on_startup.append(setup_aiohttp_client)
    setup_aiohttp_session(app, SimpleCookieStorage())
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(
                             str(PROJ_DIR / 'templates')))
    setup_routes(app)
    return app


class ServerCommand(Command):  # pragma: nocover
    """Base project.

    start_server
        {--host=0.0.0.0 : Host to listen on}
        {--port=8080 : Port to listen on}
        {--config=config.ini : Config file}
        {--debug : Debug and verbose mode}
    """

    def handle(self):
        """Handle command."""
        app = get_app(self.option('config'), self.option('debug'))
        host = os.getenv('HOST', self.option('host'))
        port = int(os.getenv('PORT', self.option('port')))
        web.run_app(app, host=host, port=port)


def main():  # pragma: nocover
    """Main."""
    application = Application()
    application.add(ServerCommand())
    application.run()
