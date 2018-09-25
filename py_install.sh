#/bin/bash
set -e

py_version="$1"
echo "${py_version}"
if [ -z "${py_version}" ];then
    exit
fi
install_path=/usr/local/python
pkg_name="Python-${py_version}"
echo "install python${py_version}"
yum install -y wget
wget "https://www.python.org/ftp/python/$py_version/${pkg_name}.tgz"
tar zxvf ${pkg_name}.tgz
cd ${pkg_name}
if [ ! -d "${install_path}" ];then
    mkdir ${install_path}
fi
./configure --prefix=${install_path}
make
make install
cd ..
rm -rf ${pkg_name}*
ln -sf ${install_path}/bin/python3.6 /usr/bin/python3
ln -sf ${install_path}/bin/pip3 /usr/bin/pip3
pip3 install --upgrade pip