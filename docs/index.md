# PyCafe plugin for MkDocs

## Introduction

Did you ever want your code snippets in your documentation to be interactive? Let you users edit them and see what the result is?

This plugin allow you to create links to, or embed PyCafe projects in your MkDocs documentation from code blocks.

## Installation

```bash
pip install mkdocs mkdocs-material mkdocs-pycafe
```

*(Assuming you use mkdocs-material.)*

For documentation on mkdocs, visit [mkdocs.org](https://www.mkdocs.org), for documentation of MkDocs Material, visit [squidfunk.github.io/mkdocs-material](https://squidfunk.github.io/mkdocs-material).

## Configuration

Make sure you configure mkdocs to use PyCafe's formatter for Python codeblocks, and enable the snippets plugin if you want to use the scissor syntax (`--8<--`).

```yaml
site_name: PyCafe plugin for MkDocs
site_url: https://mkdocs.py.cafe
theme:
  name: material
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: python
          class: 'highlight'
          validator: !!python/name:mkdocs_pycafe.validator
          format: !!python/object/apply:mkdocs_pycafe.formatter
            kwds:
              type: solara
              requirements: |
                altair
                anywidget
  - pymdownx.snippets:
      url_download: true
```

In this case, we added default requirements, and a default PyCafe type of `solara`. You can also specify the type in the code block itself by providing `pycafe-type` and `requirements` attributes.

In the examples below, we mostly use the `extra-requirements` attribute to specify additional requirements, instead of overwriting the default requirements.


## Usage

### Code block with a link to PyCafe

To insert a link to PyCafe below you code blocks, add the `pycafe-link` option, and specify the `extra-requirements`if needed.

````
```{.python pycafe-link extra-requirements="vega_datasets"}
from vega_datasets import data
import altair as alt

cars = data.cars()

chart = alt.Chart(cars).mark_circle().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
)

# assign a widget to page so solara knows what to render
page = alt.JupyterChart(chart)
```
````

Which will render as:

```{.python pycafe-link extra-requirements="vega_datasets"}
from vega_datasets import data
import altair as alt

cars = data.cars()

chart = alt.Chart(cars).mark_circle().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',

# assign a widget to page so solara knows what to render
page = alt.JupyterChart(chart)
```

The default link text (in markdown format) can be changed in `mkdocs.yml` by changing the `link_text` option in the `format` object, or by adding the `pycafe-link-text` attribute to the code block.

````
```{.python pycafe-link pycafe-link-text="My custom link text"}
...
```
````

### Existing code block features

Existing features such as [annotations](https://squidfunk.github.io/mkdocs-material/reference/annotations/) and [line highlighting](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#highlighting-specific-lines) should still work.

````
```{.python pycafe-link extra-requirements="vega_datasets" hl_lines="7-9"}
from vega_datasets import data
import altair as alt

cars = data.cars()  # (1)

chart = alt.Chart(cars).mark_circle().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
)

# assign a widget to page so solara knows what to render
page = alt.JupyterChart(chart)
```

1.  Code annotations should still work.

````

Should render as:

```{.python pycafe-link  hl_lines="7-9" extra-requirements="vega_datasets"}
from vega_datasets import data
import altair as alt

cars = data.cars()  # (1)

chart = alt.Chart(cars).mark_circle().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
)

# assign a widget to page so solara knows what to render
page = alt.JupyterChart(chart)
```

1.  Code annotations should still work.


### Code block with an embedded app

If want the app to be embedded, instead of providing a link, you can use the pycafe-embed flag.

````

```{.python pycafe-embed extra-requirements="vega_datasets" pycafe-embed-style="border: 1px solid #e6e6e6; border-radius: 8px;" pycafe-embed-width="100%" pycafe-embed-height="400px" pycafe-embed-scale="1.0"}
from vega_datasets import data
import altair as alt

cars = data.cars()

chart = alt.Chart(cars).mark_circle().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
)

# assign a widget to page so solara knows what to render
page = alt.JupyterChart(chart)
```
````

Which will render as:

```{.python pycafe-embed extra-requirements="vega_datasets" pycafe-embed-style="border: 1px solid #e6e6e6; border-radius: 8px;" pycafe-embed-width="100%" pycafe-embed-height="400px" pycafe-embed-scale="1.0"}
from vega_datasets import data
import altair as alt

cars = data.cars()

chart = alt.Chart(cars).mark_circle().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
)

# assign a widget to page so solara knows what to render
page = alt.JupyterChart(chart)
```


### Code block with code from PyCafe

If you enabled the snippets plugin, you can include code from PyCafe directly using the `--8<--` syntax.

````
```python
;--8<-- "https://py.cafe/files/maartenbreddels/altair-car-performance-comparison/app.py"
```
````

Which will render as:

```python
--8<-- "https://py.cafe/files/maartenbreddels/altair-car-performance-comparison/app.py"
```

Although this can be combined with the above PyCafe link and embed options, it is more flexible to directly use
html to include a link to, or embed a PyCafe project.

A link can be made using Markdown or HTML
```
[Custom link to PyCafe project](https://py.cafe/maartenbreddels/altair-car-performance-comparison)
<a href="https://py.cafe/maartenbreddels/altair-car-performance-comparison" target="_blank">Custom link to PyCafe project</a>
```

Which will render as: <a href="https://py.cafe/maartenbreddels/altair-car-performance-comparison" target="_blank">Custom link to PyCafe project</a>

To embed a PyCafe project, use the following HTML code (also available via the Share dialog on the PyCafe website):
```html
<iframe src="https://py.cafe/embed/maartenbreddels/altair-car-performance-comparison?theme=light&linkToApp=false" width="100%" height="400px" style="border: 1px solid #e6e6e6; border-radius: 8px;"></iframe>
```
Which will render as:


<iframe src="https://py.cafe/embed/maartenbreddels/altair-car-performance-comparison?theme=light&linkToApp=false" width="100%" height="400px" style="border: 1px solid #e6e6e6; border-radius: 8px;"></iframe>
