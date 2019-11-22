import json

import aiohttp_jinja2
from aiohttp_session import get_session


@aiohttp_jinja2.template('checkout.jinja2')
async def checkout(request):
    """Render a fake store with received data from buying form.

    In the event a request_id and a method have been received by
    redirect handler in the query string, render a payment_redirect
    event in the front to finish the operation.

    You might implement this step on a separate page, as long as you
    render the payment wall there too and send the event inmediately
    after.
    """

    session = await get_session(request)
    request_id = session.pop('request_id', None)
    method = session.pop('method', None)
    error = session.pop('error', None)

    result = None
    if (request_id and method) or error:
        # Render it as JSON so we can just send it as a javascript event
        result = json.dumps({
            'error': error,
            'method': method,
            'request_id': request_id
        })

    # Render template with current data
    return {
        "result": result,
        'environment_url': request.app['config']['main']['environment_url']
    }


@aiohttp_jinja2.template('backoffice.jinja2')
async def backoffice(request):
    """Render backoffice.

    It works exactly as the payment wall, requires a payment wall render with a
    "backoffice" config parameter, and will use the same "actions" endpoint.
    """
    return {
        'environment_url': request.app['config']['main']['environment_url']
    }
