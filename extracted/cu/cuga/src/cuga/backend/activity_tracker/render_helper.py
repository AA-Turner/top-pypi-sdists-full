import argparse
import json
import os
import re
from json import JSONDecodeError
from pathlib import Path

from cuga.backend.cuga_graph.nodes.browser.browser_planner_agent.browser_planner_agent import (
    BrowserPlannerAgent,
)


HTML_TEMPLATE = """
<!DOCTYPE html>
<head>
    <style>
        pre {{
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
    </style>
</head>
<html>
    <body>
     {body}
    </body>
</html>
"""


def get_render_action(
    action: str,
    action_set_tag: str,
) -> str:
    """Parse the predicted actions for rendering purpose. More comprehensive information"""
    action_str = ""
    action_str += f"<div class='action_object' style='background-color:grey'><pre>{action}</pre></div>"
    return action_str


def print_keys(obj):
    data = ""
    for key, value in obj.items():
        if isinstance(value, list):
            data += f"<div><b> {key}: </b> </div>"
            out = [f"<div>{i + 1}. {v}</div>" for i, v in enumerate(value) if v]
            data += "\n".join(out)
        else:
            td_str = f"<div><b> {key}</b> : {value}</div>"
            data += td_str
    return data


class RenderHelper(object):
    """Helper class to render text and image observations and meta data in the trajectory"""

    def __init__(self, config_file: str, result_dir: str, light_version: bool = False) -> None:
        with open(config_file, "r") as f:
            self._config = json.load(f)
            task_id = self._config["task_id"]
        os.makedirs(result_dir, exist_ok=True)
        self.render_file = open(Path(result_dir) / f"render_{task_id}.html", "a+")
        self.render_file.truncate(0)
        self.light_version = light_version
        # write init template
        self.render_file.write(HTML_TEMPLATE.format(body=""))
        self.render_file.read()
        self.render_file.flush()

    def render(
        self,
        render_screenshot: bool = True,
    ) -> None:
        """Render the trajectory"""
        # text observation
        new_content = "<h2>" + self._config['intent'] + "</h2>\n"

        for (
            index,
            step,
        ) in enumerate(self._config['steps']):
            new_content += f"<h3 class='step_name' style='background-color:lightblue'>Step {index + 1} : {step['name']}</h3>"
            if step['name'] == BrowserPlannerAgent:
                new_content += (
                    f"<div class='current_url'><pre>Current URL: {step['current_url']}</pre><div>\n"
                )

                if render_screenshot:
                    # image observation
                    img = step["image_before"]
                    new_content += f"<img src='{img}' style='width:50vw; height:auto;'/>\n"

                text_obs = step["observation_before"]
                new_content += (
                    f"<div class='code-viewer' style='background-color: #f4f4f4; border: 1px solid #ddd; padding: 10px; border-radius: 5px;margin: 10px;position: relative;'>"
                    f"<div class='state_obv'>"
                    f"<pre>{text_obs[:300]}"  # Limit text to 300 characters
                    f"<span class='collapse' style='display:none;'>{text_obs[300:]}</span>"  # Hidden part
                    f"</pre>"
                    f"<a href='#' class='expand-link' style='position: absolute; top: 0; bottom: 0; left: 0; width: 25px; background-color: #ddd; text-align: center; display: flex; justify-content: center; align-items: center; text-decoration: none; font-size: 15px;' onclick=\"toggleCollapse(this); return false;\"> ></a>"
                    f"</div>\n"
                    f"</div>\n"
                )

                new_content += f"<div class='prev_action' style='background-color:pink'>{print_keys(json.loads(step['plan']))}</div>\n"

            if step['name'] == "ActionAgent":
                action_str = f"<div class='parsed_action' style='background-color:yellow'><pre>{step['action_formatted']}</pre></div>"
                new_content += f"{action_str}\n"

            if step['name'] == "TaskDecompositionAgent":
                td = json.loads(step['task_decomposition'])
                new_content += print_keys(td)

            elif 'data' in step and step['data']:
                try:
                    td = json.loads(step['data'])
                except JSONDecodeError:
                    td = step['data']
                new_content += print_keys(td) if not isinstance(td, str) else td
        if not self.light_version:
            kk = f"<div class='parsed_action' style='background-color:grey'><pre>Score: {self._config['score']}</pre></div>"
            new_content += f"{kk}\n"
            kk = f"<div class='parsed_action' style='background-color:grey'><pre>{self._config.get('eval', '')}</pre></div>"
            new_content += f"{kk}\n"
            new_content += (
                "<script>\n"
                "function toggleCollapse(link) {\n"
                "  const preElement = link.previousElementSibling;\n"
                "  const collapseSpan = preElement.querySelector('.collapse');\n"
                "  if (collapseSpan.style.display === 'none') {\n"
                "    collapseSpan.style.display = 'inline';\n"
                "    link.textContent = '<';\n"
                "  } else {\n"
                "    collapseSpan.style.display = 'none';\n"
                "    link.textContent = '>';\n"
                "  }\n"
                "}\n"
                "</script>"
            )
        # add new content
        self.render_file.seek(0)
        html = self.render_file.read()
        html_body = re.findall(r"<body>(.*?)</body>", html, re.DOTALL)[0]
        html_body += new_content
        html = HTML_TEMPLATE.format(body=html_body)
        self.render_file.seek(0)
        self.render_file.truncate()
        self.render_file.write(html)
        self.render_file.flush()

    def close(self) -> None:
        self.render_file.close()


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Render JSON files to HTML.")
    parser.add_argument("--config_file", required=True, help="Path to the config file.")
    parser.add_argument("--result_dir", required=True, help="Directory to save rendered HTML files.")
    parser.add_argument(
        "--light_version",
        required=False,
        type=bool,
        default=False,
        help="Directory to save rendered HTML files.",
    )

    args = parser.parse_args()
    # Call the render function
    renderer = RenderHelper(
        config_file=args.config_file, result_dir=args.result_dir, light_version=args.light_version
    )
    renderer.render()
