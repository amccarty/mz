# Jupyter Proxy handling for Django projects in Anaconda Enterprise
#
# PROBLEM: When developing web applications in Anaconda Enterprise, the web app is accessed
# through a proxy managed by Jupyter. This proxy adds a prefix of /proxy/<port> to every
# URL, where <port> is the TCP port the application is serving on. Unfortunately, Django
# does not naturally support being served from a URL subdirectory such as this. To fix this,
# this middelware performs URL post-processing on all Django-generated content to insert the
# proxy prefix on all relative URLs.
#
# To use this file in your Django project:
# 1. Tip: place the root of your Django project in the root directory of your
#    Anaconda Enterprise project. For example, in Anaconda Enterprise, you can
#    use "django-admin startproject mysite ."
# 2. Add this file to your Python path. The root directory of your Django project,
#    where the manage.py script lives, is a good choice. If you have followed the
#    tip above, this is the root directory of your AE project.
# 3. Append the following two lines to your site's settings.py:
#        if os.environ.get('TOOL_PORT'):
#            MIDDLEWARE.append('aeproxy.ae_proxy_middleware')
#    The if statement ensures that this middleware is active only in development.
#    For deployments, TOOL_PORT does not exist, so this will be bypassed.

import re
import os

def ae_proxy_middleware(get_response):
    re_sub = re.compile(r'((?:href|action|src)=["\'])(/(?:.*?)["\'])')
    def process(request):
        response = get_response(request)
        
        # Retrieving the SERVER_PORT value allows us to be agnostic to the
        # port the web app is running on. But note that for AE deployments, the
        # web app is expected to run on port 8086.
        prefix = '/proxy/' + request.META['SERVER_PORT']

        # This is for redirects, which are used commonly in form submissions
        if 'Location' in response and response['Location'].startswith("/"):
            response['Location'] = prefix + response['Location']
 
        # This is for standard HTML content: scan for relative URLs and add the prefix
        if 'Content-Type' in response and response['Content-Type'].startswith("text/html;"):
            content = re_sub.sub(r'\1' + prefix + r'\2', response.content.decode('utf8'))
            response.content = content.encode('utf8')

        return response
    return process
