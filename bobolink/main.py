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
  '''Creates a new bobolink user.

  Password should be at least 8 characters in length, contain
  at least one lowercase and uppercase letter and one number.
  '''
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
    config['default'] = {'bobolink_email': email,
                         'bobolink_token': token}

    with open(f'{INI_PATH}/credentials', 'w') as f:
      config.write(f)

    click.echo(f'Success! Configuration written to {INI_PATH}.\nBobolink is ready to use.')
  except Exception as e:
    click.echo(f'Error while configuring environment: {e}')

def get_creds():
  config = configparser.ConfigParser()
  config.read(f'{INI_PATH}/credentials')

  default = config['default']
  return {'token': default['bobolink_token'], 
          'email': default['bobolink_email']}  


@cli.command()
@click.argument('bookmarks', nargs=-1)
def add(bookmarks):
  try:
    added = api.add_bookmarks(get_creds(), bookmarks)
    click.echo('Success! Added:\n' + '\n'.join(added))
  except Exception as e:
    click.echo(f'Error while adding bookmarks: {e}')


@cli.command()
@click.argument('bookmarks', nargs=-1)
def delete(bookmarks):
  try:
    deleted = api.delete_bookmarks(get_creds(), bookmarks)
    click.echo('Success! Deleted:\n' + '\n'.join(deleted))
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


def format_hit(hit, url_only):
  url = f'{colored("[url]", "green")}: {colored(hit["url"], attrs=["underline"])}'

  if url_only:
    return url

  arr = []
  for word in hit['content'].split(' '):
    if word.startswith('<b>'):
      word = colored(word.replace('<b>', '').replace('</b>', ''), 'yellow')
    arr.append(word)

  match = f'{colored("[match]", "green")}: {" ".join(arr)}'
  return f'{url}\n{match}'


@cli.command()
@click.argument('query')
@click.option('--field')
@click.option('--url-only', is_flag=True)
def search(query, field, url_only):
  try:
    hits = api.search_bookmarks(get_creds(), query, field)
    formatted = list(map(lambda hit: format_hit(hit, url_only), hits))
    click.echo('\n'.join(formatted))
  except Exception as e:
    click.echo(f'Error while searching bookmarks: {e}')
  

if __name__ == "__main__":
  cli()
  