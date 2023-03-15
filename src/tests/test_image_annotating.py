import pytest
from playwright.sync_api import Page, expect, BrowserType
import re
from src.common import config, utils
import time

default_timeout = 90000
image_for_upload = '../assets/ocean-quotes-index-1624414741.jpg'
expected_annotation_width = 601
expected_annotation_height = 301


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


def test_delete_all_annotations(setup):
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
    page.locator('//*[@id="toolsMenu"]/div[4]/div/button/span[2]/span').click()
    image_id = page.locator(
        '//*[@id="tabs-panel"]/div[2]/div/div/div/div/div[3]/div/div/div[2]/div/div[3]/div[1]/div[2]/div').text_content().lstrip().rstrip()
    image_container = page.locator('//*[@id="imageDisplayContainer"]/div/div/canvas[2]')
    box = image_container.bounding_box()
    annotation_coord = utils.calculate_annotation_starting_and_ending_point(box)
    page.mouse.click(x=annotation_coord['annotation_x_start_point'], y=annotation_coord['annotation_y_start_point'])
    time.sleep(1)
    page.mouse.click(x=annotation_coord['annotation_x_end_point'], y=annotation_coord['annotation_y_end_point'])
    page.locator('//*[@id="app"]/div/div[4]/div/div/div[1]/div/div/div[2]/div[3]/div[3]/div/div/div/div/button/span[2]/span/i').click()
    my_token = utils.get_authentication_token()
    annotation_details = utils.get_annotation_info(image_id, my_token)
    anottation_width = round(annotation_details[0]['coordinates'][1]['x'] - annotation_details[0]['coordinates'][0]['x'])
    anottation_height = round(annotation_details[0]['coordinates'][1]['y'] - annotation_details[0]['coordinates'][0]['y'])
    try:
        assert anottation_width == expected_annotation_width
        assert anottation_height == expected_annotation_height
    except AssertionError as e:
        pytest.fail(f"Expected annotation coordinates are not as expected. Got {e} ")
