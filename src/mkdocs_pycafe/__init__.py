import base64
import gzip
import json
from functools import partial
from urllib.parse import quote_plus, urlencode

base_url = "https://py.cafe"


def validator(language, inputs, options, attrs, md):
    valid_flags = {"pycafe-link", "pycafe-embed"}
    valid_inputs = {"requirements", "extra-requirements", "pycafe-type"}

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


def _formatter(src="", language="", class_name=None, options=None, md="", requirements="", pycafe_type="solara", **kwargs):
    from pymdownx.superfences import SuperFencesException

    options = options or {}
    pycafe_link = options.get("pycafe-link", False)
    pycafe_embed = options.get("pycafe-embed", False)
    pycafe_embed_height = options.get("pycafe-embed-height", "400px")
    pycafe_embed_width = options.get("pycafe-embed-width", "100%")
    pycafe_embed_style = options.get("pycafe-embed-style", "border: 1px solid #e6e6e6; border-radius: 8px;")
    pycafe_embed_theme = options.get("pycafe-embed-theme", "light")
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
            text = "Run and edit above code in py.cafe"
            target = "_blank"
            el = el + f"""<a href="{url}" class="PyCafe-button PyCafe-launch-button" target={target}>{text}</a>"""
        if pycafe_embed:
            url = pycafe_embed_url(code=src, requirements=requirements, app_type=pycafe_type, theme=pycafe_embed_theme)
            # e.g. <iframe src="https://py.cafe/embed?apptype=streamlit&theme=light&linkToApp=false#c=..."
            #           width="100%" height="400px" style="border: 1px solid #e6e6e6; border-radius: 8px;"></iframe>
            el = el + f"""<iframe src="{url}" width="{pycafe_embed_width}" height="{pycafe_embed_height}" style="{pycafe_embed_style}"></iframe>"""
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


def formatter(requirements="", type="solara"):  # noqa: A002
    """Create a formatter with default requirements and type."""
    return partial(_formatter, pycafe_type=type, requirements=requirements)
