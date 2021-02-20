import click
import configparser
from pathlib import Path
from bobolink import api

INI_PATH = str(Path.home()) + '/.bobolink'

@click.group()
def cli():
  pass


@cli.command()
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True)
def signup(email, password):  
  try:
    api.signup(email, password)
    click.echo('''
    Success! Your account has succesfully been created.
    Please run [bobolink configure] to initialize your
    environment.
    ''')
  except Exception as e:
    click.echo(f'Error while creating user: {e}')


@cli.command()
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True)
def configure(email, password):
  try:
    token = api.get_token(email, password)
    
    Path(INI_PATH).mkdir(exist_ok=True)

    config = configparser.ConfigParser()
    config['default'] = {'bobolink_token': token,
                         'bobolink_email': email}

    with open(INI_PATH + '/credentials', 'w') as f:
      config.write(f)

    click.echo('Success! Configuration written to ' + INI_PATH)
  except Exception as e:
    click.echo(f'Error while configuring environment: {e}')

def get_creds():
  config = configparser.ConfigParser()
  config.read(INI_PATH + '/credentials')
  default = config['default']
  return {'token': default['bobolink_token'], 
          'email': default['bobolink_email']}  


@cli.command()
@click.argument('bookmarks', nargs=-1)
def add(bookmarks):
  try:
    added = api.add_bookmarks(get_creds(), bookmarks)
    click.echo('Success! Added: ' + added)
  except Exception as e:
    click.echo(f'Error while adding bookmarks: {e}')
  

if __name__ == "__main__":
  cli()
  