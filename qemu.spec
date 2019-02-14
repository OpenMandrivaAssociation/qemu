%define _disable_lto 1
%define _disable_rebuild_configure 1
%define _disable_ld_no_undefined 1
%define sdlabi 2.0

%define qemu_version	3.1.0
%define qemu_snapshot	%{nil}
%define qemu_beta	%{nil}

%ifarch %{ix86} %{x86_64}
%bcond_without	firmwares # build firmwares from source
%endif

%bcond_with rbd                 # disabled
%bcond_without gtk              # enabled
%bcond_without usbredir         # enabled
%bcond_without xfsprogs         # enabled
%bcond_without spice            # enabled
%ifarch %{ix86} %{x86_64}
%bcond_without seccomp          # enabled
%else
%bcond_with seccomp             # disabled
%endif
# libfdt is only needed to build ARM, Microblaze or PPC emulators
%bcond_without fdt

Summary:	QEMU CPU Emulator
Name:		qemu
Version:	%{qemu_version}
%if "%{qemu_beta}" != ""
Release:	0.%{qemu_beta}.1
%else
Release:	%{?0qemu_snapshot:0.%{qemu_snapshot}.}2
%endif
License:	GPLv2+
Group:		Emulators
Url:		http://wiki.qemu.org/Main_Page
Source0:	http://wiki.qemu-project.org/download/%{name}-%{qemu_version}%{?qemu_snapshot:%{qemu_snapshot}}%{?qemu_beta:%{qemu_beta}}.tar.xz
Source3:	80-kvm.rules
# KSM control scripts
Source4:	ksm.service
Source5:	ksm.sysconfig
Source6:	ksmtuned.service
Source7:	ksmtuned
Source8:	ksmtuned.conf
Source9:	ksmctl.c
Source10:	qemu-guest-agent.service
Source11:	99-qemu-guest-agent.rules
Source12:	bridge.conf
Source13:	qemu.rpmlintrc
Patch0:		qemu-2.x.x-ld-gold.patch

BuildRequires:	gettext
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	libtool
BuildRequires:	rsync
BuildRequires:	texinfo
BuildRequires:	texi2html
BuildRequires:	alsa-oss-devel
BuildRequires:	attr-devel
BuildRequires:	cap-devel
BuildRequires:	glibc-static-devel
BuildRequires:	jpeg-devel
BuildRequires:	libaio-devel
BuildRequires:	rdmacm-devel
BuildRequires:	nss-devel
%ifnarch %{arm}
BuildRequires:	numa-devel
%endif
BuildRequires:	sasl-devel
BuildRequires:	snappy-devel
BuildRequires:	systemd
# We need both because the 'stap' binary is probed for by configure
BuildRequires:	systemtap
BuildRequires:	systemtap-devel
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(libcap-ng)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libiscsi)
BuildRequires:	pkgconfig(libnfs)
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libssh2)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(pixman-1)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(vdehist)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(epoxy)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libcacard)
%if %{with usbredir}
BuildRequires:	usbredir-devel >= 0.5.2
BuildRequires:	pkgconfig(libusbredirhost) >= 0.5.2
%endif
%if %{with spice}
BuildRequires:	pkgconfig(spice-server)
BuildRequires:	pkgconfig(spice-protocol)
%endif
%if %{with seccomp}
BuildRequires:	pkgconfig(libseccomp)
%endif
%if %{with rbd}
# For rbd block driver
BuildRequires: %{_lib}ceph-devel
%endif
# For XFS discard support in raw-posix.c
%if %{with xfsprogs}
BuildRequires:	xfsprogs-devel
%endif
%if %{with fdt}
# For FDT device tree support
BuildRequires:	fdt-devel
%endif
%ifnarch %armx
# xen
BuildRequires:	xen-devel
%endif
# For virtfs
%if %{with gtk}
# GTK frontend
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(vte-2.91)
%endif
# qemu statuc
BuildRequires:	pcre-static-devel
BuildRequires:	gpg-error-static-devel
BuildRequires:	pixman-static-devel
Provides:	kvm
Requires:	ipxe
Suggests:	qemu-img = %{version}-%{release}
Requires:	seabios
Requires:	sgabios
Requires:	vgabios

%description
QEMU is a FAST! processor emulator. By using dynamic translation it
achieves a reasonnable speed while being easy to port on new host
CPUs. QEMU has two operating modes:

