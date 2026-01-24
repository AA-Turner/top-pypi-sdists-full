from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.backends.django import DjangoTemplates as BaseDjangoTemplates
from django.template.backends.django import Template as BaseTemplate
from django.template.backends.django import reraise
from django.template.context import make_context


class Template(BaseTemplate):
    def render(self, context=None, request=None):
        context = make_context(context, request, autoescape=self.backend.engine.autoescape)
        context.update(
            {
                "PLOTLY_CDN": settings.WBCORE_PLOTLY_CDN_URL,
                "FRONTEND_VERSION": settings.FRONTEND_VERSION,
            }
        )
        try:
            return self.template.render(context)
        except TemplateDoesNotExist as exc:
            reraise(exc, self.backend)


class DjangoTemplates(BaseDjangoTemplates):
    def get_template(self, template_name):
        try:
            return Template(self.engine.get_template(template_name), self)
        except TemplateDoesNotExist as exc:
            reraise(exc, self)
