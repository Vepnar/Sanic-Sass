"""Basic precompiled example for the sanic_sass module

go to: http://0.0.0.0:8000/static/css/test.css
There will also be a directory called 'css' with our test file inside of it.
Here you will see:
body {
    font: 100% Helvetica, sans-serif;
    color: #333; }
"""


from sanic import Sanic
from sanic_sass import SassManifest

webserver = Sanic(name='precompiled')

manifest = SassManifest('/static/css', './css', './hidden', css_type='sass')
manifest.compile_webapp(webserver, register_static=True)

webserver.run(host='0.0.0.0', port=8000)