* User mode emulation. In this mode, QEMU can launch Linux processes
  compiled for one CPU on another CPU. Linux system calls are
  converted because of endianness and 32/64 bit mismatches. Wine
  (Windows emulation) and DOSEMU (DOS emulation) are the main targets
  for QEMU.

* Full system emulation. In this mode, QEMU emulates a full system,
  including a processor and various peripherials. Currently, it is
  only used to launch an x86 Linux kernel on an x86 Linux system. It
  enables easier testing and debugging of system code. It can also be
  used to provide virtual hosting of several virtual PC on a single
  server.

%package	img
Summary:	QEMU disk image utility
Group:		Emulators

%description	img
This package contains the QEMU disk image utility that is used to
create, commit, convert and get information from a disk image.

%package -n	seabios
Summary:        X86 BIOS for QEMU
Group:          Emulators
BuildArch:      noarch

%package -n ivshmem-tools
Summary: Client and server for QEMU ivshmem device
Group: Development/Tools

%description -n ivshmem-tools
This package provides client and server tools for QEMU's ivshmem device.


%description -n	seabios
SeaBIOS is an open source implementation of a 16bit x86 BIOS. SeaBIOS
is the default BIOS for QEMU.

%package -n	ipxe
Summary:        PXE ROMs for QEMU NICs
Group:          Emulators
BuildArch:      noarch
Conflicts:      qemu < 1.6.0

%description -n	ipxe
Preboot Execution Environment (PXE) ROM support for various emulated network
adapters available with QEMU.

%package -n	vgabios
Summary:        VGA BIOSes for QEMU
Group:          Emulators
BuildArch:      noarch

%description -n	vgabios
VGABIOS provides the video ROM BIOSes for the following variants of VGA
emulated devices: Std VGA, QXL, Cirrus CLGD 5446 and VMware emulated
video card.

%package -n	sgabios
Summary:        Serial Graphics Adapter BIOS for QEMU
Group:          Emulators
BuildArch:      noarch

%description -n	sgabios
The Google Serial Graphics Adapter BIOS or SGABIOS provides a means for legacy
x86 software to communicate with an attached serial console as if a video card
were attached.

%package	linux-user
Summary:        Serial Graphics Adapter BIOS for QEMU
Group:          Emulators

%description	linux-user
QEMU is an extremely well-performing CPU emulator that allows you to
choose between simulating an entire system and running userspace
binaries for different architectures under your native operating
system. It currently emulates x86, ARM, PowerPC and SPARC CPUs as well
as PC and PowerMac systems.

This sub-package contains statically linked binaries for running linux-user
emulations. This can be used together with the OBS build script to
run cross-architecture builds.

%package	guest-agent
Summary:        Universal CPU emulator -- Guest agent
Group:          Emulators
Provides:       qemu:%{_bindir}/qemu-ga

%description guest-agent
QEMU is an extremely well-performing CPU emulator that allows you to
choose between simulating an entire system and running userspace
binaries for different architectures under your native operating
system. It currently emulates x86, ARM, PowerPC and SPARC CPUs as well
as PC and PowerMac systems.

This sub-package contains the guest agent.

%package	static-aarch64
Summary:	Static build of qemu aarch64 user mode
Group:		Emulators

%description	static-aarch64
This package contains a static build of the user mode aarch64 qemu emulator,
which allows you to run aarch64 binaries in your host environment without any
need for a dedicated virtual machine.

The static nature of this build makes it usable for doing aarch64 emulation in
guest environment, ie. a chroot.

%package	static-arm
Summary:	Static build of qemu arm user mode
Group:		Emulators

%description	static-arm
This package contains a static build of the user mode arm qemu emulator,
which allows you to run arm binaries in your host environment without any
need for a dedicated virtual machine.

The static nature of this build makes it usable for doing arm emulation in
guest environment, ie. a chroot.

%package	static-mips
Summary:	Static build of qemu mips user mode
Group:		Emulators

%description	static-mips
This package contains a static build of the user mode mips qemu emulator,
which allows you to run mips binaries in your host environment without any
need for a dedicated virtual machine.

The static nature of this build makes it usable for doing mips emulation in
guest environment, ie. a chroot.

%package	static-mipsel
Summary:	Static build of qemu mipsel user mode
Group:		Emulators

%description	static-mipsel
This package contains a static build of the user mode mipsel qemu emulator,
which allows you to run mipsel binaries in your host environment without any
need for a dedicated virtual machine.

