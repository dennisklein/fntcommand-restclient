import click
from fnt import Client
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
import tomli


@click.group()
@click.option('-c',
              '--connection',
              default=None,
              help='Connection name from config.toml.')
@click.pass_context
def main(ctx, connection) -> int:
    ctx.ensure_object(dict)
    ctx.obj['connection'] = connection
    return 0


def make_client(connection: str) -> Client:
    config_home = Path(str(os.getenv('XDG_CONFIG_HOME')))
    if not config_home:
        config_home = Path(str(os.getenv('HOME'))) / '.config'

    with open(config_home / 'fnt/config.toml', 'rb') as f:
        conf = tomli.load(f)
        if not connection:
            connection = conf['default_connection']
        return Client(**conf['connection'][connection])


@main.command()
@click.pass_obj
def gateway_id(obj: dict) -> int:
    """Print business gateway ID."""
    try:
        connection = obj['connection']
        fnt = make_client(connection)
        click.echo(fnt.id())
        return 0
    except Exception:
        Console().print_exception(suppress=[click])
        return 1


@main.command()
@click.pass_obj
def systems(obj: dict) -> int:
    """Print business gateway systems."""
    try:
        connection = obj['connection']
        fnt = make_client(connection)
        systems = fnt.systems()

        table = Table()
        table.add_column('id')
        table.add_column('system')
        table.add_column('name')
        table.add_column('version')
        for system in systems:
            table.add_row(*[
                system['id'], system['system'], system['name'],
                system['version']
            ])

        Console().print(table)
        return 0
    except Exception:
        Console().print_exception(suppress=[click])
        return 1
