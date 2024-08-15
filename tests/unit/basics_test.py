import mkdocs_pycafe


def test_embed_url():
    url = mkdocs_pycafe.pycafe_embed_url(code="print('Hello, World!')", requirements="pandas", app_type="streamlit", theme="light")
    assert url.startswith("https://py.cafe/embed?apptype=streamlit&theme=light&linkToApp=false#c=")
