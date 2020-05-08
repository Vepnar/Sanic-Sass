# Sanic-sass 0.1.0

###### A simple and pythonic way to implement Sass & SCSS into Sanic without using webpack!

## Features
- On the fly compiling to speed up development with our middleware.
- Compile your entire application at once for at production

# Installation

## With pip
`pip install sanic-sass`

## With setuptools & git
Clone the newest version from github.<br>
`git clone https://github.com/Vepnar/Sanic-Sass.git`<br>
Cd into the new directory.<br>
`cd Sanic-Sass`<br>
Run setuptools.<br>
`setup.py install --user`

# Examples

### Precompiled
```py
from sanic import Sanic
from sanic_sass import SassManifest

webserver = Sanic(name='precompiled')

manifest = SassManifest('/static/css', './css', './hidden', css_type='sass')
manifest.compile_webapp(webserver, register_static=True)

webserver.run(host='0.0.0.0', port=8000)
```

### As middelware
```py
from sanic import Sanic
from sanic_sass import SassManifest

webserver = Sanic(name='middelware')

manifest = SassManifest('/static/css', './css', './hidden', css_type='scss')
manifest.middelware(webserver)

webserver.run(host='0.0.0.0', port=8000, debug=True)
```