import os
import shutil

import pytest
from unittest import mock

from pycel.excelwrapper import ExcelOpxWrapper as ExcelWrapperImpl
from pycel.excelcompiler import ExcelCompiler


@pytest.fixture('session')
def fixture_dir():
    return os.path.join(os.path.dirname(__file__), 'fixtures')


@pytest.fixture('session')
def tmpdir(tmpdir_factory):
    return tmpdir_factory.mktemp('fixtures')


def copy_fixture_xls_path(fixture_dir, tmpdir, filename):
    src = os.path.join(fixture_dir, filename)
    dst = os.path.join(str(tmpdir), filename)
    shutil.copy(src, dst)
    return dst


@pytest.fixture('session')
def fixture_xls_path(fixture_dir, tmpdir):
    return copy_fixture_xls_path(fixture_dir, tmpdir, 'excelcompiler.xlsx')


@pytest.fixture('session')
def fixture_xls_path_basic(fixture_dir, tmpdir):
    return copy_fixture_xls_path(fixture_dir, tmpdir, 'basic.xlsx')


@pytest.fixture('session')
def unconnected_excel(fixture_xls_path):
    import openpyxl.reader.worksheet as orw
    old_warn = orw.warn

    def new_warn(msg, *args, **kwargs):
        if 'Unknown' not in msg:
            old_warn(msg, *args, **kwargs)

    with mock.patch('openpyxl.reader.worksheet.warn', new_warn):
        yield ExcelWrapperImpl(fixture_xls_path)


@pytest.fixture()
def excel(unconnected_excel):
    unconnected_excel.connect()
    return unconnected_excel


@pytest.fixture('session')
def basic_ws(fixture_xls_path_basic):
    return ExcelCompiler(fixture_xls_path_basic)
