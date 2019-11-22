WAIAP Payment Wall AIOHTTP example
---------------------------------------------------

WAIAP Payment Wall AIOHTTP Example implementation. Use this a reference of a
complete integration.

Refer to our integration

Usage
-----

This project uses poetry (https://github.com/sdispater/poetry)
After installing poetry, install the project itself (don't worry about
virtualenvs, poetry will do it)::

   poetry install


And launch the server with::

   poetry run pwall_aiohttp start_server


For extra parameters (port, host...) see::

   poetry run pwall_aiohttp start_server --help


Note that this must be served under a FQDN, you could use https://www.ngrok.com
for that matter
