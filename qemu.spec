%bcond_with    x86only          # disabled
%bcond_with    exclusive_x86_64 # disabled
%bcond_without rbd              # enabled
%bcond_without fdt              # enabled

%define _disable_ld_no_undefined 1

%define _udevdir /lib/udev/rules.d
%define qemudocdir %{_docdir}/%{name}

Summary:	QEMU CPU Emulator
Name:		qemu
Version:	1.5.0
Release:	1
License:	GPLv2+ and LGPLv2+ and BSD
Group:		Emulators
Url:		http://wiki.qemu.org/Main_Page
Source0:	http://wiki.qemu.org/download/%{name}-%{version}.tar.bz2

%define qemu_snapshot	0
#Release:	%{?qemu_snapshot:0.%{qemu_snapshot}.}1
#Source0:	http://wiki.qemu.org/download/%{name}-%{version}%{?qemu_snapshot:-%{qemu_snapshot}}.tar.bz2

Source1:	qemu.binfmt

# Loads kvm kernel modules at boot
Source2:	kvm.modules

# Creates /dev/kvm
Source3:	80-kvm.rules

# KSM control scripts
Source4:	ksm.service
Source5:	ksm.sysconfig
Source6:	ksmctl.c
Source7:	ksmtuned.service
Source8:	ksmtuned
Source9:	ksmtuned.conf

Source10:	qemu-guest-agent.service
Source11:	99-qemu-guest-agent.rules
Source100:	qemu.rpmlintrc

# Non upstream build fix

# Add ./configure --disable-kvm-options
# keep: Carrying locally until qemu-kvm is fully merged into qemu.git
Patch2:	0002-configure-Add-disable-kvm-options.patch

ExclusiveArch:	%{ix86} ppc x86_64 amd64 %{sparcx}

BuildRequires:	dev86
BuildRequires:	iasl
BuildRequires:	kernel-headers
BuildRequires:	libtool
BuildRequires:	systemtap
BuildRequires:	texi2html
BuildRequires:	texinfo
BuildRequires:	brlapi-devel
BuildRequires:	sasl-devel
BuildRequires:	usbredir-devel >= 0.5.2
BuildRequires:	xfsprogs-devel
BuildRequires:	attr-devel
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(gnutls) >= 3.0
#BuildRequires:	pkgconfig(libcacard)
BuildRequires:	pkgconfig(libcap-ng)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libseccomp)
BuildRequires:	pkgconfig(libusbredirhost) >=0.5.2
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(spice-server)
BuildRequires:	pkgconfig(spice-protocol)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(vte)

#not ready yet
#%if %{with fdt}
# For FDT device tree support
#BuildRequires: libfdt-devel
#%endif
#%if %{with rbd}
## For rbd block driver
#BuildRequires: ceph-devel
#%endif

Requires:	qemu-img = %{EVRD}
#Requires:	libcacard-tools
# for %%{_sysconfdir}/sasl2
Requires:	cyrus-sasl
Requires:	vgabios >= 0.6c
Requires:	seabios-bin >= 0.6.0-1
Requires:	sgabios-bin
Requires:	ipxe-roms-qemu
%rename		kvm

%description
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation. QEMU has two operating modes:

* Full system emulation. In this mode, QEMU emulates a full system (for
  example a PC), including a processor and various peripherials. It can be
  used to launch different Operating Systems without rebooting the PC or
  to debug system code.
* User mode emulation. In this mode, QEMU can launch Linux processes compiled
  for one CPU on another CPU.

As QEMU requires no host kernel patches to run, it is safe and easy to use.

%package	img
Summary:	QEMU disk image utility
Group:		Emulators
Conflicts:	qemu < 0.9.0-3

%description	img
This package contains the QEMU disk image utility that is used to
create, commit, convert and get information from a disk image.

%prep
%setup -q
%apply_patches

%build
#(proyvind): binutils upstream bug #10862, linking with gold fails if doing parallel build
mkdir -p bfd
ln -s %{_bindir}/ld.bfd bfd/ld
export PATH=$PWD/bfd:$PATH
buildarch="i386-softmmu x86_64-softmmu arm-softmmu cris-softmmu \
    m68k-softmmu mips-softmmu mipsel-softmmu mips64-softmmu \
    mips64el-softmmu sh4-softmmu sh4eb-softmmu sparc-softmmu sparc64-softmmu \
    ppc-softmmu ppcemb-softmmu ppc64-softmmu \
    i386-linux-user x86_64-linux-user alpha-linux-user arm-linux-user \
    armeb-linux-user cris-linux-user m68k-linux-user mips-linux-user \
    mipsel-linux-user ppc-linux-user ppc64-linux-user \
    ppc64abi32-linux-user sh4-linux-user sh4eb-linux-user \
    sparc-linux-user sparc64-linux-user sparc32plus-linux-user"