The static nature of this build makes it usable for doing mipsel emulation in
guest environment, ie. a chroot.

%package	static-x86_64
Summary:	Static build of qemu x86_64 user mode
Group:		Emulators

%description	static-x86_64
This package contains a static build of the user mode x86_64 qemu emulator,
which allows you to run mipsel binaries in your host environment without any
need for a dedicated virtual machine.

The static nature of this build makes it usable for doing x86_64 emulation in
guest environment, ie. a chroot.

%package	static-i386
Summary:	Static build of qemu i386 user mode
Group:		Emulators

%description	static-i386
This package contains a static build of the user mode i386 qemu emulator,
which allows you to run mipsel binaries in your host environment without any
need for a dedicated virtual machine.

The static nature of this build makes it usable for doing i386 emulation in
guest environment, ie. a chroot.

%package	static-ppc
Summary:	Static build of qemu ppc user mode
Group:		Emulators

%description	static-ppc
This package contains a static build of the user mode ppc qemu emulator,
which allows you to run mipsel binaries in your host environment without any
need for a dedicated virtual machine.

The static nature of this build makes it usable for doing ppc emulation in
guest environment, ie. a chroot.

%package	static-ppc64
Summary:	Static build of qemu ppc64 user mode
Group:		Emulators

%description	static-ppc64
This package contains a static build of the user mode ppc64 qemu emulator,
which allows you to run mipsel binaries in your host environment without any
need for a dedicated virtual machine.

The static nature of this build makes it usable for doing ppc64 emulation in
guest environment, ie. a chroot.

%package	static-riscv32
Summary:	Static build of qemu riscv32 user mode
Group:		Emulators

%description	static-riscv32
This package contains a static build of the user mode riscv32 qemu emulator,
which allows you to run mipsel binaries in your host environment without any
need for a dedicated virtual machine.

The static nature of this build makes it usable for doing riscv64 emulation in
guest environment, ie. a chroot.

%package	static-riscv64
Summary:	Static build of qemu riscv64 user mode
Group:		Emulators

%description	static-riscv64
This package contains a static build of the user mode riscv64 qemu emulator,
which allows you to run mipsel binaries in your host environment without any
need for a dedicated virtual machine.

The static nature of this build makes it usable for doing riscv64 emulation in
guest environment, ie. a chroot.

%package	static-sparc
Summary:	Static build of qemu sparc user mode
Group:		Emulators

%description	static-sparc
This package contains a static build of the user mode sparc qemu emulator,
which allows you to run mipsel binaries in your host environment without any
need for a dedicated virtual machine.

The static nature of this build makes it usable for doing sparc emulation in
guest environment, ie. a chroot.

%package	static-sparc64
Summary:	Static build of qemu sparc64 user mode
Group:		Emulators

%description	static-sparc64
This package contains a static build of the user mode sparc64 qemu emulator,
which allows you to run mipsel binaries in your host environment without any
need for a dedicated virtual machine.

The static nature of this build makes it usable for doing sparc64 emulation in
guest environment, ie. a chroot.

%prep
%setup -q -n %{name}-%{qemu_version}%{?qemu_snapshot:%{qemu_snapshot}}%{?qemu_beta:%{qemu_beta}}
%apply_patches
sed -i 's!MAX_ARG_PAGES 33!MAX_ARG_PAGES 64!g' linux-user/qemu.h

%build
%setup_compile_flags
export CC=gcc
export CXX=g++
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

# (tpg) list of targets
%define _target_list aarch64-linux-user,arm-linux-user,mips-linux-user,mipsel-linux-user,i386-linux-user,x86_64-linux-user,sparc-linux-user,sparc64-linux-user,ppc-linux-user,ppc64-linux-user,riscv32-linux-user,riscv64-linux-user

