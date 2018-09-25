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
yum -y install gcc gcc-c++ zlib zlib-devel libffi-devel deltarpm kernel-devel kernel-headers make
yum -y install bzip2 bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel
yum -y install xz-devel
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
ln -sf ${install_path}/bin/python${py_version:0:2} /usr/bin/python${py_version:0}
ln -sf ${install_path}/bin/pip${py_version:0} /usr/bin/pip${py_version:0}
pip${py_version:0} install --upgrade pip