%if %{with x86only}
    buildarch="i386-softmmu x86_64-softmmu i386-linux-user x86_64-linux-user"
%endif

# Targets we don't build as of qemu 1.1.50
# alpha-softmmu lm32-softmmu microblaze-softmmu microblazeel-softmmu
# or32-softmmu s390x-softmmu xtensa-softmmu xtensaeb-softmmu unicore32-softmmu
# alpha-linux-user microblaze-linux-user microblazeel-linux-user
# or32-linux-user unicore32-linux-user s390x-linux-user


# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

%ifarch s390
# drop -g flag to prevent memory exhaustion by linker
%global optflags %(echo %{optflags} | sed 's/-g//')
sed -i.debug 's/"-g $CFLAGS"/"$CFLAGS"/g' configure
%endif


dobuild() {
    ./configure \
        --prefix=%{_prefix} \
        --sysconfdir=%{_sysconfdir} \
        --interp-prefix=%{_prefix}/qemu-%%M \
        --audio-drv-list=pa,sdl,alsa,oss \
        --disable-strip \
        --extra-ldflags="$extraldflags -pie -Wl,-z,relro -Wl,-z,now" \
        --extra-cflags="%{optflags} -fPIE -DPIE -fuse-ld=bfd" \
%ifarch %{ix86} x86_64
        --enable-spice \
        --enable-mixemu \
        --enable-seccomp \
	--enable-virtfs \
%endif
%if %{without rbd}
        --disable-rbd \
%endif
%if %{without fdt}
        --disable-fdt \
%endif
        --enable-trace-backend=dtrace \
        --disable-werror \
        --disable-xen \
        --enable-kvm \
	--disable-smartcard-nss \
        "$@"

    echo "config-host.mak contents:"
    echo "==="
    cat config-host.mak
    echo "==="

    %make V=1 $buildldflags
}

# This is kind of confusing. We run ./configure + make twice here to
# preserve some back compat: if on x86, we want to provide a qemu-kvm
# binary that defaults to KVM=on. All other qemu-system* should be
# able to use KVM, but default to KVM=off (upstream qemu semantics).
#
# Once qemu-kvm and qemu fully merge, and we base off qemu releases,
# all qemu-system-* will default to KVM=off, so we hopefully won't need
# to do these double builds. But then I'm not sure how we are going to
# generate a back compat qemu-kvm binary...

%ifarch %{ix86} x86_64
# Build qemu-kvm back compat binary
dobuild --target-list=x86_64-softmmu

# Setup back compat qemu-kvm binary which defaults to KVM=on
./scripts/tracetool.py --backend dtrace --format stap \
  --binary %{_bindir}/qemu-kvm --target-arch x86_64 --target-type system \
  --probe-prefix qemu.kvm < ./trace-events > qemu-kvm.stp
cp -a x86_64-softmmu/qemu-system-x86_64 qemu-kvm
make clean
%endif

# Build qemu-system-* with consistent default of kvm=off
dobuild --target-list="$buildarch" --disable-kvm-options
gcc %{SOURCE6} -O2 -g -o ksmctl

%install
install -D -p -m 0755 %{SOURCE4} %{buildroot}/%{_unitdir}/ksm.service
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl %{buildroot}/lib/systemd/ksmctl

install -D -p -m 0755 %{SOURCE7} %{buildroot}/%{_unitdir}/ksmtuned.service
install -D -p -m 0755 %{SOURCE8} %{buildroot}%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE9} %{buildroot}%{_sysconfdir}/ksmtuned.conf

%ifarch %{ix86} x86_64
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/modules
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_udevdir}
mkdir -p %{buildroot}%{_datadir}/systemtap/tapset

install -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 scripts/kvm/kvm_stat %{buildroot}%{_bindir}/
install -m 0755 qemu-kvm %{buildroot}%{_bindir}/
install -m 0644 qemu-kvm.stp %{buildroot}%{_datadir}/systemtap/tapset/
install -m 0644 %{SOURCE3} %{buildroot}%{_udevdir}
%endif

