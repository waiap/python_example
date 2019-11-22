from . import handlers


def setup_routes(app):
    """Setup app handlers."""
    # Render checkout page with the payment wall
    app.router.add_get('/', handlers.checkout, name="checkout")
    app.router.add_get('/backoffice/', handlers.backoffice, name="backoffice")
    app.router.add_get('/redirect/', handlers.redirect, name="redirect")
    app.router.add_get('/results/', handlers.results, name="results")
    app.router.add_post('/actions/', handlers.actions, name="actions")
