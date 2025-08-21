import asyncio

from project.core.jinja2_templates import get_cached_jinja2_templates
from project.core.setup_logging import setup_logging
from project.emailer.send_email import async_send_email


async def async_send_simple_email(
        *,
        to_email: str,
        project_name: str,
        title: str,
        text: str
):
    render_data = {
        "title": title,
        "project_name": project_name,
        "text": text
    }

    html_content = get_cached_jinja2_templates().get_template("simple_email.html").render(render_data)

    await async_send_email(
        to_email=to_email,
        subject=title,
        html_content=html_content
    )


async def __async_example():
    setup_logging()
    await async_send_simple_email(
        to_email="arpakit@gmail.com",
        title="Notification",
        project_name="Test",
        text="asfasf"
    )


if __name__ == '__main__':
    asyncio.run(__async_example())
