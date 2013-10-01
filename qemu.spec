# build-time settings that support --with or --without:
#
%bcond_with    exclusive_x86_64 # disabled
%bcond_without rbd              # enabled
%bcond_without xfsprogs         # enabled
%bcond_without separate_kvm     # enabled
%bcond_without gtk              # enabled
%bcond_without usbredir         # enabled
# enable it!!!
%bcond_with spice            # disabled
%ifarch %{ix86} x86_64
%bcond_without seccomp          # enabled
%else
%bcond_with seccomp             # disabled
%endif

# libfdt is only needed to build ARM, Microblaze or PPC emulators
%bcond_without fdt

%if %{with separate_kvm}
%define kvm_archs %{ix86} x86_64 ppc64 s390x armv7hl
%else
%define kvm_archs %{ix86} ppc64 s390x armv7hl
%endif
%if %{with exclusive_x86_64}
%define kvm_archs x86_64
%endif


%define need_kvm_modfile 0

%ifarch %{ix86}
%define system_x86    kvm
%define kvm_package   system-x86
%define kvm_target    i386
%define need_qemu_kvm 1
%endif
%ifarch x86_64
%define system_x86    kvm
%define kvm_package   system-x86
%define kvm_target    x86_64
%define need_qemu_kvm 1
%endif
%ifarch ppc64
%define system_ppc    kvm
%define kvm_package   system-ppc
%define kvm_target    ppc64
%define need_kvm_modfile 1
%endif
%ifarch s390x
%define system_s390x  kvm
%define kvm_package   system-s390x
%define kvm_target    s390x
%define need_kvm_modfile 1
%endif
%ifarch armv7hl
%define system_arm    kvm
%define kvm_package   system-arm
%define kvm_target    arm
%define need_qemu_kvm 1
%endif

%define user          user
%define system_alpha  system-alpha
%define system_arm    system-arm
%define system_cris   system-cris
%define system_lm32   system-lm32
%define system_m68k   system-m68k
%define system_microblaze   system-microblaze
%define system_mips   system-mips
%define system_or32   system-or32
%define system_ppc    system-ppc
%define system_s390x  system-s390x
%define system_sh4    system-sh4
%define system_sparc  system-sparc
%define system_x86    system-x86
%define system_xtensa   system-xtensa
%define system_unicore32   system-unicore32
%define system_moxie   system-moxie


Summary:	QEMU is a FAST! processor emulator
Name:		qemu
Version:	1.6.0
Release:	2
Epoch:		2
License:	GPLv2+ and LGPLv2+ and BSD
Group:		Emulators
URL:		http://www.qemu.org/

# OOM killer breaks builds with parallel make on s390(x)
%ifarch s390 s390x
%define _smp_mflags %{nil}
%endif

Source0:	http://wiki.qemu-project.org/download/%{name}-%{version}.tar.bz2


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
Source12:	bridge.conf

# qemu-kvm back compat wrapper
Source13:	qemu-kvm.sh
Source100:	qemu.rpmlintrc

# qemu-kvm migration compat (not for upstream, drop by Fedora 21?)
Patch0001: 0001-Fix-migration-from-qemu-kvm.patch