%makeinstall_std
chmod -x %{buildroot}%{_mandir}/man1/*
install -D -p -m 0644 -t %{buildroot}%{qemudocdir} Changelog README COPYING COPYING.LIB LICENSE

install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

# Provided by package ipxe
rm -rf %{buildroot}%{_datadir}/%{name}/pxe*rom
# Provided by package vgabios
rm -rf %{buildroot}%{_datadir}/%{name}/vgabios*bin
# Provided by package seabios
rm -rf %{buildroot}%{_datadir}/%{name}/bios.bin
# Provided by package sgabios
rm -rf %{buildroot}%{_datadir}/%{name}/sgabios.bin
# Provided by package openbios
#needed this:
#BuildRequires:  gcc-powerpc64-linux-gnu
#BuildRequires:  gcc-sparc64-linux-gnu
#rm -rf %{buildroot}%{_datadir}/%{name}/openbios-ppc
#rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc32
#rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc64
# Provided by package SLOF
#gcc-powerpc64-linux-gnu needed
#rm -rf % {buildroot} % {_datadir}/% {name}/slof.bin

# remove unpackaged files on x86only:
%if %{with x86only}
rm -f %{buildroot}%{_datadir}/%{name}/bamboo.dtb
rm -f %{buildroot}%{_datadir}/%{name}/ppc_rom.bin
rm -f %{buildroot}%{_datadir}/%{name}/spapr-rtas.bin
%endif

# The following aren't provided by any Fedora package

# Used by target s390/s390x
#rm -rf %{buildroot}%{_datadir}/%{name}/s390-zipl.rom
#rm -rf %{buildroot}%{_datadir}/%{name}/palcode-clipper
# Binary device trees for microblaze target
#rm -rf %{buildroot}%{_datadir}/%{name}/petalogix*.dtb


# the pxe gpxe images will be symlinks to the images on
# /usr/share/ipxe, as QEMU doesn't know how to look
# for other paths, yet.
pxe_link() {
  ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/%{name}/pxe-$1.rom
}

pxe_link e1000 8086100e
pxe_link ne2k_pci 10ec8029
pxe_link pcnet 10222000
pxe_link rtl8139 10ec8139
pxe_link virtio 1af41000

rom_link() {
    ln -s $1 %{buildroot}%{_datadir}/%{name}/$2
}

rom_link ../vgabios/VGABIOS-lgpl-latest.bin vgabios.bin
rom_link ../vgabios/VGABIOS-lgpl-latest.cirrus.bin vgabios-cirrus.bin
rom_link ../vgabios/VGABIOS-lgpl-latest.qxl.bin vgabios-qxl.bin
rom_link ../vgabios/VGABIOS-lgpl-latest.stdvga.bin vgabios-stdvga.bin
rom_link ../vgabios/VGABIOS-lgpl-latest.vmware.bin vgabios-vmware.bin
rom_link ../seabios/bios.bin bios.bin
rom_link ../sgabios/sgabios.bin sgabios.bin

mkdir -p %{buildroot}%{_exec_prefix}/lib/binfmt.d
for i in dummy \
%ifnarch %{ix86} x86_64
    qemu-i386 \
%endif
%if %{without x86only}
%ifnarch alpha
    qemu-alpha \
%endif
%ifnarch arm
    qemu-arm \
%endif
    qemu-armeb \
%ifnarch mips
    qemu-mips qemu-mipsn32 qemu-mips64 \
%endif
%ifnarch mipsel
    qemu-mipsel qemu-mipsn32el qemu-mips64el \
%endif
%ifnarch m68k
    qemu-m68k \
%endif
%ifnarch ppc ppc64
    qemu-ppc \
%endif
%ifnarch sparc sparc64
    qemu-sparc \
%endif
%ifnarch s390 s390x
    qemu-s390x \
%endif
%ifnarch sh4
    qemu-sh4 \
%endif
    qemu-sh4eb \
%endif
; do
  test $i = dummy && continue
  grep /$i:\$ %{SOURCE1} > %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i.conf
  chmod 644 %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i.conf
done < %{SOURCE1}

# For the qemu-guest-agent subpackage install the systemd
# service and udev rules.
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_udevdir}
install -m 0644 %{SOURCE10} %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE11} %{buildroot}%{_udevdir}

%find_lang %{name}


%post 
%ifarch %{ix86} x86_64
sh %{_sysconfdir}/sysconfig/modules/kvm.modules || :
udevadm trigger --sysname-match=kvm || :
%endif

%_post_service ksmtuned.service
%_post_service ksm.service
%_post_service qemu-guest-agent.service

%preun
%_preun_service ksm.service
%_preun_service ksmtuned.service
%_preun_service qemu-guest-agent.service

%triggerpostun -- qemu < 0.10.4-6
rm -f /etc/rc.d/*/{K,S}??qemu

