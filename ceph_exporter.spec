#软件包简要介绍
Summary: build ceph_exporter
#软件包的名字
Name: ceph_exporter
#软件包的主版本号
Version: 4.2.0
#软件包的次版本号
Release: 2023103066%{?dist}
#源代码包，默认将在上面提到的SOURCES目录中寻找
Source0: %{name}-%{version}.tar.gz
#授权协议
License: GPL
#软件分类
Group: Development/Tools
#去除依赖
AutoReqProv: no
#软件包的内容介绍
%description
ceph_exporter监控消息服务

#表示预操作字段，后面的命令将在源码代码BUILD前执行
%prep

#BUILD字段，将通过直接调用源码目录中自动构建工具完成源码编译操作
%build
cd /go/src/digitalocean/ceph_exporter
go build -o ceph_exporter -tags nautilus
#file

#开始把软件安装到虚拟的根目录中 （即$RPM_BUILD_ROOT）
%install
# 二进制执行文件
mkdir -p ${RPM_BUILD_ROOT}/usr/bin/
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/systemd/system/
cp -f /go/src/digitalocean/ceph_exporter/ceph_exporter ${RPM_BUILD_ROOT}/usr/bin/ceph_exporter

# 控制脚本
cp -f /go/src/digitalocean/ceph_exporter/scripts/ceph_exporter.service ${RPM_BUILD_ROOT}/usr/lib/systemd/system/ceph_exporter.service

# 版本记录
echo "%{version}_%{release}"> /go/src/digitalocean/ceph_exporter/scripts/VERSION

# rpm安装前执行的脚本
%pre
echo -e "Start Install..."

# rpm安装后执行的脚本
%post
# 添加开机自启动
chmod 775 /usr/bin/ceph_exporter
chmod 644 /usr/lib/systemd/system/ceph_exporter.service
systemctl daemon-reload
systemctl enable ceph_exporter.service

echo -e "Install Success"
#echo -e "start log rewrite to /usr/local/ceph_exporter/logs/ \n"

#文件说明字段，声明多余或者缺少都将可能出错
%files
%defattr(-,root,root)
/usr/bin/ceph_exporter
/usr/lib/systemd/system/ceph_exporter.service
 
%dir
# /usr/bin/
# /usr/lib/systemd/system/

#卸载前执行的脚本
%preun
systemctl stop ceph_exporter.service

#卸载后执行的脚本
%postun
echo -e "Uninstall Success"

#清除编译和安装时生成的临时文件
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
rm -rf $RPM_BUILD_DIR/%{name}-%{version}