mkdir -p qemu-static
pushd qemu-static
../configure	--python=%{__python} \
		--target-list=%{_target_list} \
		--disable-tools \
		--disable-linux-aio \
		--disable-tcg-interpreter \
		--disable-debug-tcg \
		--disable-debug-info \
		--disable-sparse \
		--disable-strip \
		--disable-werror \
		--disable-stack-protector \
		--disable-sdl \
		--disable-gtk \
		--disable-virtfs \
		--disable-vnc \
		--disable-cocoa \
		--disable-xen \
		--disable-xen-pci-passthrough \
		--disable-brlapi \
		--disable-vnc-sasl \
		--disable-vnc-jpeg \
		--disable-vnc-png \
		--disable-curses \
		--disable-curl \
		--disable-fdt \
		--disable-bluez \
		--disable-slirp \
		--disable-rdma \
		--disable-system \
		--disable-bsd-user \
		--disable-vde \
		--disable-netmap \
		--disable-cap-ng \
		--disable-attr \
		--disable-blobs \
		--disable-docs \
		--disable-vhost-net \
		--disable-spice \
		--disable-libiscsi \
		--disable-libnfs \
		--disable-libusb \
		--disable-usb-redir \
		--disable-guest-agent \
		--disable-seccomp \
		--with-coroutine=ucontext \
		--enable-coroutine-pool \
		--disable-glusterfs \
		--disable-tpm \
		--disable-libssh2 \
		--disable-numa \
		--disable-lzo \
		--disable-rbd \
%ifarch %{ix86} %{x86_64}
		--enable-membarrier \
%endif
		--static \
		--enable-kvm \
		--extra-ldflags="%ldflags -static -Wl,-z,relro -Wl,-z,now" \
		--extra-cflags="%{optflags}"

%make V=1 $buildldflags
popd

dobuild() {
    ../configure \
	--enable-system \
	--enable-user \
	--enable-linux-user \
	--enable-tools \
	--enable-opengl \
	--enable-libusb \
	--enable-gnutls \
	--python=%{__python} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir} \
	--audio-drv-list=pa,sdl,alsa,oss \
	--localstatedir=%{_localstatedir} \
	--libexecdir=%{_libexecdir} \
	--disable-strip \
	--extra-ldflags="%{ldflags} $extraldflags" \
	--extra-cflags="%{optflags}" \
	--enable-trace-backend=dtrace \
	--disable-werror \
	--enable-kvm \
	--enable-tcg-interpreter \
	--enable-tpm \
%ifarch %{ix86} %{x86_64}
	--enable-xen \
	--enable-xen-pci-passthrough \
%else
	--disable-xen \
%endif
%if %{with spice}
	--enable-spice \
%endif
%if %{with seccomp}
	--enable-seccomp \
%endif
%if %{with rbd}
	--enable-rbd \
%else
	--disable-rbd \
%endif
%if %{with fdt}
	--enable-fdt \
%else
	--disable-fdt \
%endif
	--enable-sdl \
	--with-sdlabi="%{sdlabi}" \
	--enable-curses \
	--enable-vnc \
	--enable-vnc-sasl \
	--enable-vnc-jpeg \
	--enable-vnc-png \
	--enable-curl \
%ifarch %{ix86} %{x86_64}
	--enable-membarrier \
%endif
	--enable-fdt \
	--enable-linux-aio \
	--enable-cap-ng \
	--enable-attr \
%if %{with usbredir}
	--enable-usb-redir \
%else
	--disable-usb-redir \
%endif
	--enable-snappy \
	--enable-libnfs \
	--enable-guest-agent \
	--enable-modules \
%ifnarch %{arm}
	--enable-numa \
%endif
        "$@"

    echo "config-host.mak contents:"
    echo "==="
    cat config-host.mak
    echo "==="

    %make V=1 $buildldflags
}

mkdir -p system
pushd system
dobuild
%{__cc} %{SOURCE9} -O2 -g -o ksmctl
popd

%install
install -D -p -m 0644 %{SOURCE4} %{buildroot}%{_unitdir}/ksm.service
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 system/ksmctl %{buildroot}/lib/systemd/ksmctl

install -D -p -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/ksmtuned.service
install -D -p -m 0755 %{SOURCE7} %{buildroot}%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE8} %{buildroot}%{_sysconfdir}/ksmtuned.conf

install -D -p -m 0644 %{SOURCE10} %{buildroot}%{_unitdir}/qemu-guest-agent.service

mkdir -p %{buildroot}%{_udevrulesdir}
install -D -p -m 0644 %{SOURCE11} %{buildroot}%{_udevrulesdir}
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_udevrulesdir}

# Install rules to use the bridge helper with libvirt's virbr0
mkdir -p %{buildroot}%{_sysconfdir}/qemu/
install -D -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/qemu/

%ifarch %{ix86} %{x86_64} %{arm}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/modules
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/%{name}
%endif

