from typing import List

from abstra_internals.constants import get_project_url
from abstra_internals.email_templates.html_wrapper import style_wrap
from abstra_internals.email_templates.i18n import get_translation
from abstra_internals.repositories.email import EmailParams
from abstra_internals.repositories.project.project import (
    FormStage,
    LocalProjectRepository,
)

template = """
<p style="font-style: normal; font-weight: 700; font-size: 30px; line-height: 36px; color:#181818; margin:30px 0 40px;">
    {a_form_is_waiting}
</p>
<a href="{stage_link}" style="text-decoration: none;white-space: nowrap; padding: 10px 22px; border-radius: 6px; background-color: #d14056; color: #FFF; box-shadow: 0 2px 0 rgba(255, 5, 5, 0.06); font-size: 16px; font-family: system-ui;">
    {waiting_cta}
</a>
"""


def generate_email(recipient_emails: List[str], form: FormStage) -> EmailParams:
    project = LocalProjectRepository().load()
    translations = get_translation(project.workspace.language or "en")
    stage_link = f"{get_project_url()}/{form.path}"

    content = template.format(
        a_form_is_waiting=translations.form_is_waiting(form.title),
        stage_link=stage_link,
        waiting_cta=translations.waiting_cta(),
    )

    html = style_wrap(content, project.workspace)

    return EmailParams(
        kind="task-waiting",
        to=recipient_emails,
        subject=translations.form_is_waiting(form.title),
        body=html,
        is_html=True,
        attachments=[],
    )