BuildRequires:		pkgconfig(sdl)
BuildRequires:		pkgconfig(zlib)
BuildRequires:		texi2html
BuildRequires:		pkgconfig(gnutls)
BuildRequires:		sasl-devel
BuildRequires:		libtool
BuildRequires:		libaio-devel
BuildRequires:		rsync
BuildRequires:		pkgconfig(libpci)
BuildRequires:		pkgconfig(libpulse)
BuildRequires:		pkgconfig(libiscsi)
BuildRequires:		alsa-oss-devel
BuildRequires:		ncurses-devel
BuildRequires:		attr-devel
%if %{with usbredir}
BuildRequires: usbredir-devel >= 0.5.2
%endif
BuildRequires: texinfo
%if %{with spice}
BuildRequires:		pkgconfig(spice-server)
BuildRequires:		pkgconfig(spice-protocol)
%endif
%if %{with seccomp}
BuildRequires:		pkgconfig(libseccomp)
%endif
# For network block driver
BuildRequires:		pkgconfig(libcurl)
%if %{with rbd}
# For rbd block driver
BuildRequires:		%{_lib}ceph-devel
%endif
# We need both because the 'stap' binary is probed for by configure
BuildRequires:		systemtap
BuildRequires:		systemtap-devel
# For smartcard NSS support
BuildRequires:		nss-devel
# For XFS discard support in raw-posix.c
%if %{with xfsprogs}
BuildRequires:		xfsprogs-devel
%endif
# For VNC JPEG support
BuildRequires:		jpeg-devel
# For VNC PNG support
BuildRequires:		pkgconfig(libpng)
# For uuid generation
BuildRequires:		pkgconfig(uuid)
# For BlueZ device support
BuildRequires:		pkgconfig(bluez)
# For Braille device support
BuildRequires:		brlapi-devel
%if %{with fdt}
# For FDT device tree support
BuildRequires:		fdt-devel
%endif
# For virtfs
BuildRequires:		pkgconfig(libcap-ng)
# Hard requirement for version >= 1.3
BuildRequires:		pkgconfig(pixman-1)
%if 0%{?fedora} > 18
# For gluster support
BuildRequires: glusterfs-devel >= 3.4.0
BuildRequires: glusterfs-api-devel >= 3.4.0
%endif
# Needed for usb passthrough for qemu >= 1.5
BuildRequires:		pkgconfig(libusb-1.0) 
# SSH block driver
BuildRequires:		pkgconfig(libssh)
%if %{with gtk}
# GTK frontend
BuildRequires:		pkgconfig(gtk+-3.0)
BuildRequires:		pkgconfig(vte)
%endif
# GTK translations
BuildRequires:		gettext
# RDMA migration
BuildRequires: librdmacm-devel

%if 0%{?user:1}
Requires: %{name}-%{user} = %{version}-%{release}
%endif
%if 0%{?system_alpha:1}
Requires: %{name}-%{system_alpha} = %{version}-%{release}
%endif
%if 0%{?system_arm:1}
Requires: %{name}-%{system_arm} = %{version}-%{release}
%endif
%if 0%{?system_cris:1}
Requires: %{name}-%{system_cris} = %{version}-%{release}
%endif
%if 0%{?system_lm32:1}
Requires: %{name}-%{system_lm32} = %{version}-%{release}
%endif
%if 0%{?system_m68k:1}
Requires: %{name}-%{system_m68k} = %{version}-%{release}
%endif
%if 0%{?system_microblaze:1}
Requires: %{name}-%{system_microblaze} = %{version}-%{release}
%endif
%if 0%{?system_mips:1}
Requires: %{name}-%{system_mips} = %{version}-%{release}
%endif
%if 0%{?system_or32:1}
Requires: %{name}-%{system_or32} = %{version}-%{release}
%endif
%if 0%{?system_ppc:1}
Requires: %{name}-%{system_ppc} = %{version}-%{release}
%endif
%if 0%{?system_s390x:1}
Requires: %{name}-%{system_s390x} = %{version}-%{release}
%endif
%if 0%{?system_sh4:1}
Requires: %{name}-%{system_sh4} = %{version}-%{release}
%endif
%if 0%{?system_sparc:1}
Requires: %{name}-%{system_sparc} = %{version}-%{release}
%endif
%if 0%{?system_unicore32:1}
Requires: %{name}-%{system_unicore32} = %{version}-%{release}
%endif
%if 0%{?system_x86:1}
Requires: %{name}-%{system_x86} = %{version}-%{release}
%endif
%if 0%{?system_xtensa:1}
Requires: %{name}-%{system_xtensa} = %{version}-%{release}
%endif
%if 0%{?system_moxie:1}
Requires: %{name}-%{system_moxie} = %{version}-%{release}
%endif
%if %{without separate_kvm}
Requires: %{name}-img = %{version}-%{release}
%else
Requires: %{name}-img
%endif

%define qemudocdir %{_docdir}/%{name}

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

%ifarch		%{kvm_archs}
%package	kvm
Summary:	QEMU metapackage for KVM support
Group:		Emulators
Requires:	qemu-%{kvm_package} = %{version}-%{release}

%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86
%endif

%package	img
Summary:	QEMU command line tool for manipulating disk images
Group:		Emulators
Requires:	libcacard-tools

%description	img
This package provides a command line tool for manipulating disk images

%package	common
Summary: QEMU common files needed by all QEMU targets
Group: Emulators
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(postun): rpm-helper
%description	common
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the common files needed by all QEMU targets

