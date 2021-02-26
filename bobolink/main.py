import click
import configparser
from bobolink import api
from pathlib import Path
from termcolor import colored

INI_PATH = str(Path.home()) + '/.bobolink'

@click.group()
def cli():
  '''Bobolink - dump links, search them later.'''
  pass


@cli.command()
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True)
def signup(email, password):
  '''Creates a new bobolink user.'''
  try:
    api.signup(email, password)
    click.echo('Success! Your account has succesfully been created.\n'
    'Please run [bobolink configure] to initialize your environment.')
  except Exception as e:    
    click.echo(f'Error while creating user: {e}')


@cli.command()
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def configure(email, password):
  '''Creates a bobolink credentials file.

  Creates an INI file containing a user's email and API
  token which are used to authenticate all requests made
  from the bobolink CLI.

  Users wishing to refresh their API tokens can simply rerun
  [bobolink configure] at any time.
  '''
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
  '''Reads user credentials from INI file'''
  config = configparser.ConfigParser()
  config.read(f'{INI_PATH}/credentials')

  default = config['default']
  return {'token': default['bobolink_token'],
          'email': default['bobolink_email']}


@cli.command()
@click.option('--get-reset-token', is_flag=True,
              help='Send the requisite reset token to the user\'s email')
def reset_password(get_reset_token):
  '''Resets a users bobolink password.

  User's should first run with [--get-reset-token] in order to generate
  a reset token (required in order to perform a password reset).

  Authentication tokens are invalidated after a password reset. User's
  should run [bobolink configure] in order to generate a new, valid auth token.
  '''
  email = get_creds()['email']
  try:
    if get_reset_token:
      api.send_reset_token(email)
      click.echo(f'Success! Reset token sent to {email}')
    else:
      reset_token = click.prompt('Token', hide_input=True)
      new_password = click.prompt('New Password', hide_input=True, confirmation_prompt=True)
      api.reset_password(email, new_password, reset_token)
      click.echo('Success! Password has been reset.\n'
                'Be sure to run [bobolink configure] to update'
                'your environment with your new password.')
  except Exception as e:
    click.echo(f'Error while resetting password: {e}')


@cli.command()
@click.argument('bookmarks', nargs=-1)
def add(bookmarks):
  '''Adds new bookmarks to a user's store.

  BOOKMARKS should be a whitespace seperated list of
  URLs.

  Bookmarks added here are immediately made searchable
  via [bobolink search].

  Users wishing to refresh the searchable content of a
  bookmark can simply rerun this command with the bookmark URL.
  '''
  try:
    added = api.add_bookmarks(get_creds(), bookmarks)
    click.echo('Success! Added:\n' + '\n'.join(added))
  except Exception as e:
    click.echo(f'Error while adding bookmarks: {e}')


@cli.command()
@click.argument('bookmarks', nargs=-1)
def delete(bookmarks):
  '''Deletes a bookmark from a user's store.

  BOOKMARKS should be a whitespace seperated list of
  URLs.
  '''
  try:
    deleted = api.delete_bookmarks(get_creds(), bookmarks)
    click.echo('Success! Deleted:\n' + '\n'.join(deleted))
  except Exception as e:
    click.echo(f'Error while deleting bookmarks: {e}')


@cli.command()
def export():
  '''Provides a url dump of all a user's stored bookmarks'''
  try:
    bookmarks = api.get_user_bookmarks(get_creds())
    click.echo('\n'.join(bookmarks))
  except Exception as e:
    click.echo(f'Error while exporting bookmarks: {e}')


def format_hit(hit, url_only, field):
  url = f'{colored("[url]", "green")}: {colored(hit["url"], attrs=["underline"])}'

  if url_only or field == "url":
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
@click.option('--field', type=click.Choice(['url', 'content']),
              help='the bookmark field to search on')
@click.option('--url-only', is_flag=True, help='only return the URL of a match')
def search(query, field, url_only):
  '''Searches a query string against a user's bookmark store.

  When no field is supplied, searches the text content of the HTML
  page associated with a user's bookmark.

  When searching on content, an attempt is made to highlight where those
  matches occured in the original HTML. Support for this feature varies
  by terminal.
  '''
  try:
    hits = api.search_bookmarks(get_creds(), query, field)
    formatted = list(map(lambda hit: format_hit(hit, url_only, field), hits))
    click.echo('\n'.join(formatted))
  except Exception as e:
    click.echo(f'Error while searching bookmarks: {e}')
  

if __name__ == "__main__":
  cli()
  