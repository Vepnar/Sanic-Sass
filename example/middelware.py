"""Basic middelware example for the sanic_sass module

go to: http://0.0.0.0:8000/static/css/test.css
Here you will see:
body {
    font: 100% Helvetica, sans-serif;
    color: #333; }
"""


from sanic import Sanic
from sanic_sass import SassManifest

webserver = Sanic(name='middelware')

manifest = SassManifest('/static/css', './css', './hidden', css_type='scss')
manifest.middelware(webserver)

webserver.run(host='0.0.0.0', port=8000, debug=True)
