import base64
import gzip
import json
import warnings
from functools import partial
from urllib.parse import quote_plus, urlencode

from markdown import Markdown

base_url = "https://py.cafe"
default_link_text = """<img src="https://py.cafe/logos/pycafe_logo.png" style="height: 24px"> **Run and edit this code in Py.Cafe**"""


def validator(language, inputs, options, attrs, md):
    valid_flags = {"pycafe-link", "pycafe-embed"}
    valid_inputs = {
        "pycafe-embed-height",
        "pycafe-embed-width",
        "pycafe-embed-style",
        "pycafe-embed-theme",
        "pycafe-link-text",
        "pycafe-embed-scale",
        "pycafe-type",
        "requirements",
        "extra-requirements",
    }

    for k, v in inputs.items():
        if k in valid_inputs:
            options[k] = v
            continue
        elif k in valid_flags:
            options[k] = True
            continue
        attrs[k] = v
    md.preprocessors["fenced_code_block"].extension.superfences[0]["validator"](language, inputs, options, attrs, md)
    return True


def _formatter(src="", language="", class_name=None, options=None, md="", requirements="", link_text="", pycafe_type="solara", **kwargs):
    from pymdownx.superfences import SuperFencesException

    options = options or {}
    pycafe_link = options.get("pycafe-link", False)
    pycafe_embed = options.get("pycafe-embed", False)
    pycafe_embed_height = options.get("pycafe-embed-height", "400px")
    pycafe_embed_width = options.get("pycafe-embed-width", "100%")
    pycafe_embed_style = options.get("pycafe-embed-style", "border: 1px solid #e6e6e6; border-radius: 8px;")
    pycafe_embed_theme = options.get("pycafe-embed-theme", "light")
    pycafe_link_text = options.get("pycafe-link-text", link_text)
    pycafe_embed_scale = float(options.get("pycafe-embed-scale", 1.0))
    pycafe_type = options.get("pycafe-type", pycafe_type)
    requirements = "\n".join(options.get("requirements", "").split(",")) or requirements
    extra_requirements = "\n".join(options.get("extra-requirements", "").split(","))
    requirements = requirements.rstrip() + "\n" + extra_requirements

    el = md.preprocessors["fenced_code_block"].extension.superfences[0]["formatter"](
        src=src, class_name=class_name, language=language, md=md, options=options, **kwargs
    )
    try:
        if pycafe_link:
            url = pycafe_edit_url(code=src, requirements=requirements, app_type=pycafe_type)
            # Ideally, we use Markdown(extensions=md.registeredExtensions)
            # but that seems to break hl_lines in code blocks
            md_renderer = Markdown()
            pycafe_link_text_html = md_renderer.convert(pycafe_link_text)
            target = "_blank"
            link = f"""<a href="{url}" class="PyCafe-button PyCafe-launch-button" target={target}>{pycafe_link_text_html}</a>"""
            el = el.rstrip()
            if el.endswith("</div>"):
                el = el[: -len("</div>")] + link + "</div>"
            else:
                warnings.warn(
                    f"pycafe-link cannot be inserted in the code block div: {el}\nThis might break annotations, please open an issue.",
                    UserWarning,
                    stacklevel=1,
                )
                el = el + link
        if pycafe_embed:
            url = pycafe_embed_url(code=src, requirements=requirements, app_type=pycafe_type, theme=pycafe_embed_theme)
            # e.g. <iframe src="https://py.cafe/embed?apptype=streamlit&theme=light&linkToApp=false#c=..."
            #           width="100%" height="400px" style="border: 1px solid #e6e6e6; border-radius: 8px;"></iframe>
            style = (
                f"max-width: unset;"
                f"width: calc({pycafe_embed_width}/{pycafe_embed_scale}); "
                f"height: calc({pycafe_embed_height}/{pycafe_embed_scale}); "
                f"transform-origin: top left; "
                f"transform: scale({pycafe_embed_scale}); "
                f"{pycafe_embed_style}"
            )
            el = (
                el
                + f"""
            <div style="width: {pycafe_embed_width}; height: {pycafe_embed_height};">
                <iframe src="{url}" style="{style}">
                </iframe>
            </div>"""
            )
    except Exception as e:
        raise SuperFencesException from e

    return el


def pycafe_query(code: str, requirements: str):
    json_object = {"code": code}
    if requirements:
        json_object["requirements"] = requirements
    json_text = json.dumps(json_object)
    # gzip -> base64
    compressed_json_text = gzip.compress(json_text.encode("utf8"))
    base64_text = base64.b64encode(compressed_json_text).decode("utf8")
    query = urlencode({"c": base64_text}, quote_via=quote_plus)
    return query


def pycafe_edit_url(*, code: str, requirements, app_type):
    query = pycafe_query(code, requirements)
    return f"{base_url}/snippet/{app_type}/v1#{query}"


def pycafe_embed_url(*, code: str, requirements, app_type, theme="light"):
    query = pycafe_query(code, requirements)
    return f"{base_url}/embed?apptype={app_type}&theme={theme}&linkToApp=false#{query}"


def formatter(requirements="", type="solara", link_text=default_link_text):  # noqa: A002
    """Create a formatter with default requirements and type."""
    return partial(_formatter, pycafe_type=type, requirements=requirements, link_text=link_text)