%package	guest-agent
Summary:	QEMU guest agent
Group:		Emulators
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(postun): rpm-helper

%description guest-agent
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.

%post guest-agent
%_post_service qemu-guest-agent.service

%preun guest-agent
%_preun_service qemu-guest-agent.service

%package -n	ksm
Summary:	Kernel Samepage Merging services
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}
Requires(post): rpm-helper
Requires(postun): rpm-helper

%description -n ksm
Kernel Samepage Merging (KSM) is a memory-saving de-duplication feature,
that merges anonymous (private) pages (not pagecache ones).

This package provides service files for disabling and tuning KSM.

%if 0%{?user:1}
%package	%{user}
Summary:	QEMU user mode emulation of qemu targets
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}
Requires(post): rpm-helper
Requires(postun): rpm-helper

%description	%{user}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets
%endif

%if 0%{?system_x86:1}
%package	%{system_x86}
Summary:	QEMU system emulator for x86
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}
Requires:	seavgabios-bin
# First version that ships aml files which we depend on
Requires:	seabios-bin >= 1.7.3-2
Requires:	seavgabios-bin
Requires:	sgabios-bin
Requires:	ipxe-roms-qemu

%description %{system_x86}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.

%package -n	seavgabios-bin
Summary:	SeaVGABIOS is an open-source VGABIOS implementation
Group:		Emulators

%description -n seavgabios-bin	
SeaVGABIOS is an open-source VGABIOS implementation.
%endif

%if 0%{?system_alpha:1}
%package	%{system_alpha}
Summary:	QEMU system emulator for Alpha
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}

%description	%{system_alpha}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Alpha systems.
%endif

%if 0%{?system_arm:1}
%package	%{system_arm}
Summary:	QEMU system emulator for ARM
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}
%description %{system_arm}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ARM boards.
%endif

%if 0%{?system_mips:1}
%package	%{system_mips}
Summary:	QEMU system emulator for MIPS
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}

%description	%{system_mips}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for MIPS boards.
%endif

%if 0%{?system_cris:1}
%package	%{system_cris}
Summary:	QEMU system emulator for CRIS
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}

%description	%{system_cris}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for CRIS boards.
%endif

%if 0%{?system_lm32:1}
%package	%{system_lm32}
Summary:	QEMU system emulator for LatticeMico32
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}
%description	%{system_lm32}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for LatticeMico32 boards.
%endif

%if 0%{?system_m68k:1}
%package	%{system_m68k}
Summary:	QEMU system emulator for ColdFire (m68k)
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}

%description	%{system_m68k}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ColdFire boards.
%endif

%if 0%{?system_microblaze:1}
%package	%{system_microblaze}
Summary:	QEMU system emulator for Microblaze
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}

%description	%{system_microblaze}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Microblaze boards.
%endif

%if 0%{?system_or32:1}
%package	%{system_or32}
Summary:	QEMU system emulator for OpenRisc32
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}

%description	%{system_or32}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for OpenRisc32 boards.
%endif

%if 0%{?system_s390x:1}
%package	%{system_s390x}
Summary:	QEMU system emulator for S390
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}
%description	%{system_s390x}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for S390 systems.
%endif

%if 0%{?system_sh4:1}
%package	%{system_sh4}
Summary:	QEMU system emulator for SH4
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}

%description	%{system_sh4}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SH4 boards.
%endif

%if 0%{?system_sparc:1}
%package	%{system_sparc}
Summary:	QEMU system emulator for SPARC
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}
Requires:	openbios

%description	%{system_sparc}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SPARC and SPARC64 systems.

%endif

%package -n	openbios
Summary:	QEMU openbios for SPARC and PPC
Group:		Emulators

%description -n	openbios
This package provides an openbios for SPARC and PPC

%if 0%{?system_ppc:1}
%package	%{system_ppc}
Summary:	QEMU system emulator for PPC
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}
Requires:	SLOF

%description %{system_ppc}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for PPC and PPC64 systems.

%package -n	SLOF
Summary:	Slimline Open Firmware (SLOF)
Group:		Emulators

%description -n	SLOF
The SLOF source code provides illustrates what's needed to initialize
and boot Linux or a hypervisor on the industry Open Firmware boot standard.

%endif

%if 0%{?system_xtensa:1}
%package	%{system_xtensa}
Summary:	QEMU system emulator for Xtensa
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}

