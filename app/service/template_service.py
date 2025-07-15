import os
from datetime import date

from jinja2 import Environment, FileSystemLoader

from app.config.variable import COPYRIGHT_NOTICE, LOGO_URL


class TemplateService:
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'template')
    jinja_env = Environment(loader=FileSystemLoader(template_dir))

    def render_template(self, template: str, **kwargs) -> str:
        template = self.jinja_env.get_template(f'{template}.jinja2')
        template_copyright = self.jinja_env.from_string(COPYRIGHT_NOTICE)
        today_date = date.today()

        rendered_content = template.render(copyrightNotice=template_copyright.render(year=today_date.year, platformName='KAYA'),
                                           platformName='KAYA',
                                           imgLink=LOGO_URL,
                                           **kwargs)

        return rendered_content
