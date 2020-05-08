#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This simple extension provides a simple way of implementing Sass & SCSS into sanic.
"""

import os
from glob import glob
from sass import compile

from sanic import response, exceptions

__version__ = '0.1.0'
__author__ = 'Arjan de Haan'
__maintainer__ = 'Arjan de Haan'
__email__ = 'vepnardev@gmail.com'
__license__ = 'MIT'
__credits__ = ['Arjan de Haan']


def _to_realpath_list(items, create_dirs=False):

    # Convert string to list
    if isinstance(items, str):
        items = [items]

    # Normalize paths
    for index, item in enumerate(items):
        items[index] = os.path.normpath(item)

        # Make new dirs when not exist
        if not os.path.exists(item) and create_dirs:
            os.makedirs(item)
    return items


class SassManifest():
    """Compile all Sass/SCSS files to CSS.

    Args:
        web_css:
            the path of the css that will be visible on the webserver.
            type: str, list
        server_css:
            the path where the compiled css will go.
            type: str, list
        server_sass:
            path where Sass/SCSS files are on the server.
            type: str, list
        style:
            Optional setting to set the coding style of the compiler.
            choose on of: 'nested' (default), 'expanded', 'compact' or 'compresssed'.
            type: str
        css_type: Whether the compiler compiles Sass or SCSS files.
            choose on of: 'sass' or 'scss'
            type: str
    Raises:
        TypeError: web_css, server_css & server_sass are not equal length.
    """

    def __init__(self, web_css, server_css, server_sass, style='nested', css_type='sass'):
        self.web_css = _to_realpath_list(web_css)
        self.server_css = _to_realpath_list(server_css)
        self.server_sass = _to_realpath_list(server_sass, create_dirs=True)
        self.style = style
        self.css_type = css_type

        if not len(self.web_css) == len(self.server_css) == len(self.server_sass):
            raise TypeError('All lists should be equal length.')

    def _get_sass(self, web_path):
        # Only allow .css files
        prefix, suffix = os.path.splitext(web_path)
        prefix = os.path.basename(prefix)
        if suffix != '.css':
            return None

        # Remove prefix and suffix
        web_dir = os.path.dirname(web_path)

        # Loop though added paths
        for index, web_css_path in enumerate(self.web_css):
            if web_css_path in web_dir:
                new_path = web_dir[len(web_css_path):]
                return f'{self.server_sass[index]}{new_path}{os.path.sep}{prefix}.{self.css_type}'
        return None

    def _web_compile(self, web_path):
        """Turn web urls into server urls"""
        sass_path = self._get_sass(web_path)
        if sass_path is None:
            return None
        if not os.path.isfile(sass_path):
            return None

        return compile(
            filename=sass_path,
            output_style=self.style,
            include_paths=self.server_sass
        )

    def _handle_request(self, request, req_path):
        """Listen to get requests"""
        css = self._web_compile(request.path)
        if css is None:
            raise exceptions.NotFound(f'{req_path} not found.', False)

        return response.text(css, content_type='text/css ')

    def _compile_dirs(self):
        """Compile all found Sass/SCSS files to CSS files"""
        for index, server_sass_dir in enumerate(self.server_sass):
            sass_files = [y for x in os.walk(server_sass_dir) for y in glob(
                os.path.join(x[0], f'*.{self.css_type}'))]
            for sass_file in sass_files:
                filename = os.path.splitext(os.path.basename(sass_file))[0]
                new_path = os.path.dirname(sass_file)[len(server_sass_dir):]
                new_path = f'{self.server_css[index]}{new_path}'
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                with open(f'{new_path}{os.path.sep}{filename}.css', 'w+') as file:
                    css = compile(
                        filename=sass_file,
                        output_style=self.style,
                        include_paths=self.server_sass
                    )
                    file.write(css)

    def compile_webapp(self, app, register_static=False):
        """Compile all found Sass/SCSS files to CSS files the webserver starts

        Args:
            app:
                The Sanic webserver object. could be none if register_static is false.
                type: Sanic
            register_static
                optional option to register all web_css paths as
                static path on the sanic web server.
                type: bool
        """
        self._compile_dirs()
        if register_static:
            for index, path in enumerate(self.server_css):
                app.static(self.web_css[index], path)

    def middelware(self, app):
        """Developer option to compile Sass/SCSS files on the fly
        so you don't need to restart everytime.

        DON'T USE THIS IN PRODUCTION

        Args:
            app:
                The Sanic webserver object.
                type: Sanic
        """
        for web_path in self.web_css:
            app.add_route(self._handle_request,
                          f'{web_path}/<req_path:path>', methods=['GET'])
