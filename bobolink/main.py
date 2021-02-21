import click
import configparser
from bobolink import api
from pathlib import Path
from termcolor import colored

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


@cli.command()
@click.argument('bookmarks', nargs=-1)
def delete(bookmarks):
  try:
    deleted = api.delete_bookmarks(get_creds(), bookmarks)
    click.echo('Success! Deleted: ' + deleted)
  except Exception as e:
    click.echo(f'Error while deleting bookmarks: {e}')


@cli.command()
@click.argument('bookmarks', nargs=-1)
def export(bookmarks):
  try:
    bookmarks = api.get_user_bookmarks(get_creds())
    click.echo('\n'.join(bookmarks))
  except Exception as e:
    click.echo(f'Error while exporting bookmarks: {e}')


def format_hit(hit):
  arr = []
  for word in hit['content'].split(' '):
    if word.startswith('<b>'):
      word = colored(word.replace('<b>', '').replace('</b>', ''), 'red')
    arr.append(word)

  match = f'{colored("match", "green")}: {" ".join(arr)}'
  url = f'{colored("url", "green")}: {colored(hit["url"], attrs=["underline"])}'

  return f'{url}\n{match}'


@cli.command()
@click.argument('query')
def search(query):
  try:
    hits = api.search_bookmarks(get_creds(), query)
    click.echo('\n\n'.join(list(map(format_hit, hits))))
  except Exception as e:
    click.echo(f'Error while searching bookmarks: {e}')
  

if __name__ == "__main__":
  cli()
  