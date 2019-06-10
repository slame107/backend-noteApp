from pyramid.security import NO_PERMISSION_REQUIRED
# from wpcd.utils import get_setting

def includeme(config):
    config.add_directive(
        'add_cors_preflight_handler', add_cors_preflight_handler)
    config.add_route_predicate('cors_preflight', CorsPreflightPredicate)

    config.add_subscriber(add_cors_to_response, 'pyramid.events.NewResponse')


# this is a route predicate that determines what type of requests should be funneled
# through the cors preflight checks
# the __init__, text, and __call__ methods are required sturctures for all route predicates
# phash requried too, but only used internally to pyramid to keep thing unique
class CorsPreflightPredicate(object):
    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'cors_preflight = %s' % bool(self.val)

    phash = text

    def __call__(self, context, request):
        if not self.val:
            return False
        # return (
        #     request.method == 'OPTIONS' and
        #     'Origin' in request.headers and
        #     'Access-Control-Request-Method' in request.headers
        # )
        return (
            request.method == 'OPTIONS'
        )

# handler adds a catch all route and view used to modify request option Response
# headers
def add_cors_preflight_handler(config):
    config.add_route(
        'cors-options-preflight', '/{catch_all:.*}',
        cors_preflight=True,
    )
    config.add_view(
        cors_options_view,
        route_name='cors-options-preflight',
        permission=NO_PERMISSION_REQUIRED,
    )

# adds cors headers to normal responses, i.e. post
def add_cors_to_response(event):
    request = event.request
    response = event.response
    if 'Origin' in request.headers or 'origin' in request.headers:
        response.headers['Access-Control-Expose-Headers'] = (
            'Content-Type,Date,Content-Length,Authorization,X-Request-ID')
        response.headers['Access-Control-Allow-Origin'] = (
            '*')
        response.headers['Access-Control-Allow-Credentials'] = 'true'

# adds cors headers to option responses.  this is what is called by the view created in
# add_cors_preflight_handler
def cors_options_view(context, request):
    response = request.response
    if 'Access-Control-Request-Headers' in request.headers:
        response.headers['Access-Control-Allow-Methods'] = (
            'OPTIONS,HEAD,GET,POST,PUT,DELETE')
    response.headers['Access-Control-Allow-Headers'] = (
        'Content-Type,Accept,Accept-Language,Authorization,X-Request-ID')
    response.headers['Access-Control-Allow-Origin'] = (
                '*')
    return response