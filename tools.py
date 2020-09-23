# coding=utf-8
from __future__ import absolute_import

import os
import shutil
import subprocess
import sys

from django.core.management.base import OutputWrapper
from django.core.management.commands.compilemessages import Command as DjangoCompilemessagesCommand
from django.core.management.commands.makemessages import check_programs, Command as DjangoMakemessagesCommand
from django.core.management.utils import handle_extensions

APPS = ('privateurl',)
LANGUAGES = ('en', 'uk', 'ru')

COMMANDS_LIST = ('makemessages', 'compilemessages', 'testmanage', 'test', 'release')
COMMANDS_INFO = {
    'makemessages': 'make po-files',
    'compilemessages': 'compile po-files to mo-files',
    'testmanage': 'run manage for test project',
    'test': 'run tests (eq. "testmanage test")',
    'release': 'make distributive and upload to pypi (setup.py bdist_wheel upload)'
}

GETTEXT_EXTENSIONS = {
    'django': ['html', 'txt', 'py'],
    'djangojs': ['js'],
}


class MakemessagesCommand(DjangoMakemessagesCommand):
    stdout = OutputWrapper(sys.stdout)
    verbosity = 1
    symlinks = False
    ignore_patterns = ['CVS', '.*', '*~', '*.pyc']
    no_obsolete = False
    keep_pot = False
    invoked_for_django = False
    locale_paths = []
    default_locale_path = None

    def _update_locale_paths(self, app_name):
        self.locale_paths = [os.path.join(app_name, 'locale').replace('\\', '/')]
        self.default_locale_path = self.locale_paths[0]
        if not os.path.exists(self.default_locale_path):
            os.makedirs(self.default_locale_path)

    @classmethod
    def get_command(cls, app_name, domain):
        assert domain in ('django', 'djangojs')
        check_programs('xgettext', 'msguniq', 'msgmerge', 'msgattrib')
        co = cls()
        co.domain = domain
        co.extensions = handle_extensions(GETTEXT_EXTENSIONS[domain])
        co._update_locale_paths(app_name)
        return co


class CompilemessagesCommand(DjangoCompilemessagesCommand):
    stdout = OutputWrapper(sys.stdout)
    verbosity = 1

    @classmethod
    def compilemessages(cls):
        check_programs('msgfmt')
        basedirs = [os.path.join(app, 'locale').replace('\\', '/') for app in APPS]
        co = cls()
        for basedir in basedirs:
            dirs = [os.path.join(basedir, locale, 'LC_MESSAGES').replace('\\', '/') for locale in LANGUAGES]
            locations = []
            for ldir in dirs:
                for dirpath, dirnames, filenames in os.walk(ldir):
                    locations.extend((dirpath, f) for f in filenames if f.endswith('.po'))
            if locations:
                co.compile_messages(locations)


def makemessages(*args):  # noqa: F841
    from django.conf import settings
    settings.configure()
    settings.MEDIA_ROOT = settings.STATIC_ROOT = '/-nopath-'
    check_programs('xgettext', 'msguniq', 'msgmerge', 'msgattrib')
    for app_name in APPS:
        for domain in ('django', 'djangojs'):
            co = MakemessagesCommand.get_command(app_name, domain)
            co.stdout.write("app: %s, domain: %s\n" % (app_name, domain))
            try:
                potfiles = co.build_potfiles()
                for locale in LANGUAGES:
                    if co.verbosity > 0:
                        co.stdout.write('processing locale %s\n' % locale)
                    for potfile in potfiles:
                        co.write_po_file(potfile, locale)
            finally:
                if not co.keep_pot:
                    co.remove_potfiles()


def compilemessages(*args):  # noqa: F841
    CompilemessagesCommand.compilemessages()


def testmanage(*args):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests'))
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py'] + list(args))


def test(*args):
    testmanage('test', *args)


def release(*args):  # noqa: F841
    root_dir = os.path.dirname(os.path.abspath(__file__))
    shutil.rmtree(os.path.join(root_dir, 'build'), ignore_errors=True)
    shutil.rmtree(os.path.join(root_dir, 'dist'), ignore_errors=True)
    shutil.rmtree(os.path.join(root_dir, 'django_privateurl.egg-info'), ignore_errors=True)
    subprocess.call(['python', 'setup.py', 'sdist', 'bdist_wheel'])
    subprocess.call(['twine', 'upload', 'dist/*'])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in COMMANDS_LIST:
        locals()[sys.argv[1]](*sys.argv[2:])
    else:
        print('Available commands:')
        for c in COMMANDS_LIST:
            print(c + ' - ' + COMMANDS_INFO[c])
