# -*- coding: utf-8 -*-

from shopping_cart import create_app

application = create_app()

if __name__ == '__main__':
    ip = '0.0.0.0'
    port = application.config['APP_PORT']
    debug = application.config['DEBUG']

    application.run(
        host=ip,
        debug=debug,
        port=port,
        threaded=True,
        use_reloader=debug
    )
