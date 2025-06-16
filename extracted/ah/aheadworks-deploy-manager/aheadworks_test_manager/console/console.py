import json
import pathlib
import os
from os.path import join as _
import re
import shutil
import subprocess
import time
from aheadworks_core.api.composer_manager import ComposerManager
from aheadworks_core.model.cd import Cd as cd

class Console:
    def __init__(self):
        os.system("mkdir -p test-results")
        self.BASIC_PATH = pathlib.Path(os.environ.get('MAGENTO_ROOT', '/var/www/html'))
        ComposerManager.init_extra_repos()

    def assert_path_exists(self, path):
        if not os.path.exists(path):
            print(f"path '{path}' should exist", path)
            exit(1)

    def di_compile(self):
        # some modules in di:compile require active mysql
        try:
            os.system("/usr/bin/mysqld --user=root --console &>/dev/null &")
        except Exception as e:
            print(e)
        time.sleep(3)
        proc = subprocess.run([_(self.BASIC_PATH, 'bin/magento'), 'module:enable', '--all'])
        ec3 = proc.returncode
        proc = subprocess.run([_(self.BASIC_PATH, 'bin/magento'), 'setup:di:compile'])
        ec4 = proc.returncode
        print(f"module:enable ended with code {ec3}")
        print(f"di:compile ended with code {ec4}")


        if ec3 or ec4:
            print("Failed to di:compile")
            exit(1)

    def install(self, path):
        """
        Install extension(s) to path from path or zip
        """
        print("Installing from %s" % path)

        with open(_(path, 'composer.json')) as f:
            composer = json.load(f)
            # repo_name too hard for simple action
            repo_name = re.sub(r'[^a-z0-9_]', '_', composer['name'])

        with cd(self.BASIC_PATH):
            # here we download our aheadworks modules, that are in require in composer.json
            subprocess.run(
                ['composer', 'config', 'repositories.aheadworks', 'composer', 'https://composer.do.staging-box.net'])

            if os.getenv("COMPOSER_AUTH") is None:
                subprocess.run(['composer', 'config', 'http-basic.repo.magento.com', 'bf08744e4b4b3aee1d54fcd7cd56194a',
                            'f5b232eab5158a4597ecb00f8cacdf4a'])
            # main module we download always from path(the fastest way to test the latest version)
            subprocess.run(['composer', 'config', 'repositories.' + repo_name, 'path', path])

            # aheadworks/module-sarp-hyva requires aheadworks/module-sarp3 which is NOT in
            # composer require section so I was made to implement this dirty hack
            # I am really sorry
            if os.getenv("BITBUCKET_REPO_SLUG") == "module-sarp-hyva":
                hacky_proc = subprocess.run(['php', '-d', 'memory_limit=4G', '/usr/local/bin/composer', 'require', '--prefer-dist',
                                    'aheadworks/module-sarp3'])

            proc = subprocess.run(['php', '-d', 'memory_limit=4G', '/usr/local/bin/composer', 'require', '--prefer-dist',
                                   '{e[name]}:{e[version]}'.format(e=composer)])

            if proc.returncode:
                raise RuntimeError("Failed to install extension")

        # we test modules that are downloaded by composer require in /var/www/html/vendor/aheadworks/module_name
        # path of module is linked by composer with path in where we started our test step in bitbucket pipeline
        result_path = self.BASIC_PATH / 'vendor' / composer['name']
        return result_path

    def codesniffer(self, path, report_file, severity=9, report="junit"):
        """Run codesniffer tests against the path"""

        if os.getenv('SEVERITY'):
            severity = os.getenv('SEVERITY')
        self.assert_path_exists(path)

        allowed_report_formats = ["full", "xml", "checkstyle", "csv",
                                   "json", "junit", "emacs", "source",
                                   "summary", "diff", "svnblame",
                                   "gitblame",
                                   "hgblame", "notifysend"]
        if report not in allowed_report_formats:
            print(f"Unknown report format {format}", report)
            exit(1)

        options = [
            _(self.BASIC_PATH, 'vendor/bin/phpcs'),
            path
        ]

        options += ['--severity=%s' % severity]
        options += ['--standard=Magento2']
        options += ['--extensions=php,phtml']

        if report_file:
            options += ['--report=' + report]
            stdout = open(report_file, 'w')

        process = subprocess.run(options, stdout=None)
        exit(process.returncode)


    def unit(self, path, report_file, report="junit"):
        """Run unit tests for extension at path"""

        self.assert_path_exists(path)
        result_path = self.install(path)
        time.sleep(3)
        self.di_compile()
        time.sleep(3)

        try:
            os.mkdir('allure')
            shutil.copyfile("/var/www/html/dev/tests/unit/allure/allure.config.php", "allure/allure.config.php")
        except:
            print('allure config not found, its unit test for 2.4.4')

        options = [
            _(self.BASIC_PATH, 'vendor/bin/phpunit'),
            '--configuration', _(self.BASIC_PATH, 'dev/tests/unit/phpunit.xml.dist')
        ]

        if report_file:
            options += ['--log-%s' % report, report_file]

        proc = subprocess.Popen(options + [_(result_path, 'Test/Unit')])
        proc.communicate()

        exit(proc.returncode)


    def phpstan(self, path, report_file, severity=0):
        """Run phpstan static analysis against the path"""

        self.assert_path_exists(path)
        result_path = self.install(path)
        self.di_compile()

        options = [
            _(self.BASIC_PATH, 'vendor/bin/phpstan'),
            'analyse',
            path
        ]
        config = _(path, 'phpstan.neon')
        if pathlib.Path(config).is_file():
            options += ['--configuration', config]

        if os.getenv('PHPSTANSEVERITY'):
            severity = os.getenv('PHPSTANSEVERITY')

        options += ['--level', str(severity)]
        options += [
            '--autoload-file',
            _(self.BASIC_PATH, 'dev/tests/integration/framework/autoload.php')
        ]

        if report_file:
            stdout = open(report_file, 'w')

        process = subprocess.run(options, stdout=None)
        print(process)
        os.system("cat test-results/*")
        exit(process.returncode)


    def mess_detector(self, path, report_file=False, report="xml"):
        """Run mess detector against the path"""

        self.assert_path_exists(path)
        result_path = self.install(path)
        self.di_compile()

        if not report_file:
            report = 'ansi'

        options = [
            _(self.BASIC_PATH, 'vendor/bin/phpmd'),
            result_path,
            report,
            _(self.BASIC_PATH, 'dev/tests/static/testsuite/Magento/Test/Php/_files/phpmd/ruleset.xml')
        ]

        if report_file:
            stdout = open(report_file, 'w')

        process = subprocess.run(options, stdout=None)
        exit(process.returncode)


    def install_magento(self, path):
        """Run install magento with extension at path"""

        self.assert_path_exists(path)

        try:
            output = subprocess.run(
                ['sh', "/tmp/install-db-and-magento.sh"],
                check=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            os.system("mkdir logs1")
            # user pass and db_name as variable in install-db-and-magento.sh
            os.system("mysqldump -umagento2 -pPasswor8 magento_db >> logs1/dump.sql")
            os.system(f"cp /var/www/html/var/log/* logs1")
            os.system("cp /var/www/html/app/etc/* logs1")
            exit(e.returncode)

        result_path = self.install(path)
        self.di_compile()

        exit(output.returncode)
