import aiohttp_jinja2
from aiohttp_session import get_session


@aiohttp_jinja2.template('results.jinja2')
async def results(request):
    """Show payment results."""
    session = await get_session(request)
    return {'result': session.get('last_response', {})}