%description	%{system_xtensa}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Xtensa boards.
%endif

%if 0%{?system_unicore32:1}
%package	%{system_unicore32}
Summary:	QEMU system emulator for Unicore32
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}

%description	%{system_unicore32}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Unicore32 boards.
%endif

%if 0%{?system_moxie:1}
%package	%{system_moxie}
Summary:	QEMU system emulator for Moxie
Group:		Emulators
Requires:	%{name}-common = %{version}-%{release}

%description	%{system_moxie}
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Moxie boards.
%endif

%ifarch %{kvm_archs}
%package	kvm-tools
Summary:	KVM debugging and diagnostics tools
Group:		Emulators

%description	kvm-tools
This package contains some diagnostics and debugging tools for KVM,
such as kvm_stat.
%endif

%prep
%setup -q

# qemu-kvm migration compat (not for upstream, drop by Fedora 21?)
%patch0001 -p1


%build
buildarch="i386-softmmu x86_64-softmmu alpha-softmmu arm-softmmu \
    cris-softmmu lm32-softmmu m68k-softmmu microblaze-softmmu \
    microblazeel-softmmu mips-softmmu mipsel-softmmu mips64-softmmu \
    mips64el-softmmu or32-softmmu ppc-softmmu ppcemb-softmmu ppc64-softmmu \
    s390x-softmmu sh4-softmmu sh4eb-softmmu sparc-softmmu sparc64-softmmu \
    xtensa-softmmu xtensaeb-softmmu unicore32-softmmu moxie-softmmu \
    i386-linux-user x86_64-linux-user alpha-linux-user arm-linux-user \
    armeb-linux-user cris-linux-user m68k-linux-user \
    microblaze-linux-user microblazeel-linux-user mips-linux-user \
    mipsel-linux-user mips64-linux-user mips64el-linux-user \
    mipsn32-linux-user mipsn32el-linux-user \
    or32-linux-user ppc-linux-user ppc64-linux-user \
    ppc64abi32-linux-user s390x-linux-user sh4-linux-user sh4eb-linux-user \
    sparc-linux-user sparc64-linux-user sparc32plus-linux-user \
    unicore32-linux-user"

# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

%ifarch s390
# drop -g flag to prevent memory exhaustion by linker
%define optflags %(echo %{optflags} | sed 's/-g//')
sed -i.debug 's/"-g $CFLAGS"/"$CFLAGS"/g' configure
%endif


dobuild() {
    ./configure \
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --sysconfdir=%{_sysconfdir} \
        --interp-prefix=%{_prefix}/qemu-%%M \
        --audio-drv-list=pa,sdl,alsa,oss \
        --localstatedir=%{_localstatedir} \
        --libexecdir=%{_libexecdir} \
        --disable-strip \
        --extra-ldflags="$extraldflags -pie -Wl,-z,relro -Wl,-z,now" \
        --extra-cflags="%{optflags} -fPIE -DPIE" \
        --enable-mixemu \
        --enable-trace-backend=dtrace \
        --disable-werror \
        --disable-xen \
        --enable-kvm \
%if %{with spice}
        --enable-spice \
%endif
%if %{with seccomp}
        --enable-seccomp \
%endif
%if %{without rbd}
        --disable-rbd \
%endif
%if %{with fdt}
        --enable-fdt \
%else
        --disable-fdt \
%endif
%if %{with gtk}
        --with-gtkabi="3.0" \
%endif
        --enable-tpm \
        "$@"

    echo "config-host.mak contents:"
    echo "==="
    cat config-host.mak
    echo "==="

    make V=1 %{?_smp_mflags} $buildldflags
}

dobuild --target-list="$buildarch"

gcc %{SOURCE6} -O2 -g -o ksmctl


%install

%define _udevdir /lib/udev/rules.d

install -D -p -m 0644 %{SOURCE4} %{buildroot}/lib/systemd/system/ksm.service
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl %{buildroot}/lib/systemd/ksmctl

install -D -p -m 0644 %{SOURCE7} %{buildroot}/lib/systemd/system/ksmtuned.service
install -D -p -m 0755 %{SOURCE8} %{buildroot}%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE9} %{buildroot}%{_sysconfdir}/ksmtuned.conf

