import pytest
from playwright.sync_api import sync_playwright, Playwright
from typing import Dict

@pytest.fixture(scope="session")
def context(
    playwright: Playwright,
    browser_name: str,
    browser_type_launch_args: Dict,
    browser_context_args: Dict
):
    context = getattr(playwright, browser_name).launch_persistent_context("./foobar", **{
        **browser_type_launch_args,
        **browser_context_args,
        "locale": "en-GB",
    })
    yield context
    context.close()


@pytest.fixture(scope='session')
def create_page_context(context):
    return context.new_page()