%makeinstall_std -C system BUILD_DOCS="yes"

install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

install -d -m 755 %{buildroot}%{_sbindir}
install -m 755 scripts/qemu-binfmt-conf.sh %{buildroot}%{_sbindir}
%ifnarch %ix86 %{x86_64}
ln -sf ../../../emul/ia32-linux %{buildroot}/usr/share/qemu/qemu-i386
%endif
%ifnarch ia64
mkdir -p %{buildroot}/emul/ia32-linux
%endif
rm -rf %{buildroot}%{_datadir}/%{name}/QEMU,tcx.bin

install -d %{buildroot}%{_binfmtdir}
magic_aarch64='\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\xb7:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff'
magic_arm='\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x28\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff'
magic_mips='\x7fELF\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x08:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff'
magic_mipsel='\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x08\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff'
magic_i386='\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x03\x00:\xff\xff\xff\xff\xff\xfe\xfe\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff'
magic_i486='\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x03\x00:\xff\xff\xff\xff\xff\xfe\xfe\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff'
magic_x86_64='\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x3e\x00:\xff\xff\xff\xff\xff\xfe\xfe\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff'
magic_ppc='\x7fELF\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x14:\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff'
magic_ppc64='\x7fELF\x02\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x15:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff'
magic_sparc='\x7fELF\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x02:\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff'
magic_sparc64='\x7fELF\x02\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x2b:\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff'
magic_riscv64='\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\xf3\x00:\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff'

# We don't currently build the qemu binaries for the following
# architectures, but let's keep the magic values here just in case...
magic_alpha='\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x26\x90:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff'
magic_armeb='\x7fELF\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x28:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff'
magic_cris='\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x4c\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff'
magic_m68k='\x7fELF\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x04:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff'
magic_microblaze='\x7fELF\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xba\xab:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff'
magic_s390x='\x7fELF\x02\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x16:\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff'
magic_ppc64abi32='\x7fELF\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x15:\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff'
magic_sh4='\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x2a\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff'
magic_sh4eb='\x7fELF\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x2a:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff'
magic_sparc32plus='\x7fELF\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x12:\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff'

for i in aarch64 arm mips mipsel i386 x86_64 ppc ppc64 sparc sparc64 riscv32 riscv64; do
	install -m755 qemu-static/$i-linux-user/qemu-$i -D %{buildroot}%{_bindir}/qemu-static-$i
	echo ":$i:M::$(eval echo \$magic_$i):%{_bindir}/qemu-static-$i:" >%{buildroot}%{_binfmtdir}/qemu-$i.conf
done
# Some subtypes that have different magic values but same qemu binaries...
echo ":i486:M::$magic_i486:%{_bindir}/qemu-static-i386:" >%{buildroot}%{_binfmtdir}/qemu-i486.conf

# Registering a binfmt handler for our own arch is a really really bad idea...
%ifarch aarch64
rm -f %{buildroot}%{_binfmtdir}/qemu-aarch64.conf
%endif
%ifarch %{armx} aarch64
rm -f %{buildroot}%{_binfmtdir}/qemu-arm.conf
%endif
%ifarch %{x86_64}
rm -f %{buildroot}%{_binfmtdir}/qemu-x86_64.conf
%endif
%ifarch %{ix86} %{x86_64}
rm -f %{buildroot}%{_binfmtdir}/qemu-i?86.conf
%endif
%ifarch mips
rm -f %{buildroot}%{_binfmtdir}/qemu-mips.conf
%endif
%ifarch mipsel
rm -f %{buildroot}%{_binfmtdir}/qemu-mipsel.conf
%endif
%ifarch sparc sparc64
rm -f %{buildroot}%{_binfmtdir}/qemu-sparc.conf
%endif
%ifarch sparc64
rm -f %{buildroot}%{_binfmtdir}/qemu-sparc64.conf
%endif
%ifarch ppc ppc64
rm -f %{buildroot}%{_binfmtdir}/qemu-ppc.conf
%endif
%ifarch ppc64
rm -f %{buildroot}%{_binfmtdir}/qemu-ppc64.conf
%endif
%ifarch riscv32 riscv64
rm -f %{buildroot}%{_binfmtdir}/qemu-riscv*.conf
%endif


%find_lang %{name}