%ifarch %{kvm_archs}
%if 0%{?need_kvm_modfile}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/modules
install -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/modules/kvm.modules
%endif

mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_udevdir}

install -m 0755 scripts/kvm/kvm_stat %{buildroot}%{_bindir}/
install -m 0644 %{SOURCE3} %{buildroot}%{_udevdir}
%endif

make DESTDIR=%{buildroot} install

%if 0%{?need_qemu_kvm}
install -m 0755 %{SOURCE13} %{buildroot}%{_bindir}/qemu-kvm
%endif

chmod -x %{buildroot}%{_mandir}/man1/*
install -D -p -m 0644 -t %{buildroot}%{qemudocdir} Changelog README COPYING COPYING.LIB LICENSE
for emu in %{buildroot}%{_bindir}/qemu-system-*; do
    ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/$(basename $emu).1.gz
done
%if 0%{?need_qemu_kvm}
ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/qemu-kvm.1.gz
%endif

install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

# Provided by package SLOF
# rm -rf %{buildroot}%{_datadir}/%{name}/slof.bin

# Remove possibly unpackaged files.  Unlike others that are removed
# unconditionally, these firmware files are still distributed as a binary
# together with the qemu package.  We should try to move at least s390-zipl.rom
# to a separate package...  Discussed here on the packaging list:
# https://lists.fedoraproject.org/pipermail/packaging/2012-July/008563.html
%if 0%{!?system_alpha:1}
rm -rf %{buildroot}%{_datadir}/%{name}/palcode-clipper
%endif
%if 0%{!?system_microblaze:1}
rm -rf %{buildroot}%{_datadir}/%{name}/petalogix*.dtb
%endif
%if 0%{!?system_ppc:1}
rm -f %{buildroot}%{_datadir}/%{name}/bamboo.dtb
rm -f %{buildroot}%{_datadir}/%{name}/ppc_rom.bin
rm -f %{buildroot}%{_datadir}/%{name}/spapr-rtas.bin
%endif
%if 0%{!?system_s390x:1}
rm -rf %{buildroot}%{_datadir}/%{name}/s390-zipl.rom
rm -rf %{buildroot}%{_datadir}/%{name}/s390-ccw.img
%endif

# Provided by package ipxe
rm -rf %{buildroot}%{_datadir}/%{name}/pxe*rom
rm -rf %{buildroot}%{_datadir}/%{name}/efi*rom
# Provided by package seabios
rm -rf %{buildroot}%{_datadir}/%{name}/bios.bin
rm -rf %{buildroot}%{_datadir}/%{name}/acpi-dsdt.aml
rm -rf %{buildroot}%{_datadir}/%{name}/q35-acpi-dsdt.aml
# Provided by package sgabios
rm -rf %{buildroot}%{_datadir}/%{name}/sgabios.bin

%if 0%{?system_x86:1}
# the pxe gpxe images will be symlinks to the images on
# /usr/share/ipxe, as QEMU doesn't know how to look
# for other paths, yet.
pxe_link() {
  ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/%{name}/pxe-$1.rom
  ln -s ../ipxe.efi/$2.rom %{buildroot}%{_datadir}/%{name}/efi-$1.rom
}

pxe_link e1000 8086100e
pxe_link ne2k_pci 10ec8029
pxe_link pcnet 10222000
pxe_link rtl8139 10ec8139
pxe_link virtio 1af41000

rom_link() {
    ln -s $1 %{buildroot}%{_datadir}/%{name}/$2
}

rom_link ../seabios/bios.bin bios.bin
rom_link ../seabios/acpi-dsdt.aml acpi-dsdt.aml
rom_link ../seabios/q35-acpi-dsdt.aml q35-acpi-dsdt.aml
rom_link ../sgabios/sgabios.bin sgabios.bin
%endif

%if 0%{?user:1}
mkdir -p %{buildroot}%{_exec_prefix}/lib/binfmt.d
for i in dummy \
%ifnarch %{ix86} x86_64
    qemu-i386 \
%endif
%ifnarch alpha
    qemu-alpha \
%endif
%ifnarch %{arm}
    qemu-arm \
%endif
    qemu-armeb \
    qemu-cris \
    qemu-microblaze qemu-microblazeel \
%ifnarch mips
    qemu-mips qemu-mips64 \
%endif
%ifnarch mipsel
    qemu-mipsel qemu-mips64el \
%endif
%ifnarch m68k
    qemu-m68k \
%endif
%ifnarch ppc ppc64
    qemu-ppc qemu-ppc64abi32 qemu-ppc64 \
%endif
%ifnarch sparc sparc64
    qemu-sparc qemu-sparc32plus qemu-sparc64 \
%endif
%ifnarch s390 s390x
    qemu-s390x \
%endif
%ifnarch sh4
    qemu-sh4 \
%endif
    qemu-sh4eb \
; do
  test $i = dummy && continue
  grep /$i:\$ %{SOURCE1} > %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i.conf
  chmod 644 %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i.conf
done < %{SOURCE1}
%endif

# For the qemu-guest-agent subpackage install the systemd
# service and udev rules.
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_udevdir}
install -m 0644 %{SOURCE10} %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE11} %{buildroot}%{_udevdir}

# Install rules to use the bridge helper with libvirt's virbr0
install -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/qemu
chmod u+s %{buildroot}%{_libexecdir}/qemu-bridge-helper

find %{buildroot} -name '*.la' -or -name '*.a' | xargs rm -f
find %{buildroot} -name "libcacard.so*" -exec chmod +x \{\} \;

rm -f %{buildroot}%{_bindir}/vscclient
rm -f %{buildroot}%{_libdir}/libcacard*
rm -f %{buildroot}%{_libdir}/pkgconfig/libcacard.pc
rm -rf %{buildroot}%{_includedir}/cacard

%check
make check

%ifarch %{kvm_archs}
%post %{kvm_package}
# load kvm modules now, so we can make sure no reboot is needed.
# If there's already a kvm module installed, we don't mess with it
sh %{_sysconfdir}/sysconfig/modules/kvm.modules &> /dev/null || :
udevadm trigger --subsystem-match=misc --sysname-match=kvm --action=add || :
%endif

%if %{with separate_kvm}
%post common
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu

%post -n ksm
%_post_service ksm.service
%_post_service ksmtuned.service
%preun -n ksm
%_preun_service ksm.service
%_preun_service ksmtuned.service
%endif

%if 0%{?user:1}
%post %{user}
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%postun %{user}
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%endif

%define kvm_files \
%if 0%{?need_kvm_modfile} \
%{_sysconfdir}/sysconfig/modules/kvm.modules \
%endif \
%{_udevdir}/80-kvm.rules

%if 0%{?need_qemu_kvm}
%define qemu_kvm_files \
%{_bindir}/qemu-kvm \
%{_mandir}/man1/qemu-kvm.1*
%endif

%files


%ifarch %{kvm_archs}
%files kvm

%endif

%files common
%dir %{qemudocdir}
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/README
%doc %{qemudocdir}/qemu-doc.html
%doc %{qemudocdir}/qemu-tech.html
%doc %{qemudocdir}/qmp-commands.txt
%doc %{qemudocdir}/COPYING
%doc %{qemudocdir}/COPYING.LIB
%doc %{qemudocdir}/LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/qemu-icon.bmp
%{_datadir}/%{name}/qemu_logo_no_text.svg
%{_datadir}/%{name}/keymaps/
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/virtfs-proxy-helper.1*
%{_bindir}/virtfs-proxy-helper
%{_libexecdir}/qemu-bridge-helper
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
%dir %{_sysconfdir}/qemu
%config(noreplace) %{_sysconfdir}/qemu/bridge.conf

%if %{with separate_kvm}
%files -n ksm
/lib/systemd/system/ksm.service
/lib/systemd/ksmctl
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
/lib/systemd/system/ksmtuned.service
%{_sbindir}/ksmtuned
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%endif

%if %{with separate_kvm}
%files guest-agent

%doc COPYING README
%{_bindir}/qemu-ga
%{_unitdir}/qemu-guest-agent.service
%{_udevdir}/99-qemu-guest-agent.rules
%endif

%if 0%{?user:1}
%files %{user}
%{_exec_prefix}/lib/binfmt.d/qemu-*.conf
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-mips64
%{_bindir}/qemu-mips64el
%{_bindir}/qemu-mipsn32
%{_bindir}/qemu-mipsn32el
%{_bindir}/qemu-or32
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64abi32
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-unicore32
%{_datadir}/systemtap/tapset/qemu-i386.stp
%{_datadir}/systemtap/tapset/qemu-x86_64.stp
%{_datadir}/systemtap/tapset/qemu-alpha.stp
%{_datadir}/systemtap/tapset/qemu-arm.stp
%{_datadir}/systemtap/tapset/qemu-armeb.stp
%{_datadir}/systemtap/tapset/qemu-cris.stp
%{_datadir}/systemtap/tapset/qemu-m68k.stp
%{_datadir}/systemtap/tapset/qemu-microblaze.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel.stp
%{_datadir}/systemtap/tapset/qemu-mips.stp
%{_datadir}/systemtap/tapset/qemu-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-mips64.stp
%{_datadir}/systemtap/tapset/qemu-mips64el.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el.stp
%{_datadir}/systemtap/tapset/qemu-or32.stp
%{_datadir}/systemtap/tapset/qemu-ppc.stp
%{_datadir}/systemtap/tapset/qemu-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-ppc64abi32.stp
%{_datadir}/systemtap/tapset/qemu-s390x.stp
%{_datadir}/systemtap/tapset/qemu-sh4.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb.stp
%{_datadir}/systemtap/tapset/qemu-sparc.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus.stp
%{_datadir}/systemtap/tapset/qemu-sparc64.stp
%{_datadir}/systemtap/tapset/qemu-unicore32.stp
%endif

%if 0%{?system_x86:1}
%files %{system_x86}
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_datadir}/systemtap/tapset/qemu-system-i386.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64.stp
%{_mandir}/man1/qemu-system-i386.1*
%{_mandir}/man1/qemu-system-x86_64.1*
%{_datadir}/%{name}/acpi-dsdt.aml
%{_datadir}/%{name}/q35-acpi-dsdt.aml
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/sgabios.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/kvmvapic.bin
%{_datadir}/%{name}/pxe-e1000.rom
%{_datadir}/%{name}/efi-e1000.rom
%{_datadir}/%{name}/pxe-virtio.rom
%{_datadir}/%{name}/efi-virtio.rom
%{_datadir}/%{name}/pxe-pcnet.rom
%{_datadir}/%{name}/efi-pcnet.rom
%{_datadir}/%{name}/pxe-rtl8139.rom
%{_datadir}/%{name}/efi-rtl8139.rom
%{_datadir}/%{name}/pxe-ne2k_pci.rom
%{_datadir}/%{name}/efi-ne2k_pci.rom
%config(noreplace) %{_sysconfdir}/qemu/target-x86_64.conf
%if %{with separate_kvm}
%ifarch %{ix86} x86_64
%{?kvm_files:}
%{?qemu_kvm_files:}
%endif
%endif
%endif

%ifarch %{kvm_archs}
%files kvm-tools
%{_bindir}/kvm_stat
%endif

%if 0%{?system_alpha:1}
%files %{system_alpha}
%{_bindir}/qemu-system-alpha
%{_datadir}/systemtap/tapset/qemu-system-alpha.stp
%{_mandir}/man1/qemu-system-alpha.1*
%{_datadir}/%{name}/palcode-clipper
%endif

%if 0%{?system_arm:1}
%files %{system_arm}
%{_bindir}/qemu-system-arm
%{_datadir}/systemtap/tapset/qemu-system-arm.stp
%{_mandir}/man1/qemu-system-arm.1*
%if %{with separate_kvm}
%ifarch armv7hl
%{?kvm_files:}
%{?qemu_kvm_files:}
%endif
%endif

%if 0%{?system_mips:1}
%files %{system_mips}
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%{_datadir}/systemtap/tapset/qemu-system-mips.stp
%{_datadir}/systemtap/tapset/qemu-system-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64el.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64.stp
%{_mandir}/man1/qemu-system-mips.1*
%{_mandir}/man1/qemu-system-mipsel.1*
%{_mandir}/man1/qemu-system-mips64el.1*
%{_mandir}/man1/qemu-system-mips64.1*
%endif

%if 0%{?system_cris:1}
%files %{system_cris}
%{_bindir}/qemu-system-cris
%{_datadir}/systemtap/tapset/qemu-system-cris.stp
%{_mandir}/man1/qemu-system-cris.1*
%endif

%if 0%{?system_lm32:1}
%files %{system_lm32}
%{_bindir}/qemu-system-lm32
%{_datadir}/systemtap/tapset/qemu-system-lm32.stp
%{_mandir}/man1/qemu-system-lm32.1*
%endif

%if 0%{?system_m68k:1}
%files %{system_m68k}
%{_bindir}/qemu-system-m68k
%{_datadir}/systemtap/tapset/qemu-system-m68k.stp
%{_mandir}/man1/qemu-system-m68k.1*
%endif

%if 0%{?system_microblaze:1}
%files %{system_microblaze}
%{_bindir}/qemu-system-microblaze
%{_bindir}/qemu-system-microblazeel
%{_datadir}/systemtap/tapset/qemu-system-microblaze.stp
%{_datadir}/systemtap/tapset/qemu-system-microblazeel.stp
%{_mandir}/man1/qemu-system-microblaze.1*
%{_mandir}/man1/qemu-system-microblazeel.1*
%{_datadir}/%{name}/petalogix*.dtb
%endif

%if 0%{?system_or32:1}
%files %{system_or32}
%{_bindir}/qemu-system-or32
%{_datadir}/systemtap/tapset/qemu-system-or32.stp
%{_mandir}/man1/qemu-system-or32.1*
%endif

%if 0%{?system_s390x:1}
%files %{system_s390x}
%{_bindir}/qemu-system-s390x
%{_datadir}/systemtap/tapset/qemu-system-s390x.stp
%{_mandir}/man1/qemu-system-s390x.1*
%{_datadir}/%{name}/s390-zipl.rom
%{_datadir}/%{name}/s390-ccw.img
%ifarch s390x
%{?kvm_files:}
%{?qemu_kvm_files:}
%endif
%endif

%if 0%{?system_sh4:1}
%files %{system_sh4}
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb
%{_datadir}/systemtap/tapset/qemu-system-sh4.stp
%{_datadir}/systemtap/tapset/qemu-system-sh4eb.stp
%{_mandir}/man1/qemu-system-sh4.1*
%{_mandir}/man1/qemu-system-sh4eb.1*
%endif

%if 0%{?system_sparc:1}
%files %{system_sparc}
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-sparc64
%{_datadir}/systemtap/tapset/qemu-system-sparc.stp
%{_datadir}/systemtap/tapset/qemu-system-sparc64.stp
%{_mandir}/man1/qemu-system-sparc.1*
%{_mandir}/man1/qemu-system-sparc64.1*
%endif

%if 0%{?system_ppc:1}
%files %{system_ppc}
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
%{_bindir}/qemu-system-ppcemb
%{_datadir}/systemtap/tapset/qemu-system-ppc.stp
%{_datadir}/systemtap/tapset/qemu-system-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-system-ppcemb.stp
%{_mandir}/man1/qemu-system-ppc.1*
%{_mandir}/man1/qemu-system-ppc64.1*
%{_mandir}/man1/qemu-system-ppcemb.1*
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/ppc_rom.bin
%{_datadir}/%{name}/spapr-rtas.bin
%ifarch ppc64
%{?kvm_files:}
%{?qemu_kvm_files:}
%endif
%endif
%endif

%if 0%{?system_unicore32:1}
%files %{system_unicore32}
%{_bindir}/qemu-system-unicore32
%{_datadir}/systemtap/tapset/qemu-system-unicore32.stp
%{_mandir}/man1/qemu-system-unicore32.1*
%endif

%if 0%{?system_xtensa:1}
%files %{system_xtensa}
%{_bindir}/qemu-system-xtensa
%{_bindir}/qemu-system-xtensaeb
%{_datadir}/systemtap/tapset/qemu-system-xtensa.stp
%{_datadir}/systemtap/tapset/qemu-system-xtensaeb.stp
%{_mandir}/man1/qemu-system-xtensa.1*
%{_mandir}/man1/qemu-system-xtensaeb.1*
%endif

%if 0%{?system_moxie:1}
%files %{system_moxie}
%{_bindir}/qemu-system-moxie
%{_datadir}/systemtap/tapset/qemu-system-moxie.stp
%{_mandir}/man1/qemu-system-moxie.1*
%endif

%if %{with separate_kvm}
%files img
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*
%endif

%files -n openbios
%{_datadir}/%{name}/openbios-*

%files -n SLOF
%{_datadir}/%{name}/slof.bin

%files -n seavgabios-bin
# Provided by package seavgabios
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/vgabios-stdvga.bin
%{_datadir}/%{name}/vgabios-vmware.bin
