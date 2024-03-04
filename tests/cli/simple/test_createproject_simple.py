import os
import shutil

import pytest

from lilya.apps import Lilya
from tests.cli.utils import run_cmd

app = Lilya(routes=[])


@pytest.fixture(scope="module")
def create_folders():
    os.chdir(os.path.split(os.path.abspath(__file__))[0])
    try:
        os.remove("app.db")
    except OSError:
        pass
    try:
        shutil.rmtree("myproject")
        shutil.rmtree("simple/myproject")
    except OSError:
        pass
    try:
        shutil.rmtree("temp_folder")
    except OSError:
        pass

    yield

    try:
        os.remove("app.db")
    except OSError:
        pass
    try:
        shutil.rmtree("myproject")
        shutil.rmtree("simple/myproject")
    except OSError:
        pass
    try:
        shutil.rmtree("temp_folder")
    except OSError:
        pass


def test_create_project_simple(create_folders):
    (o, e, ss) = run_cmd("tests.cli.main:app", "lilya createproject myproject")
    assert ss == 0

    with open("myproject/Makefile") as f:
        assert f.readline().strip() == ".DEFAULT_GOAL := help"
    with open("myproject/.gitignore") as f:
        assert f.readline().strip() == "# Byte-compiled / optimized / DLL files"
    with open("myproject/myproject/app.py") as f:
        assert """__name__""" in f.read()


def _run_simple_asserts():
    assert os.path.isfile("myproject/Makefile") is True
    assert os.path.isfile("myproject/.gitignore") is True
    assert os.path.isfile("myproject/myproject/__init__.py") is True
    assert os.path.isfile("myproject/myproject/app.py") is True
    assert os.path.isfile("myproject/myproject/tests/__init__.py") is True
    assert os.path.isfile("myproject/myproject/tests/test_app.py") is True
    assert os.path.isfile("myproject/requirements/base.txt") is True
    assert os.path.isfile("myproject/requirements/testing.txt") is True
    assert os.path.isfile("myproject/requirements/development.txt") is True


def test_create_project_files_with_env_var_simple(create_folders):
    (o, e, ss) = run_cmd("tests.cli.main:app", "lilya createproject myproject")
    assert ss == 0

    _run_simple_asserts()


def test_create_project_files_without_env_var_simple(create_folders):
    (o, e, ss) = run_cmd("tests.cli.main:app", "lilya createproject myproject", is_app=False)
    assert ss == 0

    _run_simple_asserts()


def test_create_project_files_without_env_var_and_with_app_flag_simple(create_folders):
    (o, e, ss) = run_cmd(
        "tests.cli.main:app",
        "lilya --app tests.cli.main:app createproject myproject",
        is_app=False,
    )
    assert ss == 0

    _run_simple_asserts()
