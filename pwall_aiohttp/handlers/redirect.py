from aiohttp import web
from aiohttp_session import get_session


async def redirect(request):
    """Redirect reception endpoint

    Set request_id for operation confirmation on a session
    and return to checkout page to complete the payment.

    Instead of checkout page, *any* page that renders the payment wall
    and sends out a payment_wall_process_redirect event is valid
    """
    session = await get_session(request)
    session['request_id'] = request.query.get('request_id')
    session['method'] = request.query.get('method')
    session['error'] = request.query.get('error')
    raise web.HTTPFound(request.app.router['checkout'].url_for())
