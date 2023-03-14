import pytest
from playwright.sync_api import Page, expect, BrowserType
import re
from src.common import config, utils
import time

default_timeout = 90000
image_for_upload = '../assets/ocean-quotes-index-1624414741.jpg'

@pytest.fixture(scope="session")
def setup(create_page_context):
    return dict(
        page=create_page_context
    )


@pytest.fixture(scope='session', autouse=True)
def teardown(setup):
    yield
    page = setup.get('page')
    page.click("header .q-avatar__content")
    logout = page.get_by_text(' Log Out ')
    logout.click()
    time.sleep(2)


def test_login(setup):
    page = setup.get('page')
    page.goto(config.dl_platform_url)
    expect(page).to_have_title(re.compile("Dataloop Platform"))
    login_button = page.get_by_role("button", name='Sign Up / Login')
    login_button.click()
    expect(page.get_by_placeholder('yours@example.com')).to_be_visible(timeout=default_timeout)
    page.get_by_label('email').fill(config.test_email)
    page.get_by_label('password').fill(config.test_password)
    locator = page.locator('//*[@id="auth0-lock-container-1"]/div/div[2]/form/div/div/button')
    expect(locator).to_be_visible(timeout=default_timeout)
    locator.click()
    expect(page.get_by_text(' bzoref.adv@gmail.com ')).to_be_visible(timeout=default_timeout)


def test_enter_the_dataset(setup):
    page = setup.get('page')
    dataset_locator = page.get_by_text(config.test_dataset)
    expect(dataset_locator).to_be_visible(timeout=default_timeout)
    dataset_locator.dblclick()


def test_goto_studio(setup):
    page = setup.get('page')
    image = page.locator('[id=item_open_button_640f53514e6b73338efe06cf]')
    expect(image).to_be_visible(timeout=default_timeout)
    image.dblclick()


def test_delete_all_anotations(setup):
    page = setup.get('page')
    time.sleep(3)
    delete_annotations_btn = page.get_by_role('button').all()[36]
    all_annotations_button = page.get_by_role('checkbox').all()[0]
    try:
        assert all_annotations_button.is_checked()
    except AssertionError:
        all_annotations_button.click()
    try:
        assert delete_annotations_btn.is_disabled()
    except AssertionError:
        delete_annotations_btn.click()
        time.sleep(2)
        page.keyboard.press('Enter')


def test_create_box_annotation(setup):
    page = setup.get('page')
    page.locator('//*[@id="tabs-panel"]/div[1]/div[1]/div/div/div[2]/div[2]').click()
    time.sleep(2)
    image_id = page.locator('//*[@id="tabs-panel"]/div[2]/div/div/div/div/div[3]/div/div/div[2]/div/div[3]/div[1]/div[2]/div').text_content().lstrip().rstrip()
    my_token = utils.get_authentication_token()
    get_image_info = utils.get_item_info(item_id=image_id, token=my_token)
    image_height = get_image_info['metadata']['system']['height']
    image_width = get_image_info['metadata']['system']['width']
    page.locator('//*[@id="toolsMenu"]/div[4]/div/button/span[2]/span').click()
    page.mouse.click(x=round(image_width/4), y=round(image_height/4), button="left")
    page.mouse.click(x=round(3*(image_width/4)), y=round(3*(image_height/4)), button="left")