%files -f %{name}.lang
%doc README system/qemu-doc.html
%config(noreplace)%{_sysconfdir}/sasl2/qemu.conf
%{_unitdir}/ksm.service
/lib/systemd/ksmctl
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%{_udevrulesdir}/80-kvm.rules
%{_unitdir}/ksmtuned.service
%{_sbindir}/ksmtuned
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%config(noreplace) %{_sysconfdir}/qemu/bridge.conf
%{_bindir}/qemu-system-*
%{_bindir}/qemu-pr-helper
%{_bindir}/qemu-keymap
%{_bindir}/qemu-edid
%{_bindir}/virtfs-proxy-helper
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/virtfs-proxy-helper.*
%{_mandir}/man7/qemu-cpu-models.7*
%dir %{_datadir}/qemu
%{_datadir}/qemu/keymaps
%{_datadir}/qemu/trace-events-all
%{_datadir}/qemu/openbios-sparc32
%{_datadir}/qemu/openbios-sparc64
%{_datadir}/qemu/openbios-ppc
%{_datadir}/qemu/vgabios-bochs-display.bin
%{_datadir}/qemu/vgabios-ramfb.bin
%{_datadir}/qemu/*.dtb
%{_datadir}/qemu/qemu-icon.bmp
%{_libexecdir}/qemu-bridge-helper
%{_datadir}/qemu/*.svg
%{_datadir}/systemtap/tapset/*
%{_datadir}/%{name}/efi-rtl8139.rom
%{_datadir}/%{name}/efi-ne2k_pci.rom
%{_datadir}/%{name}/efi-pcnet.rom
%{_datadir}/%{name}/efi-e1000*.rom
%{_datadir}/%{name}/efi-vmx*.rom
%{_datadir}/%{name}/efi-virtio.rom
%{_datadir}/%{name}/efi-eepro100.rom
%{_datadir}/%{name}/kvmvapic.bin
%{_datadir}/%{name}/linuxboot*.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/QEMU,cgthree.bin
%{_datadir}/%{name}/bios-256k.bin
%{_datadir}/%{name}/u-boot.e500
%{_datadir}/%{name}/skiboot.lid
%{_datadir}/%{name}/qemu_vga.ndrv
%{_datadir}/%{name}/s390-netboot.img
%dir %{_libdir}/qemu
%{_libdir}/qemu/block-curl.so
%{_libdir}/qemu/block-iscsi.so
%if %{with rbd}
%{_libdir}/qemu/block-rbd.so
%endif
%{_libdir}/qemu/block-ssh.so
%{_libdir}/qemu/block-dmg-bz2.so
%{_libdir}/qemu/block-nfs.so
%{_libdir}/qemu/ui-sdl.so
%{_libdir}/qemu/ui-gtk.so
%{_libdir}/qemu/ui-curses.so
%{_libdir}/qemu/audio*.so



%files linux-user
%{_datadir}/%{name}/ppc_rom.bin
%{_datadir}/%{name}/spapr-rtas.bin
%{_datadir}/%{name}/slof.bin
%{_datadir}/%{name}/palcode-clipper
%{_datadir}/%{name}/s390-ccw.img
%{_datadir}/%{name}/u-boot-sam460-20100605.bin
%{_datadir}/%{name}/hppa-firmware.img
%{_bindir}/qemu-aarch64
%{_bindir}/qemu-riscv*
%{_bindir}/qemu-xtensa*
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-aarch64_be
%{_bindir}/qemu-i386
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-mipsn32
%{_bindir}/qemu-mipsn32el
%{_bindir}/qemu-mips64
%{_bindir}/qemu-mips64el
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64abi32
%{_bindir}/qemu-ppc64le
%{_bindir}/qemu-riscv32
%{_bindir}/qemu-riscv64
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-sparc
%{_bindir}/qemu-tilegx
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-hppa
%{_bindir}/qemu-nios2
%{_bindir}/qemu-or1k
%{_sbindir}/qemu-binfmt-conf.sh
%ifnarch %ix86 %{x86_64} ia64
%dir /emul/ia32-linux
%endif
%ifnarch %ix86 %{x86_64}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/qemu-i386
%endif

%files img
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_mandir}/man8/qemu-nbd.8*
%{_mandir}/man1/qemu-img.1*

%files -n ivshmem-tools
%{_bindir}/ivshmem-client
%{_bindir}/ivshmem-server

%files -n seabios
%{_datadir}/%{name}/bios.bin

%files -n vgabios
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/vgabios-stdvga.bin
%{_datadir}/%{name}/vgabios-vmware.bin
%{_datadir}/%{name}/vgabios-virtio.bin

%files -n sgabios
%{_datadir}/%{name}/sgabios.bin

%files -n ipxe
%{_datadir}/%{name}/pxe-e1000.rom
%{_datadir}/%{name}/pxe-eepro100.rom
%{_datadir}/%{name}/pxe-pcnet.rom
%{_datadir}/%{name}/pxe-ne2k_pci.rom
%{_datadir}/%{name}/pxe-rtl8139.rom
%{_datadir}/%{name}/pxe-virtio.rom

%files guest-agent
%{_bindir}/qemu-ga
%{_mandir}/man8/qemu-ga*8*
%{_mandir}/man7/qemu-qmp*.7*
%{_mandir}/man7/qemu-block*.7*
%{_mandir}/man7/qemu-ga-ref*.7*
%{_unitdir}/qemu-guest-agent.service
%{_udevrulesdir}/99-qemu-guest-agent.rules

%files -n qemu-static-aarch64
%{_bindir}/qemu-static-aarch64
%ifnarch aarch64
%{_binfmtdir}/qemu-aarch64.conf

%post -n qemu-static-aarch64
%{_bindir}/systemctl restart systemd-binfmt
%endif

%files -n qemu-static-arm
%{_bindir}/qemu-static-arm
%ifnarch %{arm} %{armx} aarch64
%{_binfmtdir}/qemu-arm.conf

%post -n qemu-static-arm
%{_bindir}/systemctl restart systemd-binfmt
%endif

%files -n qemu-static-mips
%{_bindir}/qemu-static-mips
%ifnarch mips
%{_binfmtdir}/qemu-mips.conf

%post -n qemu-static-mips
%{_bindir}/systemctl restart systemd-binfmt
%endif

%files -n qemu-static-mipsel
%{_bindir}/qemu-static-mipsel
%ifnarch mipsel
%{_binfmtdir}/qemu-mipsel.conf

%post -n qemu-static-mipsel
%{_bindir}/systemctl restart systemd-binfmt
%endif

%files -n qemu-static-x86_64
%{_bindir}/qemu-static-x86_64
%ifnarch %{x86_64}
%{_binfmtdir}/qemu-x86_64.conf

%post -n qemu-static-x86_64
%{_bindir}/systemctl restart systemd-binfmt
%endif

%files -n qemu-static-i386
%{_bindir}/qemu-static-i386
%ifnarch %{ix86} %{x86_64}
%{_binfmtdir}/qemu-i?86.conf

%post -n qemu-static-i386
%{_bindir}/systemctl restart systemd-binfmt
%endif

%files -n qemu-static-ppc
%{_bindir}/qemu-static-ppc
%ifnarch ppc ppc64
%{_binfmtdir}/qemu-ppc.conf

%post -n qemu-static-ppc
%{_bindir}/systemctl restart systemd-binfmt
%endif

%files -n qemu-static-ppc64
%{_bindir}/qemu-static-ppc64
%ifnarch ppc64
%{_binfmtdir}/qemu-ppc64.conf

%post -n qemu-static-ppc64
%{_bindir}/systemctl restart systemd-binfmt
%endif

%files -n qemu-static-riscv32
%{_bindir}/qemu-static-riscv32
%ifnarch riscv32 riscv64
%{_binfmtdir}/qemu-riscv32.conf

%post -n qemu-static-riscv32
%{_bindir}/systemctl restart systemd-binfmt
%endif

%files -n qemu-static-riscv64
%{_bindir}/qemu-static-riscv64
%ifnarch riscv32 riscv64
%{_binfmtdir}/qemu-riscv64.conf

%post -n qemu-static-riscv64
%{_bindir}/systemctl restart systemd-binfmt
%endif

%files -n qemu-static-sparc
%{_bindir}/qemu-static-sparc
%ifnarch sparc sparc64
%{_binfmtdir}/qemu-sparc.conf

%post -n qemu-static-sparc
%{_bindir}/systemctl restart systemd-binfmt
%endif

%files -n qemu-static-sparc64
%{_bindir}/qemu-static-sparc64
%ifnarch sparc64
%{_binfmtdir}/qemu-sparc64.conf

%post -n qemu-static-sparc64
%{_bindir}/systemctl restart systemd-binfmt
%endif
