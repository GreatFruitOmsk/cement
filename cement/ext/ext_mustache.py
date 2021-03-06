"""Mustache Framework Extension."""

import sys
import pystache
from ..core import output, exc, handler
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class MustacheOutputHandler(output.TemplateOutputHandler):
    """
    This class implements the :ref:`IOutput <cement.core.output>`
    interface.  It provides text output from template and uses the
    `Mustache Templating Language <http://mustache.github.com>`_.

    **Note** This extension has an external dependency on `pystache`.  You
    must include `pystache` in your applications dependencies as Cement
    explicitly does *not* include external dependencies for optional
    extensions.

    Usage:

    .. code-block:: python

        from cement.core import foundation

        class MyApp(foundation.CementApp):
            class Meta:
                label = 'myapp'
                extensions = ['mustache']
                output_handler = 'mustache'
                template_module = 'myapp.templates'
                template_dir = '/usr/lib/myapp/templates'
        # ...

    From here, you would then put a Mustache template file in
    `myapp.templates.my_template.mustache` and then render a data dictionary
    with it:

    .. code-block:: python

        # via the app object
        myapp.render(some_data_dict, 'my_template.mustache')

        # or from within a controller or handler
        self.app.render(some_data_dict, 'my_template.mustache')



    Configuration:

    This extension honors the ``template_dir`` configuration option under the
    base configuration section of any application configuration file.  It
    also honors the ``template_module`` and ``template_dir`` meta options
    under the main application object.

    """

    class Meta:
        interface = output.IOutput
        label = 'mustache'

    def render(self, data_dict, template):
        """
        Take a data dictionary and render it using the given template file.

        Required Arguments:

        :param data_dict: The data dictionary to render.
        :param template: The path to the template, after the
            ``template_module`` or ``template_dir`` prefix as defined in the
            application.
        :returns: str (the rendered template text)

        """
        LOG.debug("rendering output using '%s' as a template." % template)
        content = self.load_template(template)
        return pystache.render(content, data_dict)


def load():
    handler.register(MustacheOutputHandler)