%files -f %{name}.lang
%doc README qemu-doc.html qemu-tech.html
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
%{_unitdir}/ksm.service
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%{_unitdir}/ksmtuned.service
%{_sbindir}/ksmtuned
%{_unitdir}/qemu-guest-agent.service
%{_udevdir}/99-qemu-guest-agent.rules
%{_udevdir}/80-kvm.rules
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%{_sysconfdir}/sysconfig/modules/kvm.modules
%{_sysconfdir}/qemu/target-x86_64.conf
%{_bindir}/kvm_stat
%{_bindir}/qemu-io
%{_bindir}/qemu-kvm
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm*
%{_bindir}/qemu-cris
%{_bindir}/qemu-ga
%{_bindir}/qemu-i386
%{_bindir}/qemu-m68k
%{_bindir}/qemu-mips*
%{_bindir}/qemu-nbd
%{_bindir}/qemu-ppc*
%{_bindir}/qemu-sh4*
%{_bindir}/qemu-sparc*
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-system-arm
%{_bindir}/qemu-system-cris
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-m68k
%{_bindir}/qemu-system-sh4*
%{_bindir}/qemu-system-ppc*
%{_bindir}/qemu-system-mips*
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-sparc64
%{_bindir}/qemu-system-x86_64
#% {_bindir}/qmp-shell
#conflicts with cacard-tools
#% {_bindir}/vscclient
%{_bindir}/virtfs-proxy-helper
/lib/systemd/ksmctl
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/virtfs-proxy-helper.1*
%{_mandir}/man8/qemu-nbd.8*
%{_prefix}/libexec/qemu-bridge-helper
%dir %{_datadir}/qemu
%{_datadir}/qemu/*.bin
%{_datadir}/qemu/*.rom
%{_datadir}/qemu/*.img
%{_datadir}/qemu/*.aml
%{_datadir}/qemu/keymaps
%{_datadir}/qemu/openbios-sparc32
%{_datadir}/qemu/openbios-sparc64
%{_datadir}/qemu/openbios-ppc
%{_datadir}/qemu/bamboo.dtb
#%{_datadir}/qemu/mpc8544ds.dtb
%{_datadir}/qemu/palcode-clipper
%{_datadir}/qemu/petalogix-ml605.dtb
%{_datadir}/qemu/petalogix-s3adsp1800.dtb
%{_datadir}/qemu/qemu-icon.bmp

%{_datadir}/systemtap/tapset/qemu-alpha.stp
%{_datadir}/systemtap/tapset/qemu-arm.stp
%{_datadir}/systemtap/tapset/qemu-armeb.stp
%{_datadir}/systemtap/tapset/qemu-cris.stp
%{_datadir}/systemtap/tapset/qemu-m68k.stp
%{_datadir}/systemtap/tapset/qemu-mips.stp
%{_datadir}/systemtap/tapset/qemu-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-ppc.stp
%{_datadir}/systemtap/tapset/qemu-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-ppc64abi32.stp
%{_datadir}/systemtap/tapset/qemu-sh4.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb.stp
%{_datadir}/systemtap/tapset/qemu-sparc.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus.stp
%{_datadir}/systemtap/tapset/qemu-sparc64.stp
#%{_datadir}/systemtap/tapset/qemu-kvm.stp
%{_datadir}/systemtap/tapset/qemu-system-i386.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64.stp
%{_datadir}/systemtap/tapset/qemu-system-mips.stp
%{_datadir}/systemtap/tapset/qemu-system-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64el.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64.stp
%{_datadir}/systemtap/tapset/qemu-system-m68k.stp
%{_datadir}/systemtap/tapset/qemu-system-cris.stp
%{_datadir}/systemtap/tapset/qemu-system-sh4.stp
%{_datadir}/systemtap/tapset/qemu-system-sh4eb.stp
%{_datadir}/systemtap/tapset/qemu-system-sparc.stp
%{_datadir}/systemtap/tapset/qemu-system-sparc64.stp
%{_datadir}/systemtap/tapset/qemu-system-ppc.stp
%{_datadir}/systemtap/tapset/qemu-system-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-system-ppcemb.stp
%{_datadir}/systemtap/tapset/qemu-system-arm.stp
%{_datadir}/systemtap/tapset/qemu-kvm.stp
%{_datadir}/systemtap/tapset/qemu-x86_64.stp
%{_datadir}/systemtap/tapset/qemu-i386.stp

%{_exec_prefix}/lib/binfmt.d/qemu-*.conf

#% {py_platsitedir}/qmp.py

%files img
%{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*
