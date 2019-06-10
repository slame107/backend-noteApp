from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('.cors')
        config.add_cors_preflight_handler()
        config.include('.models')
        config.include('pyramid_chameleon')
        config.add_static_view('static', 'static', cache_max_age=3600)
        config.add_route('add_note', '/')
        config.add_route('view_notes', '/view-notes/{pagename}')
        config.add_route('get_note', '/get-note')
        config.add_route('update_note', '/update-note/{pagename}')
        config.add_route('delete_note', '/delete-note/{pagename}')
        config.add_route('get_notelib', '/get-notelib/{pagename}')
        config.scan()
    return config.make_wsgi_app()
