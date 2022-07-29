import click
from fnt import Client
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
import tomli
import typing as t
from click.core import Context
from functools import wraps

F = t.TypeVar("F", bound=t.Callable[..., t.Any])


def pp_exceptions(f: F) -> F:
    """Decorator that catches all exceptions and pretty prints it"""
    @wraps(f)
    def wrapper(*args, **kwds):  # type: ignore
        try:
            return f(*args, **kwds)
        except Exception:
            Console().print_exception(suppress=[click])
            return 1

    return wrapper


def make_client(connection: str) -> Client:
    """Factory for an fnt.Client"""
    config_home = Path(str(os.getenv('XDG_CONFIG_HOME')))
    if not config_home:
        config_home = Path(str(os.getenv('HOME'))) / '.config'

    with open(config_home / 'fnt/config.toml', 'rb') as f:
        conf = tomli.load(f)
        if not connection:
            connection = conf['default_connection']
        return Client(**conf['connection'][connection])


def pass_client(f: F) -> F:
    """Decorator that creates and passes a fnt.Client"""
    @wraps(f)
    @click.pass_obj
    def wrapper(obj: dict, *args, **kwds):  # type: ignore
        client = make_client(obj['connection'])
        return f(client, *args, **kwds)

    return wrapper


@click.group()
@click.option('-c',
              '--connection',
              default=None,
              help='Connection name from config.toml.')
@click.pass_context
def main(ctx: Context, connection: str) -> int:
    ctx.ensure_object(dict)
    ctx.obj['connection'] = connection
    return 0


@main.command()
@pass_client
@pp_exceptions
def sysinfo(fnt: Client) -> int:
    """Print business gateway id and systems."""
    gwid = fnt.id()
    systems = fnt.systems()

    cols = ('id', 'system', 'name', 'version')
    table = Table()
    for col in cols:
        table.add_column(col)
    for system in systems:
        table.add_row(*[system[col] for col in cols])

    console = Console()
    console.print(f'Business Gateway ID: {gwid}')
    console.print(table)
    return 0
