"""Json-rpc proxy."""
import hashlib
import hmac
import json
import time
import uuid
from urllib.parse import urlunparse

from aiohttp import web
from aiohttp_session import get_session


async def actions(request):
    """Main actions backend.

    This is the endpoint that will *actually* work as a PROXY.
    All the server-to-server calls go here.
    """
    path = str(request.app.router["redirect"].url_for())
    redirect_url = urlunparse((request.scheme, request.host, path, '', '', ''))
    current_url = urlunparse((request.scheme, request.host, "", '', '', ''))

    # This emulates a cart system where payment amount is
    # stored. All of it is stored in a simple session. Have in account
    # that this is for demonstration purposes and your store will have a
    # different system to handle carts
    session = await get_session(request)

    # Key, resource and secret are WAIAP-provided configuration values.
    config = request.app['config']['main']
    key = config.get('key')
    resource = config.get('resource')
    secret = config.get('secret')

    request.app['logger'].info('set_up',
                               extra=dict(key=key,
                                          resource=resource,
                                          secret=secret))

    # Extract JSON data.
    # As it's a JSON-RPC call, we'll need to modify the 'params' key.
    data = await request.json()

    # This is the group_id, the *user identifier*.
    # Users will be uniquely identified with this, their cards will be
    # associated with this ID. It is a *very* important and sensitive
    # parameter.

    # Make sure an authenticated user always sends its own user id.
    # In case the user is not authenticated, this value must be "0" as string.
    # If you really, really need it, you can have a prefix, for example
    # "auth-{user_id"}
    group_id = config['group_id']
    data['params']['group_id'] = group_id

    # Currency and amount of the cart
    data['params']['amount'] = "300"
    data['params']['currency'] = 'EUR'

    # This is the redirect_url, where redirect alternative payment
    # methods will lead.
    # These methods will append a "request_id" and a "method" in the
    # query string
    data['params']['notify'] = {'result': redirect_url}

    # This is not mandatory unless you have more than one terminal for
    # your store.
    data['params']['original_url'] = current_url

    # Order lenght must be <= 12
    data['params']['order'] = uuid.uuid4().hex[:12]

    # Save current action request for later use
    action = data['action']

    data = dict(payload=data,
                mode='sha256',
                key=key,
                resource=resource,
                nonce=str(time.time()).replace('.', '')[:10])

    request.app['logger'].info('sending_data', extra=data)

    signature = hmac.new(secret.encode(),
                         json.dumps(data).encode(),
                         hashlib.sha256).hexdigest()

    # Send payload against WAIAP servers.
    response = await request.app['http_session'].post(
        request.app['config']['main']['environment_url'] +
        'pwall/api/v1/actions',
        headers={
            'Content-Type': 'application/json',
            'Content-Signature': signature
        },
        json=data)

    # Return response as-is, store in session for later use if needed.
    result = await response.json()
    payload = result['result'].get('payload', {})

    # We have requested a sale action, and WAIAP servers have not returned a
    # redirect url. This is a final sale result.
    sale_ok = result['result'].get('code') == '0'
    is_not_dcc = payload.get('code') != "198"
    is_redirect = payload.get('url')

    if action == 'pwall.sale' and not is_redirect and is_not_dcc and sale_ok:
        session['last_response'] = result
        # In this case, a sale has been completed and payment is *confirmed*.
        request.app['logger'].info('sale_processed', extra=result)

    request.app['logger'].info('received_data', extra=result)
    return web.json_response(result)
