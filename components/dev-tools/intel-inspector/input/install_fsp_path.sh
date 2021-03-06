#!/bin/bash

# FSP: install from release rpms into standard FSP path

version=16.0.1.407184
release=inspector_xe_2015_update1
relocate_ver=inspector_xe_20$version

input_dir=../../../compiler-families/intel-compilers/input/update2/parallel_studio_xe_2016_beta

match_keys=intel-inspector
skip_keys=i486.rpm

INSTALL=1
POST_UNINSTALL=1
TARBALL=1

installed_RPMS=""

#for rpm in `ls $release/rpm/*.rpm` `ls $release/CLI_Install/rpm/*.rpm` ; do 

for rpm in `ls $input_dir/rpm/*.rpm`; do

    name=`basename $rpm`

    echo $rpm | egrep -q "$skip_keys" 
    if [ $? -eq 0 ];then
        continue
    fi

    echo $rpm | egrep -q "$match_keys" 
    if [ $? -eq 0 ];then
        echo "detected Inspector $rpm..."
    else
        continue
    fi

    if [ $INSTALL -eq 1 ];then
        echo "installing $rpm...."
        rpm -ivh --nodeps --relocate /opt/intel/$relocate_ver=/opt/fsp/pub/inspector/$version $rpm
        installed_RPMS="$name $installed_RPMS"
    fi
done


if [ $TARBALL -eq 1 ];then
    tar cfz intel-inspector-fsp-$version.tar.gz /opt/fsp/pub/inspector/$version
fi

if [ $POST_UNINSTALL -eq 1 ];then
    echo " "
    for pkg in $installed_RPMS; do 
        localrpm=`basename --suffix=.rpm $pkg`
        echo "[post-install] removing $localrpm...."
        rpm -e --nodeps $localrpm
    done
fi


