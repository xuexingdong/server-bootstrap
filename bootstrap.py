import os
import subprocess
import tarfile
from os import path

import sys

DEFAULT_CONFIG = {
    'root_path': '/usr/local'
}


class Software:
    wget_shell = ''

    def __init__(self):
        self.install_path = DEFAULT_CONFIG.get('root_path') + '/' + self.__class__.__name__.lower()
        self.download_file_name = self.wget_shell[self.wget_shell.rindex('/') + 1:]

    def install(self):
        self.__download()
        self.__extract()
        self.configure()
        subprocess.call('. /etc/profile', shell=True)
        os.remove(self.download_file_name)

    def __download(self):
        subprocess.call(self.wget_shell, shell=True)

    def __extract(self):
        with tarfile.open(self.download_file_name, 'r:gz') as tar:
            file_names = tar.getnames()
            target_path = self.install_path
            if not path.exists(target_path):
                os.mkdir(target_path)
            for file_name in file_names:
                tar.extract(file_name, target_path)

    def configure(self):
        pass


class Java(Software):
    wget_shell = """wget --no-cookies --no-check-certificate 
        --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" 
        http://download.oracle.com/otn-pub/java/jdk/8u152-b16/aa0333dd3019491ca4f6ddbe78cdb6d0/jdk-8u152-linux-x64.tar.gz
        """

    def __init__(self):
        super().__init__()

    def configure(self):
        if not os.environ.get('JAVA_HOME'):
            with open('/etc/profile', 'a+', encoding='utf-8') as f:
                f.writelines(
                    ['\n',
                     'export JAVA_HOME=' + self.install_path + '/jdk1.8.0_152\n',
                     'export PATH=$JAVA_HOME/bin:$PATH\n',
                     'export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar'
                     ]
                )


class Maven(Software):
    wget_shell = 'wget https://mirrors.tuna.tsinghua.edu.cn/apache/maven/maven-3/3.5.2/binaries/apache-maven-3.5.2-bin.tar.gz'

    def configure(self):
        if not os.getenv('JAVA_HOME'):
            sys.stderr.write('No JAVA_HOME found in environment variables\n')
            return
        if not os.getenv('MAVEN_HOME'):
            with open('/etc/profile', 'a+', encoding='utf-8') as f:
                f.writelines(
                    ['\n',
                     'export MAVEN_HOME=' + self.install_path + '/apache-maven-3.5.2\n',
                     'export PATH=$MAVEN_HOME/bin:$PATH'
                     ]
                )


class Nexus(Software):
    wget_shell = 'wget https://sonatype-download.global.ssl.fastly.net/nexus/3/nexus-3.6.2-01-unix.tar.gz'

    def configure(self):
        if not os.getenv('JAVA_HOME'):
            sys.stderr.write('No JAVA_HOME found in environment variables\n')
            return
        with open('/etc/profile', 'a+', encoding='utf-8') as f:
            f.writelines(
                ['\n',
                 'export NEXUS_HOME=' + self.install_path + '/nexus-3.6.2-01\n',
                 'export PATH=NEXUS_HOME/bin:$PATH'
                 ]
            )


if __name__ == '__main__':
    Maven().install()
