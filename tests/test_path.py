# coding: utf8
from __future__ import unicode_literals
import re
import sys

from six import text_type
import pytest

from clldutils.path import Path, Manifest, copytree, memorymapped


def make_file(d, name='test.txt', text='test', encoding=None):
    path = d.join(name)
    path.write_text(text, encoding=encoding)
    return Path(str(path))


def test_Manifest(tmpdir):
    d = Path(__file__).parent
    m = {k: v for k, v in Manifest.from_dir(d).items()}
    copytree(d, str(tmpdir.join('d')))
    assert m == Manifest.from_dir(Path(tmpdir.join('d')))
    copytree(d, Path(str(tmpdir.join('d', 'd'))))
    assert m != Manifest.from_dir(Path(tmpdir.join('d')))


def test_Manifest2(tmpdir):
    make_file(tmpdir, name='b.txt')
    make_file(tmpdir, name='a.txt')
    m = Manifest.from_dir(Path(tmpdir))
    assert '{0}'.format(m) == \
        '098f6bcd4621d373cade4e832627b4f6  a.txt\n098f6bcd4621d373cade4e832627b4f6  b.txt'
    m.write(Path(tmpdir))
    assert tmpdir.join('manifest-md5.txt').check()


def test_memorymapped(tmpdir):
    p = make_file(tmpdir, text='äöü', encoding='utf-8')
    with memorymapped(p) as b:
        assert b.find('ö'.encode('utf-8')) == 2


def test_read_write(tmpdir):
    from clldutils.path import read_text, write_text

    text = 'äöüß'
    p = Path(tmpdir.join('test'))
    assert write_text(p, text) == len(text)
    assert read_text(p) == text


def test_readlines(tmpdir):
    from clldutils.path import readlines

    # Test files are read using universal newline mode:
    fname = make_file(tmpdir, text='a\nb\r\nc\rd')
    assert len(readlines(fname)) == 4

    lines = ['\t#ä ']
    assert readlines(lines) == lines
    assert readlines(lines, normalize='NFD') != lines
    assert readlines(lines, strip=True)[0] == lines[0].strip()
    assert readlines(lines, comment='#') == []
    assert readlines(lines, comment='#', linenumbers=True) == [(1, None)]
    lines = ['']
    assert readlines(lines) == ['']
    assert readlines(lines, comment='#') == []
    assert readlines(lines, strip=True, normalize='NFC') == []


def test_import_module(tmpdir):
    from clldutils.path import import_module

    make_file(tmpdir, name='__init__.py', encoding='ascii', text='A = [1, 2, 3]')
    syspath = sys.path[:]
    m = import_module(Path(tmpdir))
    assert len(m.A) == 3
    assert syspath == sys.path

    make_file(tmpdir, name='abcd.py', encoding='ascii', text='A = [1, 2, 3]')
    m = import_module(Path(tmpdir.join('abcd.py')))
    assert len(m.A) == 3


def test_non_ascii():
    from clldutils.path import Path, path_component, as_unicode

    p = Path(path_component('äöü')).joinpath(path_component('äöü'))
    assert isinstance(as_unicode(p), text_type)
    assert isinstance(as_unicode(p.name), text_type)


def test_as_posix():
    from clldutils.path import as_posix, Path

    with pytest.raises(ValueError):
        as_posix(5)
    assert as_posix('.') == as_posix(Path('.'))


def test_md5():
    from clldutils.path import md5

    assert re.match('[a-f0-9]{32}$', md5(__file__))


def test_copytree(tmpdir):
    from clldutils.path import copytree

    dst = Path(tmpdir.join('a', 'b'))
    copytree(Path(tmpdir), dst)
    assert dst.exists()
    with pytest.raises(OSError):
        copytree(dst, dst)


def test_copy(tmpdir):
    from clldutils.path import copy

    src = make_file(tmpdir, name='test', text='abc')
    dst = Path(tmpdir.join('other'))
    copy(src, dst)
    assert src.stat().st_size == dst.stat().st_size


def test_move(tmpdir):
    from clldutils.path import move

    dst = Path(tmpdir.join('a'))
    dst.mkdir()
    src = make_file(tmpdir, name='test')
    move(src, dst)
    assert not src.exists()
    assert dst.joinpath(src.name).exists()


def test_remove(tmpdir):
    from clldutils.path import remove

    with pytest.raises(OSError):
        remove(Path(tmpdir.join('nonexistingpath')))
    tmp = make_file(tmpdir, name='test')
    assert tmp.exists()
    remove(tmp)
    assert not tmp.exists()


def test_rmtree(tmpdir):
    from clldutils.path import rmtree

    with pytest.raises(OSError):
        rmtree(str(tmpdir.join('nonexistingpath')))
    rmtree(str(tmpdir.join('nonexistingpath')), ignore_errors=True)
    tmp = Path(tmpdir.join('test'))
    tmp.mkdir()
    assert tmp.exists()
    rmtree(tmp)
    assert not tmp.exists()


def test_walk(tmpdir):
    from clldutils.path import walk

    d = Path(tmpdir.join('testdir'))
    d.mkdir()
    make_file(tmpdir, name='testfile')
    res = [p.name for p in walk(d.parent, mode='files')]
    assert 'testdir' not in res
    assert 'testfile' in res
    res = [p.name for p in walk(d.parent, mode='dirs')]
    assert 'testdir' in res
    assert 'testfile' not in res


def test_git_describe(tmpdir, capsys):
    from clldutils.path import git_describe

    d = Path(tmpdir.join('testdir'))
    with pytest.raises(ValueError):
        git_describe(d)
    d.mkdir()
    assert git_describe(d) == 'testdir'


def test_TemporaryDirectory():
    from clldutils.path import TemporaryDirectory

    with TemporaryDirectory() as tmp:
        assert tmp.exists()
    assert not tmp.exists()
