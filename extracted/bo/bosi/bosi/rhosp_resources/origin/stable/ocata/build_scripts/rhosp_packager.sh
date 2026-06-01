#!/bin/bash -eux

# Following build params expected for this script:
# OpenStackBranch
# BcfBranch
# IvsBranch (optional)

# Revision is set to a constant 0. If ever this needs changing,
# it can be added to build params
Revision="0"

# mapping for OpenStackBranch to RHOSPVersion, default is latest = 10
# occasionally cleanup when we stop supporting certain versions
RHOSPVersion="10"
case "$OpenStackBranch" in
  *"pike"*) RHOSPVersion="12" ;;
  *"ocata"*) RHOSPVersion="11" ;;
  *"newton"*) RHOSPVersion="10" ;;
  *"mitaka"*) RHOSPVersion="9" ;;
esac

# if IvsBranch is not specified, it is same as BcfBranch
if [ -z "${IvsBranch+x}" ]; then
    IvsBranch="$BcfBranch"
fi

# cleanup old stuff
sudo rm -rf *

# get ivs packages
mkdir ivs
rsync -e 'ssh -o "StrictHostKeyChecking no"' -uva  bigtop:public_html/xenon-bsn/centos7-x86_64/$IvsBranch/latest/* ./ivs

# get networking-bigswitch packages
mkdir networking-bigswitch
rsync -e 'ssh -o "StrictHostKeyChecking no"' -uva  bigtop:public_html/networking-bigswitch/centos7-x86_64/$OpenStackBranch/latest/* ./networking-bigswitch

# since we have special branching for networking-bigswitch, we need to sanitize it for horizon-bsn package
HorizonBsnBranch="$OpenStackBranch"

# get horizon-bsn packages
mkdir horizon-bsn
rsync -e 'ssh -o "StrictHostKeyChecking no"' -uva  bigtop:public_html/horizon-bsn/centos7-x86_64/$HorizonBsnBranch/latest/* ./horizon-bsn

# get bosi packages
mkdir bosi
rsync -e 'ssh -o "StrictHostKeyChecking no"' -uva  bigtop:public_html/bosi/$BcfBranch/latest/* ./bosi

# grunt work aka packaging
mkdir -p tarball/bosi
mv ./bosi/rhosp_resources/$HorizonBsnBranch/ivs/customize.sh ./tarball
mv ./bosi/rhosp_resources/$HorizonBsnBranch/ivs/README ./tarball
mv ./bosi/rhosp_resources/$HorizonBsnBranch/ivs/startup.sh ./tarball
mv ./bosi/rhosp_resources/$HorizonBsnBranch/yamls ./tarball
mv ./bosi/bosi_offline_packages_*tar.gz ./tarball/bosi
mv ./networking-bigswitch/*.noarch.rpm ./tarball
mv ./horizon-bsn/*.noarch.rpm ./tarball
mv ./ivs/*.rpm ./tarball

get_version () {
    RPM=$1;
    B=${RPM##*/};
    B=${B%-*};
    V=${B##*-};
}

# given $BcfBranch is master, IVS_VERSION will be whatever value set in master.
# hence we take it from package name
IVS_VERSION="$IvsBranch"
if [ "$IVS_VERSION" == "master" ]
then
    IVS_PKG="`ls ./tarball/ivs-debug*`"
    get_version $IVS_PKG
    IVS_VERSION=$V
fi

# networking-bigswitch and horizon-bsn is <openstack-version>.<bcf-version>.<bug-fix-id>
# however, to maintain compatibility with lower version of bcf releases,
# $BcfBranch specified for build and latest package's <bcf-version> may not be same.
# e.g. liberty, 3.7 will still use liberty.36.x since liberty was first released with
# BCF 3.6.0 and we want to retain support

BSNLIB_PKG="`ls ./tarball/python-networking-bigswitch*`"
get_version $BSNLIB_PKG
NETWORKING_BIGSWITCH_VERSION=$V

HORIZON_PKG="`ls ./tarball/python-horizon-bsn*`"
get_version $HORIZON_PKG
HORIZON_BSN_VERSION=$V

echo "ivs version is" $IVS_VERSION
echo "networking-bigswitch version is" $NETWORKING_BIGSWITCH_VERSION
echo "horizon-bsn version is" $HORIZON_BSN_VERSION

# IVS_VERSION_REVISION includes ivs version with its revision number, default = -1. redhat naming convention
# that needs to be adhered.
IVS_VERSION_REVISION="$IVS_VERSION""-1"
# for beta releases, revision is preappended, no changes required
# i.e. 4.0.0-beta1 already has revision set to beta1
if [[ "$IVS_VERSION" == *"beta"* ]]
then
    IVS_VERSION_REVISION="$IVS_VERSION"
fi

sed -i -e "s/\${networking_bigswitch_version}/$NETWORKING_BIGSWITCH_VERSION/" -e "s/\${horizon_bsn_version}/$HORIZON_BSN_VERSION/" -e "s/\${ivs_version}/$IVS_VERSION_REVISION/" ./tarball/customize.sh
sed -i -e "s/\${networking_bigswitch_version}/$NETWORKING_BIGSWITCH_VERSION/" -e "s/\${horizon_bsn_version}/$HORIZON_BSN_VERSION/" -e "s/\${ivs_version}/$IVS_VERSION_REVISION/" ./tarball/startup.sh
sed -i -e "s/\${networking_bigswitch_version}/$NETWORKING_BIGSWITCH_VERSION/" -e "s/\${horizon_bsn_version}/$HORIZON_BSN_VERSION/" -e "s/\${ivs_version}/$IVS_VERSION_REVISION/" ./tarball/README

DATE=`date +%Y-%m-%d-%H-%M-%S`
TAR_NAME="BCF-RHOSP-$RHOSPVersion-plugins-$IVS_VERSION.$Revision-$DATE"
mv tarball $TAR_NAME
tar -zcvf $TAR_NAME.tar.gz $TAR_NAME

# Copy built tarball to pkg/
OUTDIR=$(readlink -m "pkg/$OpenStackBranch/$TAR_NAME")
rm -rf "$OUTDIR" && mkdir -p "$OUTDIR"
mv $TAR_NAME.tar.gz "$OUTDIR"
ln -snf $(basename $OUTDIR) $OUTDIR/../latest
