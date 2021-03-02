# bobolink-cli

bobolink is a small tool that helps user's store bookmarks and search for them later.
More specifically, bobolink provides full text search on the HTML documents of the bookmarks that you've saved. In practice, this allows you to use bobolink to save some links, and later search/return all your links which contain for example "(songbird OR blackbird) AND NOT currawong".

For more information on bobolink in general, please refer to the [website](https://bobolink.me)

bobolink-cli is the command line interface to the public instance 
of the bobolink [backend.](https://github.com/jtanza/bobolink/)

### Installation

```
$ python -m pip install bobolink
```

### Getting Started

For user's without a bobolink account, the fastest way to get going is to run
`bobolink signup` after installation. This, followed by `bobolink configure` is all that is needed in order to start saving and searching your bookmarks.

The cli is heavily documented and can be accessed at anytime directly via 
`bobolink [COMMAND] --help`. Please refer to the terminal session below for an exploration
of what's possible with bobolink.
