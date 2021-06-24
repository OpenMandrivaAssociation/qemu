%define _disable_lto 1
%define _disable_rebuild_configure 1
%define _disable_ld_no_undefined 1

%ifarch %{ix86}
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch %{x86_64}
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch %{power64}
%global kvm_package   system-ppc
%endif
%ifarch s390x
%global kvm_package   system-s390x
%endif
%ifarch %{arm}
%global kvm_package   system-arm
%endif
%ifarch aarch64
%global kvm_package   system-aarch64
%endif
%ifarch %{mips}
%global kvm_package   system-mips
%endif

%global user_static 1

%global have_kvm 0
%if 0%{?kvm_package:1}
%global have_kvm 1
%endif

# Matches numactl ExcludeArch
%global have_numactl 1
%ifarch s390 %{arm}
%global have_numactl 0
%endif

# Upstream disables iasl for big endian and QEMU checks
# for this. Fedora has re-enabled it on BE circumventing
# the QEMU checks, but it fails none the less:
#
# https://bugzilla.redhat.com/show_bug.cgi?id=1332449
%global have_iasl 1
%ifnarch s390 s390x ppc ppc64
%global have_iasl 0
%endif

%ifarch %{ix86} %{x86_64} %{armx}
%global have_spice 1
%else
# Matches spice ExclusiveArch
%global have_spice 0
%endif

# Matches xen ExclusiveArch
%global have_xen 0

%bcond_with rbd                 # disabled
%bcond_without gtk              # enabled
%bcond_without usbredir         # enabled
%bcond_without spice            # enabled
%bcond_without seccomp          # enabled

%ifarch %{ix86} %{x86_64} %{armx}
%global have_edk2 0
%endif

# If we can run qemu-sanity-check, hostqemu gets defined.
%ifarch %{arm}
%global hostqemu arm-softmmu/qemu-system-arm
%endif
%ifarch aarch64
%global hostqemu arm-softmmu/qemu-system-aarch64
%endif
%ifarch %{ix86}
%global hostqemu i386-softmmu/qemu-system-i386
%endif
%ifarch %{x86_64}
%global hostqemu x86_64-softmmu/qemu-system-x86_64
%endif

# All modules should be listed here.
%ifarch %{ix86} %{arm}
%define with_block_rbd 0
%else
%define with_block_rbd 0
%endif
# not in main yet
%global with_block_gluster 0

%define EVRD %{epoch}:%{version}-%{release}

%define requires_block_curl Requires: %{name}-block-curl = %{EVRD}
%define requires_block_dmg Requires: %{name}-block-dmg = %{EVRD}
%if %{with_block_gluster}
%define requires_block_gluster Requires: %{name}-block-gluster = %{EVRD}
%define obsoletes_block_gluster %{nil}
%else
%define requires_block_gluster %{nil}
%define obsoletes_block_gluster Obsoletes: %{name}-block-gluster < %{EVRD}
%endif
%define requires_block_iscsi Requires: %{name}-block-iscsi = %{EVRD}
%define requires_block_nfs Requires: %{name}-block-nfs = %{EVRD}
%if %{with_block_rbd}
%define requires_block_rbd Requires: %{name}-block-rbd = %{EVRD}
%define obsoletes_block_rbd %{nil}
%else
%define requires_block_rbd %{nil}
%define obsoletes_block_rbd Obsoletes: %{name}-block-rbd < %{EVRD}
%endif
%define requires_block_ssh Requires: %{name}-block-ssh = %{EVRD}
%define requires_audio_alsa Requires: %{name}-audio-alsa = %{EVRD}
%define requires_audio_oss Requires: %{name}-audio-oss = %{EVRD}
%define requires_audio_pa Requires: %{name}-audio-pa = %{EVRD}
%define requires_audio_sdl Requires: %{name}-audio-sdl = %{EVRD}
%define requires_ui_curses Requires: %{name}-ui-curses = %{EVRD}
%define requires_ui_gtk Requires: %{name}-ui-gtk = %{EVRD}
%define requires_ui_sdl Requires: %{name}-ui-sdl = %{EVRD}
%define requires_ui_egl_headless Requires: %{name}-ui-egl-headless = %{EVRD}
%define requires_ui_opengl Requires: %{name}-ui-opengl = %{EVRD}
%define requires_device_display_virtio_gpu Requires: %{name}-device-display-virtio-gpu = %{EVRD}
%define requires_device_display_virtio_gpu_pci Requires: %{name}-device-display-virtio-gpu-pci = %{EVRD}
%define requires_device_display_virtio_vga Requires: %{name}-device-display-virtio-vga = %{EVRD}
%if %{have_spice}
%define requires_ui_spice_app Requires: %{name}-ui-spice-app = %{EVRD}
%define requires_ui_spice_core Requires: %{name}-ui-spice-core = %{EVRD}
%define requires_device_display_qxl Requires: %{name}-device-display-qxl = %{EVRD}
%define requires_audio_spice Requires: %{name}-audio-spice = %{EVRD}
%define requires_char_spice Requires: %{name}-char-spice = %{EVRD}
%else
%define requires_ui_spice_app %{nil}
%define requires_ui_spice_core %{nil}
%define requires_device_display_qxl %{nil}
%define requires_audio_spice %{nil}
%define requires_char_spice %{nil}
%endif

%global requires_all_modules \
%{requires_block_curl} \
%{requires_block_dmg} \
%{requires_block_gluster} \
%{requires_block_iscsi} \
%{requires_block_nfs} \
%{requires_block_rbd} \
%{requires_block_ssh} \
%{requires_audio_alsa} \
%{requires_audio_oss} \
%{requires_audio_pa} \
%{requires_audio_sdl} \
%{requires_ui_egl_headless} \
%{requires_ui_opengl} \
%{requires_device_display_virtio_gpu} \
%{requires_device_display_virtio_gpu_pci} \
%{requires_device_display_virtio_vga} \
%{requires_ui_curses} \
%{requires_ui_gtk} \
%{requires_ui_sdl} \
%{requires_ui_spice_app} \
%{requires_ui_spice_core} \
%{requires_char_spice} \
%{requires_device_display_qxl}

# Modules which can be conditionally built
%global obsoletes_some_modules \
%{obsoletes_block_gluster} \
%{obsoletes_block_rbd}

%define beta rc3

Summary:	QEMU is a FAST! processor emulator
Name:		qemu
Version:	6.0.0
Release:	%{?beta:0.%{beta}.}2
Group:		Emulators
Epoch:		3
License:	GPLv2 and BSD and MIT and CC-BY
URL:		http://www.qemu.org/

Source0: https://download.qemu.org/%{name}-%{version}%{?beta:-%{beta}}.tar.xz
Source1: qemu.rpmlintrc

# guest agent service
Source10: qemu-guest-agent.service
Source17: qemu-ga.sysconfig
# guest agent udev rules
Source11: 99-qemu-guest-agent.rules
# /etc/qemu/bridge.conf
Source12: bridge.conf
# qemu-kvm back compat wrapper installed as /usr/bin/qemu-kvm
Source13: qemu-kvm.sh
# PR manager service
Source14: qemu-pr-helper.service
Source15: qemu-pr-helper.socket
# /etc/modprobe.d/kvm.conf, for x86
Source20: kvm-x86.modprobe.conf
# /etc/security/limits.d/95-kvm-ppc64-memlock.conf
Source21: 95-kvm-ppc64-memlock.conf

BuildRequires: %mklibname zstd -s -d
BuildRequires: meson
# documentation deps
BuildRequires: texinfo
BuildRequires: capstone-devel
# For /usr/bin/pod2man
#BuildRequires: perl-podlators
# For sanity test
# BuildRequires: qemu-sanity-check-nodeps
%if %{have_iasl}
# For acpi compilation
BuildRequires: iasl
%endif
# For chrpath calls in specfile
BuildRequires:	chrpath
BuildRequires:	pkgconfig(libibverbs)

# -display sdl support
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(SDL2_image)
BuildRequires:	pkgconfig(libzstd)
# used in various places for compression
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(vdeplug)
BuildRequires:	xfsprogs-devel

# used in various places for crypto
BuildRequires:	gnutls-devel
# VNC sasl auth support
BuildRequires:	sasl-devel
# aio implementation for block drivers
BuildRequires:	libaio-devel
# pulseaudio audio output
BuildRequires:	pkgconfig(libpulse)
# alsa audio output
BuildRequires:	alsa-oss-devel
BuildRequires:	pkgconfig(alsa)
# qemu-pr-helper multipath support (requires libudev too)
BuildRequires:	device-mapper-multipath-devel
BuildRequires:	systemd
# iscsi drive support
BuildRequires:	pkgconfig(libiscsi)
# NFS drive support
BuildRequires:	pkgconfig(libnfs)
# snappy compression for memory dump
BuildRequires:	snappy-devel
# lzo compression for memory dump
BuildRequires:	pkgconfig(lzo2)
# needed for -display curses
BuildRequires:	pkgconfig(ncurses)
# used by 9pfs
BuildRequires:  attr-devel
BuildRequires:  cap-devel
# used by qemu-bridge-helper and qemu-pr-helper
BuildRequires:	pkgconfig(libcap-ng)
# spice usb redirection support
%if %{with usbredir}
BuildRequires:	usbredir-devel >= 0.5.2
BuildRequires:	pkgconfig(libusbredirhost) >= 0.5.2
%endif
%if %{have_spice}
# spice graphics support
BuildRequires:	pkgconfig(spice-server)
BuildRequires:	pkgconfig(spice-protocol)
%endif
%if %{with seccomp}
# seccomp containment support
BuildRequires: pkgconfig(libseccomp) >= 2.3.0
%endif
# For network block driver
BuildRequires: pkgconfig(libcurl)
%if %{with_block_rbd}
# For rbd block driver
BuildRequires: ceph-devel
%endif
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
BuildRequires: systemtap-devel
# For VNC JPEG support
BuildRequires: jpeg-devel
# For VNC PNG support
BuildRequires: pkgconfig(libpng)
# For BlueZ device support
BuildRequires: pkgconfig(bluez)
# For Braille device support
#BuildRequires: brlapi-devel
%if %{with fdt}
# For FDT device tree support
BuildRequires:	fdt-devel
%endif
# Hard requirement for version >= 1.3
BuildRequires:	pkgconfig(pixman-1)
%if %{with_block_gluster}
# For gluster support
BuildRequires: glusterfs-devel >= 3.4.0
%endif
# Needed for usb passthrough for qemu >= 1.5
BuildRequires:	pkgconfig(libusb-1.0)
# SSH block driver
BuildRequires:	pkgconfig(libssh)
# GTK frontend
%if %{with gtk}
# GTK frontend
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(vte-2.91)
# GTK translations
BuildRequires: gettext
%endif
# RDMA migration
BuildRequires: rdmacm-devel
%if %{have_xen}
# Xen support
BuildRequires: xen-devel
%endif
%if %{have_numactl}
# qemu 2.1: needed for memdev hostmem backend
%ifnarch %{arm} %{risc}
BuildRequires:	numa-devel
%endif
%endif
# qemu 2.3: reading bzip2 compressed dmg images
BuildRequires: bzip2-devel
# qemu 2.4: needed for opengl bits
BuildRequires:	pkgconfig(epoxy)
# qemu 2.5: needed for TLS test suite
BuildRequires:	pkgconfig(libtasn1)
# qemu 2.5: libcacard is it's own project now
BuildRequires:	pkgconfig(libcacard)
# qemu 2.5: virgl 3d support
BuildRequires:	virglrenderer-devel
# qemu 2.6: Needed for gtk GL support
BuildRequires:	pkgconfig(gl)
# gpu vhost
BuildRequires:	pkgconfig(gbm)
# qemu 2.11: preferred disassembler for TCG
BuildRequires:	capstone-devel
BuildRequires:	pkgconfig(slirp)
# qemu 2.12: parallels disk images require libxml2 now
BuildRequires:	pkgconfig(libxml-2.0)
%ifarch %{x86_64}
# qemu 3.1: Used for nvdimm
#BuildRequires: libpmem-devel
%endif
# qemu 3.1: Used for qemu-ga
BuildRequires:	pkgconfig(udev)
# qemu 4.0: Use for qauth infrastructure
BuildRequires:	pam-devel
# qemu 4.0: sphinx-build used for some docs
BuildRequires:	python3-sphinx
# qemu 4.0: Used by test suite ./scripts/tap-driver.pl
BuildRequires:	perl-Test-Harness
# Required for making python shebangs versioned
BuildRequires:	python3-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	glib2-static-devel

BuildRequires:	pcre-static-devel
BuildRequires:	glibc-static-devel
BuildRequires:	gpg-error-static-devel

%if 0%{?hostqemu:1}
# For complicated reasons, this is required so that
# /bin/kernel-install puts the kernel directly into /boot, instead of
# into a /boot/<machine-id> subdirectory (in Fedora >= 23).  This is
# so we can run qemu-sanity-check.  Read the kernel-install script to
# understand why.
BuildRequires: grubby
%endif

Requires: %{name}-user = %{EVRD}
Requires: %{name}-system-aarch64 = %{EVRD}
Requires: %{name}-system-alpha = %{EVRD}
Requires: %{name}-system-arm = %{EVRD}
Requires: %{name}-system-avr = %{EVRD}
Requires: %{name}-system-cris = %{EVRD}
Requires: %{name}-system-m68k = %{EVRD}
Requires: %{name}-system-microblaze = %{EVRD}
Requires: %{name}-system-mips = %{EVRD}
Requires: %{name}-system-nios2 = %{EVRD}
Requires: %{name}-system-or1k = %{EVRD}
Requires: %{name}-system-ppc = %{EVRD}
Requires: %{name}-system-riscv = %{EVRD}
Requires: %{name}-system-s390x = %{EVRD}
Requires: %{name}-system-sh4 = %{EVRD}
Requires: %{name}-system-sparc = %{EVRD}
Requires: %{name}-system-tricore = %{EVRD}
Requires: %{name}-system-x86 = %{EVRD}
Requires: %{name}-system-xtensa = %{EVRD}
Requires: %{name}-img = %{EVRD}


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

%package -n	seabios
Summary:        X86 BIOS for QEMU
Group:          Emulators
BuildArch:      noarch

%description -n	seabios
SeaBIOS is an open source implementation of a 16bit x86 BIOS. SeaBIOS
is the default BIOS for QEMU.


%package  common
Summary: QEMU common files needed by all QEMU targets
Requires:	ipxe
Requires:	seabios
Requires:	sgabios
Requires:	vgabios
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%{obsoletes_some_modules}
%description common
This package provides the common files needed by all QEMU targets


%package guest-agent
Summary: QEMU guest agent
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%description guest-agent
This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.


%package  img
Summary: QEMU command line tool for manipulating disk images
%description img
This package provides a command line tool for manipulating disk images


%package  block-curl
Summary: QEMU CURL block driver
Requires: %{name}-common = %{EVRD}
%description block-curl
This package provides the additional CURL block driver for QEMU.

Install this package if you want to access remote disks over
http, https, ftp and other transports provided by the CURL library.


%package  block-dmg
Summary: QEMU block driver for DMG disk images
Requires: %{name}-common = %{EVRD}
%description block-dmg
This package provides the additional DMG block driver for QEMU.

Install this package if you want to open '.dmg' files.


%if %{with_block_gluster}
%package  block-gluster
Summary: QEMU Gluster block driver
Requires: %{name}-common = %{EVRD}
%description block-gluster
This package provides the additional Gluster block driver for QEMU.

Install this package if you want to access remote Gluster storage.
%endif


%package  block-iscsi
Summary: QEMU iSCSI block driver
Requires: %{name}-common = %{EVRD}
%description block-iscsi
This package provides the additional iSCSI block driver for QEMU.

Install this package if you want to access iSCSI volumes.


%package  block-nfs
Summary: QEMU NFS block driver
Requires: %{name}-common = %{EVRD}

%description block-nfs
This package provides the additional NFS block driver for QEMU.

Install this package if you want to access remote NFS storage.


%if %{with_block_rbd}
%package  block-rbd
Summary: QEMU Ceph/RBD block driver
Provides: qemu-kvm-block-rbd = %{EVRD}
Requires: %{name}-common = %{EVRD}

%description block-rbd
This package provides the additional Ceph/RBD block driver for QEMU.

Install this package if you want to access remote Ceph volumes
using the rbd protocol.
%endif

%package  block-ssh
Summary: QEMU SSH block driver
Requires: %{name}-common = %{EVRD}
Provides: qemu-kvm-block-ssh = %{EVRD}
%description block-ssh
This package provides the additional SSH block driver for QEMU.

Install this package if you want to access remote disks using
the Secure Shell (SSH) protocol.


%package  audio-alsa
Summary: QEMU ALSA audio driver
Requires: %{name}-common = %{EVRD}
%description audio-alsa
This package provides the additional ALSA audio driver for QEMU.

%package  audio-oss
Summary: QEMU OSS audio driver
Requires: %{name}-common = %{EVRD}
%description audio-oss
This package provides the additional OSS audio driver for QEMU.

%package  audio-pa
Summary: QEMU PulseAudio audio driver
Requires: %{name}-common = %{EVRD}
%description audio-pa
This package provides the additional PulseAudi audio driver for QEMU.

%package  audio-sdl
Summary: QEMU SDL audio driver
Requires: %{name}-common = %{EVRD}
%description audio-sdl
This package provides the additional SDL audio driver for QEMU.


%package  ui-curses
Summary: QEMU curses UI driver
Requires: %{name}-common = %{EVRD}
%description ui-curses
This package provides the additional curses UI for QEMU.

%package  ui-gtk
Summary: QEMU GTK UI driver
Requires: %{name}-common = %{EVRD}
%description ui-gtk
This package provides the additional GTK UI for QEMU.

%package  ui-sdl
Summary: QEMU SDL UI driver
Requires: %{name}-common = %{EVRD}
%description ui-sdl
This package provides the additional SDL UI for QEMU.

%package  ui-egl-headless
Summary: QEMU EGL headless driver
Requires: %{name}-common = %{EVRD}
Requires: %{name}-ui-opengl = %{EVRD}
%description ui-egl-headless
This package provides the additional egl-headless UI for QEMU.

%package  ui-opengl
Summary: QEMU OpenGL driver
Requires: %{name}-common = %{EVRD}
%description ui-opengl
This package provides the additional opengl UI for QEMU.

%package device-display-virtio-gpu
Summary: QEMU virtio-gpu display device
Requires: %{name}-common = %{EVRD}
%description device-display-virtio-gpu
This package provides the virtio-gpu display device for QEMU.

%package device-display-virtio-gpu-pci
Summary: QEMU virtio-gpu-pci display device
Requires: %{name}-common = %{EVRD}

%description device-display-virtio-gpu-pci
This package provides the virtio-gpu-pci display device for QEMU.

%package device-display-virtio-vga
Summary: QEMU virtio-vga display device
Requires: %{name}-common = %{EVRD}
%description device-display-virtio-vga
This package provides the virtio-vga display device for QEMU.

%if %{have_spice}
%package  ui-spice-core
Summary: QEMU Spice UI driver
Requires: %{name}-common = %{EVRD}
%description ui-spice-core
This package provides the additional Spice UI for QEMU.

%package  ui-spice-app
Summary: QEMU spice-app UI driver
Requires: %{name}-common = %{EVRD}
Requires: %{name}-ui-spice-core = %{EVRD}
Requires: %{name}-char-spice = %{EVRD}
%description ui-spice-app
This package provides the additional spice-app UI for QEMU.

%package device-display-qxl
Summary: QEMU QXL display device
Requires: %{name}-common = %{EVRD}
Requires: %{name}-ui-spice-core = %{EVRD}
%description device-display-qxl
This package provides the QXL display device for QEMU.

%package  char-spice
Summary: QEMU spice chardev driver
Requires: %{name}-common = %{EVRD}
Requires: %{name}-ui-spice-core = %{EVRD}
%description char-spice
This package provides the spice chardev driver for QEMU.

%package  audio-spice
Summary: QEMU spice audio driver
Requires: %{name}-common = %{EVRD}
Requires: %{name}-ui-spice-core = %{EVRD}
%description audio-spice
This package provides the spice audio driver for QEMU.
%endif

%if %{have_kvm}
%package kvm
Summary: QEMU metapackage for KVM support
Requires: qemu-%{kvm_package} = %{EVRD}
%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86


%package kvm-core
Summary: QEMU metapackage for KVM support
Requires: qemu-%{kvm_package}-core = %{EVRD}
%description kvm-core
This is a meta-package that provides a qemu-system-<arch>-core package
for native architectures where kvm can be enabled. For example, in an
x86 system, this will install qemu-system-x86-core
%endif


%package user
Summary: QEMU user mode emulation of qemu targets
Requires: %{name}-common = %{EVRD}
# On upgrade, make qemu-user get replaced with qemu-user + qemu-user-binfmt
Obsoletes: %{name}-user < 2:2.6.0-5%{?dist}
%description user
This package provides the user mode emulation of qemu targets


%package user-binfmt
Summary: QEMU user mode emulation of qemu targets
Requires: %{name}-user = %{EVRD}
Requires(post): systemd-units
Requires(postun): systemd-units
# qemu-user-binfmt + qemu-user-static both provide binfmt rules
Conflicts: %{name}-user-static
# On upgrade, make qemu-user get replaced with qemu-user + qemu-user-binfmt
Obsoletes: %{name}-user < 2:2.6.0-5%{?dist}
%description user-binfmt
This package provides the user mode emulation of qemu targets

%if %{user_static}
%package user-static-tapset
Summary: QEMU user mode emulation of qemu targets static build
Requires: %{name}-common = %{EVRD}

%description user-static-tapset
This package provides the user mode emulation of qemu targets built as
static binaries
%endif


%package system-aarch64
Summary: QEMU system emulator for AArch64
Requires: %{name}-system-aarch64-core = %{EVRD}
%{requires_all_modules}
%description system-aarch64
This package provides the QEMU system emulator for AArch64.

%package system-aarch64-core
Summary: QEMU system emulator for AArch64
Requires: %{name}-common = %{EVRD}
%if %{have_edk2}
Requires: edk2-aarch64
%endif
%description system-aarch64-core
This package provides the QEMU system emulator for AArch64.


%package system-alpha
Summary: QEMU system emulator for Alpha
Requires: %{name}-system-alpha-core = %{EVRD}
%{requires_all_modules}
%description system-alpha
This package provides the QEMU system emulator for Alpha systems.

%package system-alpha-core
Summary: QEMU system emulator for Alpha
Requires: %{name}-common = %{EVRD}
%description system-alpha-core
This package provides the QEMU system emulator for Alpha systems.


%package system-arm
Summary: QEMU system emulator for ARM
Requires: %{name}-system-arm-core = %{EVRD}
%{requires_all_modules}
%description system-arm
This package provides the QEMU system emulator for ARM systems.

%package system-arm-core
Summary: QEMU system emulator for ARM
Requires: %{name}-common = %{EVRD}
%description system-arm-core
This package provides the QEMU system emulator for ARM boards.

%package system-avr
Summary: QEMU system emulator for ARM
Requires: %{name}-system-avr-core = %{EVRD}
%{requires_all_modules}
%description system-avr
This package provides the QEMU system emulator for AVR systems.

%package system-avr-core
Summary: QEMU system emulator for ARM
Requires: %{name}-common = %{EVRD}
%description system-avr-core
This package provides the QEMU system emulator for AVR boards.


%package system-cris
Summary: QEMU system emulator for CRIS
Requires: %{name}-system-cris-core = %{EVRD}
%{requires_all_modules}
%description system-cris
This package provides the system emulator for CRIS systems.

%package system-cris-core
Summary: QEMU system emulator for CRIS
Requires: %{name}-common = %{EVRD}
%description system-cris-core
This package provides the system emulator for CRIS boards.


%package system-hppa
Summary: QEMU system emulator for HPPA
Requires: %{name}-system-hppa-core = %{EVRD}
%{requires_all_modules}
%description system-hppa
This package provides the QEMU system emulator for HPPA.

%package system-hppa-core
Summary: QEMU system emulator for hppa
Requires: %{name}-common = %{EVRD}
%description system-hppa-core
This package provides the QEMU system emulator for HPPA.


%package system-m68k
Summary: QEMU system emulator for ColdFire (m68k)
Requires: %{name}-system-m68k-core = %{EVRD}
%{requires_all_modules}
%description system-m68k
This package provides the QEMU system emulator for ColdFire boards.

%package system-m68k-core
Summary: QEMU system emulator for ColdFire (m68k)
Requires: %{name}-common = %{EVRD}
%description system-m68k-core
This package provides the QEMU system emulator for ColdFire boards.


%package system-microblaze
Summary: QEMU system emulator for Microblaze
Requires: %{name}-system-microblaze-core = %{EVRD}
%{requires_all_modules}
%description system-microblaze
This package provides the QEMU system emulator for Microblaze boards.

%package system-microblaze-core
Summary: QEMU system emulator for Microblaze
Requires: %{name}-common = %{EVRD}
%description system-microblaze-core
This package provides the QEMU system emulator for Microblaze boards.


%package system-mips
Summary: QEMU system emulator for MIPS
Requires: %{name}-system-mips-core = %{EVRD}
%{requires_all_modules}
%description system-mips
This package provides the QEMU system emulator for MIPS systems.

%package system-mips-core
Summary: QEMU system emulator for MIPS
Requires: %{name}-common = %{EVRD}
%description system-mips-core
This package provides the QEMU system emulator for MIPS systems.


%package system-nios2
Summary: QEMU system emulator for nios2
Requires: %{name}-system-nios2-core = %{EVRD}
%{requires_all_modules}
%description system-nios2
This package provides the QEMU system emulator for NIOS2.

%package system-nios2-core
Summary: QEMU system emulator for nios2
Requires: %{name}-common = %{EVRD}
%description system-nios2-core
This package provides the QEMU system emulator for NIOS2.


%package system-or1k
Summary: QEMU system emulator for OpenRisc32
Requires: %{name}-system-or1k-core = %{EVRD}
Obsoletes: %{name}-system-or32 < 2:2.9.0
%{requires_all_modules}
%description system-or1k
This package provides the QEMU system emulator for OpenRisc32 boards.

%package system-or1k-core
Summary: QEMU system emulator for OpenRisc32
Requires: %{name}-common = %{EVRD}
Obsoletes: %{name}-system-or32-core < 2:2.9.0
%description system-or1k-core
This package provides the QEMU system emulator for OpenRisc32 boards.


%package system-ppc
Summary: QEMU system emulator for PPC
Requires: %{name}-system-ppc-core = %{EVRD}
%{requires_all_modules}
%description system-ppc
This package provides the QEMU system emulator for PPC and PPC64 systems.

%package system-ppc-core
Summary: QEMU system emulator for PPC
Requires: %{name}-common = %{EVRD}
Requires: seabios
Requires: sgabios
Requires: vgabios
%description system-ppc-core
This package provides the QEMU system emulator for PPC and PPC64 systems.


%package system-riscv
Summary: QEMU system emulator for RISC-V
Requires: %{name}-system-riscv-core = %{EVRD}
%{requires_all_modules}
%description system-riscv
This package provides the QEMU system emulator for RISC-V systems.

%package system-riscv-core
Summary: QEMU system emulator for RISC-V
Requires: %{name}-common = %{EVRD}
%description system-riscv-core
This package provides the QEMU system emulator for RISC-V systems.


%package system-s390x
Summary: QEMU system emulator for S390
Requires: %{name}-system-s390x-core = %{EVRD}
%{requires_all_modules}
%description system-s390x
This package provides the QEMU system emulator for S390 systems.

%package system-s390x-core
Summary: QEMU system emulator for S390
Requires: %{name}-common = %{EVRD}
%description system-s390x-core
This package provides the QEMU system emulator for S390 systems.


%package system-sh4
Summary: QEMU system emulator for SH4
Requires: %{name}-system-sh4-core = %{EVRD}
%{requires_all_modules}
%description system-sh4
This package provides the QEMU system emulator for SH4 boards.

%package system-sh4-core
Summary: QEMU system emulator for SH4
Requires: %{name}-common = %{EVRD}
%description system-sh4-core
This package provides the QEMU system emulator for SH4 boards.


%package system-sparc
Summary: QEMU system emulator for SPARC
Requires: %{name}-system-sparc-core = %{EVRD}
%{requires_all_modules}
%description system-sparc
This package provides the QEMU system emulator for SPARC and SPARC64 systems.

%package system-sparc-core
Summary: QEMU system emulator for SPARC
Requires: %{name}-common = %{EVRD}
%description system-sparc-core
This package provides the QEMU system emulator for SPARC and SPARC64 systems.


%package system-tricore
Summary: QEMU system emulator for tricore
Requires: %{name}-system-tricore-core = %{EVRD}
%{requires_all_modules}
%description system-tricore
This package provides the QEMU system emulator for Tricore.

%package system-tricore-core
Summary: QEMU system emulator for tricore
Requires: %{name}-common = %{EVRD}
%description system-tricore-core
This package provides the QEMU system emulator for Tricore.


%package system-x86
Summary: QEMU system emulator for x86
Requires: %{name}-system-x86-core = %{EVRD}
%{requires_all_modules}
%description system-x86
This package provides the QEMU system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.

%package system-x86-core
Summary: QEMU system emulator for x86
Requires: %{name}-common = %{EVRD}
Requires: seabios
Requires: sgabios
Requires: vgabios
%if %{have_edk2}
Requires: edk2-ovmf
%endif
%description system-x86-core
This package provides the QEMU system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.


%package system-xtensa
Summary: QEMU system emulator for Xtensa
Requires: %{name}-system-xtensa-core = %{EVRD}
%{requires_all_modules}
%description system-xtensa
This package provides the QEMU system emulator for Xtensa boards.

%package system-xtensa-core
Summary: QEMU system emulator for Xtensa
Requires: %{name}-common = %{EVRD}
%description system-xtensa-core
This package provides the QEMU system emulator for Xtensa boards.

%package system-rx
Summary: QEMU system emulator for Renesas RX
%description system-rx
This package provides the QEMU system emulator for Renesas RX

%ifarch %{armx}
	#list with conf file in binfmt
	%define static_arches aarch64_be i386 x86_64 alpha armeb hexagon hppa m68k microblaze microblazeel mips mips64 mips64el mipsel mipsn32 mipsn32el or1k ppc ppc64 ppc64le riscv32 riscv64 s390x sh4 sh4eb sparc sparc32plus sparc64 xtensa xtensaeb
	#list without conf file in binfmt
	%define static_wo_binfmt cris aarch64 arm nios2 trace-stap
%else
	#list with conf file in binfmt
	%define static_arches aarch64 aarch64_be alpha arm armeb hexagon hppa m68k microblaze microblazeel mips mips64 mips64el mipsel mipsn32 mipsn32el or1k ppc ppc64 ppc64le riscv32 riscv64 s390x sh4 sh4eb sparc sparc32plus sparc64 xtensa xtensaeb
	#list without conf file in binfmt
	%define static_wo_binfmt cris i386 nios2 trace-stap x86_64
%endif

%{expand:%(for arch in %static_arches; do archstatic=${arch}; cat <<EOF
%%package       $archstatic-static
Summary:        Qemu static binary for $archstatic
# no one should require this, but provided anyway for maximum compatibility:
Provides:       qemu-static-$archstatic = %{EVRD}
Group:          System/Libraries

%%description $archstatic-static
QEMU static binary for $archstatic

%%files $archstatic-static
%{_bindir}/qemu-$archstatic-static
/usr/lib/binfmt.d/qemu-$archstatic-static.conf

%post -n qemu-$archstatic-static
%{_bindir}/systemctl restart systemd-binfmt
EOF
done)}

%{expand:%(for arch in %static_wo_binfmt; do archstatic=${arch}; cat <<EOF
%%package       $archstatic-static
Summary:        Qemu static binary for $archstatic
# no one should require this, but provided anyway for maximum compatibility:
Provides:       qemu-static-$archstatic = %{EVRD}
Group:          System/Libraries

%%description $archstatic-static
QEMU static binary for $archstatic

%%files $archstatic-static
%{_bindir}/qemu-$archstatic-static
EOF
done)}


%prep
%autosetup -p1 -n qemu-%{version}%{?beta:-%{beta}}

%build
#export CC=gcc
#export CXX=g++
%set_build_flags
# drop -g flag to prevent memory exhaustion by linker
%ifarch s390
%global optflags %(echo %{optflags} | sed 's/-g//')
sed -i.debug 's/"-g $CFLAGS"/"$CFLAGS"/g' configure
%endif

# OOM killer breaks builds with parallel make on s390(x)
%ifarch s390 s390x
%global _smp_mflags %{nil}
%endif

# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"
export LINK_ARGS="%ldflags"

# As of qemu 2.1, --enable-trace-backends supports multiple backends,
# but there's a performance impact for non-dtrace so we don't use them
tracebackends="dtrace"

%if %{have_spice}
    %global spiceflag --enable-spice
%else
    %global spiceflag --disable-spice
%endif

run_configure() {
    ../configure \
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --sysconfdir=%{_sysconfdir} \
        --localstatedir=%{_localstatedir} \
        --libexecdir=%{_libexecdir} \
        --interp-prefix=%{_prefix}/qemu-%%M \
        --with-pkgversion=%{name}-%{version}-%{release} \
        --disable-strip \
        --disable-werror \
        --enable-kvm \
%ifarch s390 %{mips64}
        --enable-tcg-interpreter \
%endif
        --enable-trace-backend=$tracebackends \
        --extra-ldflags="$extraldflags -Wl,-z,relro -Wl,-z,now" \
        --extra-cflags="%{optflags}" \
        "$@" || cat config.log
    sed -i -e 's| -Wl,--no-undefined||g' config-host.mak
}

mkdir build-dynamic
pushd build-dynamic

#--enable-slirp=system \
run_configure \
    --enable-system \
    --enable-linux-user \
    --enable-pie \
    --enable-modules \
    --audio-drv-list=pa,sdl,alsa,oss \
    --tls-priority=@QEMU,SYSTEM \
    --target-list-exclude=moxie-softmmu \
    --enable-kvm \
    --enable-mpath \
    %{spiceflag}

echo "config-host.mak contents:"
echo "==="
cat config-host.mak
echo "==="

# dirty hack
pwd
sed -i 's!-Wl,--no-undefined!!g' build.ninja

%make_build $buildldflags

popd

%if %{user_static}
mkdir build-static
pushd build-static

run_configure \
    --disable-system \
    --enable-linux-user \
    --static \
    --disable-capstone \
    --disable-pie \
    --disable-sdl \
    --disable-gtk \
    --disable-spice \
    --disable-zstd \
    --disable-tools \
    --disable-guest-agent \
    --disable-guest-agent-msi \
    --disable-curses \
    --disable-curl \
    --disable-gnutls \
    --disable-gcrypt \
    --disable-nettle \
    --disable-cap-ng \
    --disable-brlapi \
    --disable-mpath \
    --disable-libnfs \
    --disable-capstone \
    --disable-xen \
    --disable-rdma

%make_build $buildldflags

popd
%endif


%install

%global _udevdir /lib/udev/rules.d
%global qemudocdir %{_docdir}/%{name}

mkdir -p %{buildroot}%{_udevdir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/qemu
mkdir -p %{buildroot}%{_bindir}

# Install qemu-guest-agent service and udev rules
install -p -m 0644 %{_sourcedir}/qemu-guest-agent.service %{buildroot}%{_unitdir}
install -D -p -m 0644 %{_sourcedir}/qemu-ga.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/qemu-ga
install -m 0644 %{_sourcedir}/99-qemu-guest-agent.rules %{buildroot}%{_udevdir}

mkdir -p %{buildroot}%{_sysconfdir}/qemu-ga/fsfreeze-hook.d
install -p -m 0755 scripts/qemu-guest-agent/fsfreeze-hook %{buildroot}%{_sysconfdir}/qemu-ga
install -p -m 0644 scripts/qemu-guest-agent/fsfreeze-hook.d/*.sample %{buildroot}%{_sysconfdir}/qemu-ga/fsfreeze-hook.d/
mkdir -p %{buildroot}%{_localstatedir}/log
touch %{buildroot}%{_localstatedir}/log/qga-fsfreeze-hook.log

# Install qemu-pr-helper service
install -m 0644 %{_sourcedir}/qemu-pr-helper.service %{buildroot}%{_unitdir}
install -m 0644 %{_sourcedir}/qemu-pr-helper.socket %{buildroot}%{_unitdir}

%ifarch %{power64}
install -d %{buildroot}%{_sysconfdir}/security/limits.d
install -m 0644 %{_sourcedir}/95-kvm-ppc64-memlock.conf %{buildroot}%{_sysconfdir}/security/limits.d
%endif


# Install kvm specific bits
%if %{have_kvm}
mkdir -p %{buildroot}%{_bindir}/
%endif

%if %{user_static}
pushd build-static
make DESTDIR=%{buildroot} install

# Give all QEMU user emulators a -static suffix
for src in %{buildroot}%{_bindir}/qemu-*
do
  mv $src $src-static
done

# Update trace files to match

for src in %{buildroot}%{_datadir}/systemtap/tapset/qemu-*.stp
do
  dst=`echo $src | sed -e 's/.stp/-static.stp/'`
  mv $src $dst
  perl -i -p -e 's/(qemu-\w+)/$1-static/g; s/(qemu\.user\.\w+)/$1.static/g' $dst
done


popd
%endif

pushd build-dynamic
make DESTDIR=%{buildroot} install
popd

%find_lang %{name}

chmod -x %{buildroot}%{_mandir}/man1/*
install -D -p -m 0644 -t %{buildroot}%{qemudocdir} COPYING COPYING.LIB LICENSE
for emu in %{buildroot}%{_bindir}/qemu-system-*; do
    ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/$(basename $emu).1.gz
done

%if 0%{?need_qemu_kvm}
install -m 0755 %{_sourcedir}/qemu-kvm.sh %{buildroot}%{_bindir}/qemu-kvm
ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/qemu-kvm.1.gz
install -D -p -m 0644 %{_sourcedir}/kvm-x86.modprobe.conf %{buildroot}%{_sysconfdir}/modprobe.d/kvm.conf
%endif

install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

# XXX With qemu 2.11 we can probably drop this symlinking with use of
# configure --firmwarepath, see qemu git 3d5eecab4

# Provided by package openbios
#rm -rf %{buildroot}%{_datadir}/%{name}/openbios-ppc
#rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc32
#rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc64
# Provided by package SLOF
#rm -rf %{buildroot}%{_datadir}/%{name}/slof.bin
# Provided by package ipxe
#rm -rf %{buildroot}%{_datadir}/%{name}/pxe*rom
#rm -rf %{buildroot}%{_datadir}/%{name}/efi*rom
# Provided by package seavgabios
#rm -rf %{buildroot}%{_datadir}/%{name}/vgabios*bin
# Provided by package seabios
#rm -rf %{buildroot}%{_datadir}/%{name}/bios.bin
#rm -rf %{buildroot}%{_datadir}/%{name}/bios-256k.bin
# Provided by package sgabios
#rm -rf %{buildroot}%{_datadir}/%{name}/sgabios.bin

pxe_link() {
  ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/%{name}/pxe-$1.rom
  ln -s ../ipxe.efi/$2.rom %{buildroot}%{_datadir}/%{name}/efi-$1.rom
}

#pxe_link e1000 8086100e
#pxe_link ne2k_pci 10ec8029
#pxe_link pcnet 10222000
#pxe_link rtl8139 10ec8139
#pxe_link virtio 1af41000
#pxe_link eepro100 80861209
#pxe_link e1000e 808610d3
#pxe_link vmxnet3 15ad07b0

rom_link() {
    ln -s $1 %{buildroot}%{_datadir}/%{name}/$2
}

#rom_link ../seavgabios/vgabios-isavga.bin vgabios.bin
#rom_link ../seavgabios/vgabios-cirrus.bin vgabios-cirrus.bin
#rom_link ../seavgabios/vgabios-qxl.bin vgabios-qxl.bin
#rom_link ../seavgabios/vgabios-stdvga.bin vgabios-stdvga.bin
#rom_link ../seavgabios/vgabios-vmware.bin vgabios-vmware.bin
#rom_link ../seavgabios/vgabios-virtio.bin vgabios-virtio.bin
#rom_link ../seabios/bios.bin bios.bin
#rom_link ../seabios/bios-256k.bin bios-256k.bin
#rom_link ../sgabios/sgabios.bin sgabios.bin

# Install binfmt
%global binfmt_dir %{buildroot}%{_exec_prefix}/lib/binfmt.d
mkdir -p %{binfmt_dir}

./scripts/qemu-binfmt-conf.sh --systemd ALL --exportdir %{binfmt_dir} --qemu-path %{_bindir}
for i in %{binfmt_dir}/*; do
    mv $i $(echo $i | sed 's/.conf/-dynamic.conf/')
done

%if %{user_static}
for regularfmt in %{binfmt_dir}/*; do
  staticfmt="$(echo $regularfmt | sed 's/-dynamic/-static/g')"
  cat $regularfmt | tr -d '\n' | sed "s/:$/-static:F/" > $staticfmt
done
%endif
#remove conf file, qemu-i486-static not available
rm -rf %{binfmt_dir}/qemu-i486-static.conf

# Install rules to use the bridge helper with libvirt's virbr0
install -m 0644 %{_sourcedir}/bridge.conf %{buildroot}%{_sysconfdir}/qemu

# When building using 'rpmbuild' or 'fedpkg local', RPATHs can be left in
# the binaries and libraries (although this doesn't occur when
# building in Koji, for some unknown reason). Some discussion here:
#
# https://lists.fedoraproject.org/pipermail/devel/2013-November/192553.html
#
# In any case it should always be safe to remove RPATHs from
# the final binaries:
for f in %{buildroot}%{_bindir}/* %{buildroot}%{_libdir}/* \
         %{buildroot}%{_libexecdir}/*; do
  if file $f | grep -q ELF | grep -q -i shared; then chrpath --delete $f; fi
done

# We need to make the modules executable else
# RPM won't pick up their dependencies.
chmod +x %{buildroot}%{_libdir}/qemu/*.so

%check

# Tests are hanging on s390 as of 2.3.0
#   https://bugzilla.redhat.com/show_bug.cgi?id=1206057
# Tests seem to be a recurring problem on s390, so I'd suggest just leaving
# it disabled.
%global archs_skip_tests s390
# Tests seem to be broken in 4.2.0 with current glib
# MALLOC_PERTURB_=${MALLOC_PERTURB_:-$(( ${RANDOM:-0} % 255 + 1))}  QTEST_QEMU_BINARY=aarch64-softmmu/qemu-system-aarch64 QTEST_QEMU_IMG=qemu-img tests/modules-test -m=quick -k --tap < /dev/null | ./scripts/tap-driver.pl --test-name="modules-test"
#
#(tests/modules-test:1584256): GLib-ERROR **: 03:34:48.134: duplicate test case path: /aarch64//module/load/sdl
# ERROR - Bail out! GLib-FATAL-ERROR: duplicate test case path: /aarch64//module/load/sdl
%define ignore_test_failures 1

pushd build-dynamic
%ifnarch %{archs_skip_tests}

# Check the binary runs (see eg RHBZ#998722).
b="./x86_64-softmmu/qemu-system-x86_64"
if [ -x "$b" ]; then "$b" -help; fi

%if 0%{ignore_test_failures}
make check V=1 || :
%else
make check V=1
%endif

%if 0%{?hostqemu:1}
# Sanity-check current kernel can boot on this qemu.
# The results are advisory only.
qemu-sanity-check --qemu=%{?hostqemu} ||:
%endif

%endif
# archs_skip_tests
popd


%post common
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu

%post user-binfmt
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-binfmt
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post guest-agent
%systemd_post qemu-guest-agent.service
%preun guest-agent
%systemd_preun qemu-guest-agent.service
%postun guest-agent
%systemd_postun_with_restart qemu-guest-agent.service



%files
# Deliberately empty


%files common -f %{name}.lang
%dir %{qemudocdir}
%doc %{qemudocdir}/COPYING
%doc %{qemudocdir}/COPYING.LIB
%doc %{qemudocdir}/LICENSE
%doc %{qemudocdir}/interop
%doc %{qemudocdir}/specs
%doc %{_docdir}/qemu
%dir %{_datadir}/%{name}/
%{_datadir}/applications/qemu.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/%{name}/keymaps/
%{_datadir}/%{name}/trace-events-all
%{_datadir}/%{name}/bios-microvm.bin
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/vgabios-stdvga.bin
%{_datadir}/%{name}/vgabios-vmware.bin
%{_datadir}/%{name}/vgabios-virtio.bin
%{_datadir}/%{name}/vgabios-ati.bin
%{_datadir}/%{name}/pxe-e1000.rom
%{_datadir}/%{name}/efi-e1000.rom
#%%{_datadir}/%%{name}/pxe-e1000e.rom
%{_datadir}/%{name}/efi-e1000e.rom
%{_datadir}/%{name}/pxe-eepro100.rom
%{_datadir}/%{name}/efi-eepro100.rom
%{_datadir}/%{name}/pxe-ne2k_pci.rom
%{_datadir}/%{name}/efi-ne2k_pci.rom
%{_datadir}/%{name}/pxe-pcnet.rom
%{_datadir}/%{name}/efi-pcnet.rom
%{_datadir}/%{name}/pxe-rtl8139.rom
%{_datadir}/%{name}/efi-rtl8139.rom
%{_datadir}/%{name}/pxe-virtio.rom
%{_datadir}/%{name}/efi-virtio.rom
#%%{_datadir}/%%{name}/pxe-vmxnet3.rom
%{_datadir}/%{name}/efi-vmxnet3.rom
%{_datadir}/%{name}/edk2-licenses.txt
%{_datadir}/%{name}/edk2*.fd
%{_datadir}/%{name}/firmware/*.json
%{_datadir}/%{name}/qemu-nsis.bmp
%dir %{_datadir}/%{name}/vhost-user
%{_datadir}/%{name}/vhost-user/50-qemu-gpu.json
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/qemu-trace-stap.1*
%{_mandir}/man1/virtfs-proxy-helper.1*
%{_mandir}/man7/qemu-block-drivers.7*
%{_mandir}/man7/qemu-cpu-models.7*
%{_mandir}/man7/qemu-ga-ref.7*
%{_mandir}/man7/qemu-qmp-ref.7*
%{_mandir}/man8/qemu-pr-helper.8*
%{_bindir}/elf2dmp
%{_bindir}/qemu-edid
%{_bindir}/qemu-keymap
%{_bindir}/qemu-trace-stap
%if %{with seccomp}
%{_mandir}/man1/virtiofsd.1*
%{_libexecdir}/virtiofsd
%{_bindir}/qemu-pr-helper
%{_libexecdir}/virtfs-proxy-helper
%{_datadir}/qemu/vhost-user/50-qemu-virtiofsd.json
%endif
%{_bindir}/qemu-storage-daemon
%{_unitdir}/qemu-pr-helper.service
%{_unitdir}/qemu-pr-helper.socket
%attr(4755, root, root) %{_libexecdir}/qemu-bridge-helper
%{_libexecdir}/vhost-user-gpu
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
%dir %{_sysconfdir}/qemu
%config(noreplace) %{_sysconfdir}/qemu/bridge.conf
%dir %{_libdir}/qemu
%if %{have_spice}
%{_libdir}/qemu/hw-display-qxl.so
%endif
%{_libdir}/qemu/hw-usb-redirect.so
%{_libdir}/qemu/hw-usb-smartcard.so
%{_mandir}/man1/qemu-storage-daemon.1*
%{_mandir}/man7/qemu-storage-daemon-qmp-ref.7*

%files guest-agent
%{_bindir}/qemu-ga
%{_mandir}/man8/qemu-ga.8*
%{_unitdir}/qemu-guest-agent.service
%{_udevdir}/99-qemu-guest-agent.rules
%config(noreplace) %{_sysconfdir}/sysconfig/qemu-ga
%{_sysconfdir}/qemu-ga
%ghost %{_localstatedir}/log/qga-fsfreeze-hook.log


%files img
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*


%files block-curl
%{_libdir}/qemu/block-curl.so
%files block-dmg
%{_libdir}/qemu/block-dmg-bz2.so
%if %{with_block_gluster}
%files block-gluster
%{_libdir}/qemu/block-gluster.so
%endif
%files block-iscsi
%{_libdir}/qemu/block-iscsi.so
%files block-nfs
%{_libdir}/qemu/block-nfs.so
%if %{with_block_rbd}
%files block-rbd
%{_libdir}/qemu/block-rbd.so
%endif
%files block-ssh
%{_libdir}/qemu/block-ssh.so


%files audio-alsa
%{_libdir}/qemu/audio-alsa.so
%files audio-oss
%{_libdir}/qemu/audio-oss.so
%files audio-pa
%{_libdir}/qemu/audio-pa.so
%files audio-sdl
%{_libdir}/qemu/audio-sdl.so

%files ui-curses
%{_libdir}/qemu/ui-curses.so
%files ui-gtk
%{_libdir}/qemu/ui-gtk.so
%files ui-sdl
%{_libdir}/qemu/ui-sdl.so
%files ui-egl-headless
%{_libdir}/qemu/ui-egl-headless.so
%files ui-opengl
%{_libdir}/qemu/ui-opengl.so

%files device-display-virtio-gpu
%{_libdir}/qemu/hw-display-virtio-gpu.so
%files device-display-virtio-gpu-pci
%{_libdir}/qemu/hw-display-virtio-gpu-pci.so
%files device-display-virtio-vga
%{_libdir}/qemu/hw-display-virtio-vga.so

%if %{have_spice}
%files audio-spice
%{_libdir}/qemu/audio-spice.so
%files char-spice
%{_libdir}/qemu/chardev-spice.so
%files device-display-qxl
%{_libdir}/qemu/hw-display-qxl.so
%files ui-spice-core
%{_libdir}/qemu/ui-spice-core.so
%files ui-spice-app
%{_libdir}/qemu/ui-spice-app.so
%endif


%if %{have_kvm}
%files kvm
# Deliberately empty

%files kvm-core
# Deliberately empty
%endif


%files user
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-aarch64
%{_bindir}/qemu-aarch64_be
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-hexagon
%{_bindir}/qemu-hppa
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-mips64
%{_bindir}/qemu-mips64el
%{_bindir}/qemu-mipsn32
%{_bindir}/qemu-mipsn32el
%{_bindir}/qemu-nios2
%{_bindir}/qemu-or1k
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64le
%{_bindir}/qemu-riscv32
%{_bindir}/qemu-riscv64
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-xtensa
%{_bindir}/qemu-xtensaeb

%{_datadir}/systemtap/tapset/qemu-i386.stp
%{_datadir}/systemtap/tapset/qemu-i386-log.stp
%{_datadir}/systemtap/tapset/qemu-i386-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-x86_64.stp
%{_datadir}/systemtap/tapset/qemu-x86_64-log.stp
%{_datadir}/systemtap/tapset/qemu-x86_64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-aarch64.stp
%{_datadir}/systemtap/tapset/qemu-aarch64-log.stp
%{_datadir}/systemtap/tapset/qemu-aarch64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-aarch64_be.stp
%{_datadir}/systemtap/tapset/qemu-aarch64_be-log.stp
%{_datadir}/systemtap/tapset/qemu-aarch64_be-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-alpha.stp
%{_datadir}/systemtap/tapset/qemu-alpha-log.stp
%{_datadir}/systemtap/tapset/qemu-alpha-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-arm.stp
%{_datadir}/systemtap/tapset/qemu-arm-log.stp
%{_datadir}/systemtap/tapset/qemu-arm-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-armeb.stp
%{_datadir}/systemtap/tapset/qemu-armeb-log.stp
%{_datadir}/systemtap/tapset/qemu-armeb-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-cris.stp
%{_datadir}/systemtap/tapset/qemu-cris-log.stp
%{_datadir}/systemtap/tapset/qemu-cris-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-hexagon.stp
%{_datadir}/systemtap/tapset/qemu-hexagon-log.stp
%{_datadir}/systemtap/tapset/qemu-hexagon-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-hppa.stp
%{_datadir}/systemtap/tapset/qemu-hppa-log.stp
%{_datadir}/systemtap/tapset/qemu-hppa-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-m68k.stp
%{_datadir}/systemtap/tapset/qemu-m68k-log.stp
%{_datadir}/systemtap/tapset/qemu-m68k-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-microblaze.stp
%{_datadir}/systemtap/tapset/qemu-microblaze-log.stp
%{_datadir}/systemtap/tapset/qemu-microblaze-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel-log.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mips.stp
%{_datadir}/systemtap/tapset/qemu-mips-log.stp
%{_datadir}/systemtap/tapset/qemu-mips-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-mipsel-log.stp
%{_datadir}/systemtap/tapset/qemu-mipsel-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mips64.stp
%{_datadir}/systemtap/tapset/qemu-mips64-log.stp
%{_datadir}/systemtap/tapset/qemu-mips64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mips64el.stp
%{_datadir}/systemtap/tapset/qemu-mips64el-log.stp
%{_datadir}/systemtap/tapset/qemu-mips64el-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32-log.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el-log.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-nios2.stp
%{_datadir}/systemtap/tapset/qemu-nios2-log.stp
%{_datadir}/systemtap/tapset/qemu-nios2-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-or1k.stp
%{_datadir}/systemtap/tapset/qemu-or1k-log.stp
%{_datadir}/systemtap/tapset/qemu-or1k-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-ppc.stp
%{_datadir}/systemtap/tapset/qemu-ppc-log.stp
%{_datadir}/systemtap/tapset/qemu-ppc-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-ppc64-log.stp
%{_datadir}/systemtap/tapset/qemu-ppc64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le-log.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-riscv32.stp
%{_datadir}/systemtap/tapset/qemu-riscv32-log.stp
%{_datadir}/systemtap/tapset/qemu-riscv32-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-riscv64.stp
%{_datadir}/systemtap/tapset/qemu-riscv64-log.stp
%{_datadir}/systemtap/tapset/qemu-riscv64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-s390x.stp
%{_datadir}/systemtap/tapset/qemu-s390x-log.stp
%{_datadir}/systemtap/tapset/qemu-s390x-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sh4.stp
%{_datadir}/systemtap/tapset/qemu-sh4-log.stp
%{_datadir}/systemtap/tapset/qemu-sh4-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb-log.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sparc.stp
%{_datadir}/systemtap/tapset/qemu-sparc-log.stp
%{_datadir}/systemtap/tapset/qemu-sparc-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus-log.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sparc64.stp
%{_datadir}/systemtap/tapset/qemu-sparc64-log.stp
%{_datadir}/systemtap/tapset/qemu-sparc64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-xtensa.stp
%{_datadir}/systemtap/tapset/qemu-xtensa-log.stp
%{_datadir}/systemtap/tapset/qemu-xtensa-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-xtensaeb.stp
%{_datadir}/systemtap/tapset/qemu-xtensaeb-log.stp
%{_datadir}/systemtap/tapset/qemu-xtensaeb-simpletrace.stp

%dir %doc %{_docdir}/qemu
%doc %{_docdir}/qemu/index.html
%doc %{_docdir}/qemu/user
%doc %{_docdir}/qemu/system
%doc %{_docdir}/qemu/tools

%files user-binfmt
%{_exec_prefix}/lib/binfmt.d/qemu-*-dynamic.conf

%if %{user_static}
%files user-static-tapset
%{_datadir}/systemtap/tapset/qemu-*-static.stp
%endif


%files system-aarch64
%files system-aarch64-core
%{_bindir}/qemu-system-aarch64
%{_datadir}/systemtap/tapset/qemu-system-aarch64*.stp
%{_mandir}/man1/qemu-system-aarch64.1*


%files system-alpha
%files system-alpha-core
%{_bindir}/qemu-system-alpha
%{_datadir}/systemtap/tapset/qemu-system-alpha*.stp
%{_mandir}/man1/qemu-system-alpha.1*
%{_datadir}/%{name}/palcode-clipper


%files system-arm
%files system-arm-core
%{_bindir}/qemu-system-arm
%{_datadir}/systemtap/tapset/qemu-system-arm*.stp
%{_datadir}/%{name}/npcm7xx_bootrom.bin
%{_mandir}/man1/qemu-system-arm.1*


%files system-cris
%files system-cris-core
%{_bindir}/qemu-system-cris
%{_datadir}/systemtap/tapset/qemu-system-cris*.stp
%{_mandir}/man1/qemu-system-cris.1*


%files system-hppa
%files system-hppa-core
%{_bindir}/qemu-system-hppa
%{_datadir}/systemtap/tapset/qemu-system-hppa*.stp
%{_mandir}/man1/qemu-system-hppa.1*
%{_datadir}/%{name}/hppa-firmware.img


%files system-m68k
%files system-m68k-core
%{_bindir}/qemu-system-m68k
%{_datadir}/systemtap/tapset/qemu-system-m68k*.stp
%{_mandir}/man1/qemu-system-m68k.1*


%files system-microblaze
%files system-microblaze-core
%{_bindir}/qemu-system-microblaze
%{_bindir}/qemu-system-microblazeel
%{_datadir}/systemtap/tapset/qemu-system-microblaze*.stp
%{_mandir}/man1/qemu-system-microblaze.1*
%{_mandir}/man1/qemu-system-microblazeel.1*
%{_datadir}/%{name}/petalogix*.dtb


%files system-mips
%files system-mips-core
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%{_datadir}/systemtap/tapset/qemu-system-mips*.stp
%{_mandir}/man1/qemu-system-mips.1*
%{_mandir}/man1/qemu-system-mipsel.1*
%{_mandir}/man1/qemu-system-mips64el.1*
%{_mandir}/man1/qemu-system-mips64.1*


%files system-nios2
%files system-nios2-core
%{_bindir}/qemu-system-nios2
%{_datadir}/systemtap/tapset/qemu-system-nios2*.stp
%{_mandir}/man1/qemu-system-nios2.1*


%files system-or1k
%files system-or1k-core
%{_bindir}/qemu-system-or1k
%{_datadir}/systemtap/tapset/qemu-system-or1k*.stp
%{_mandir}/man1/qemu-system-or1k.1*


%files system-ppc
%files system-ppc-core
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
%{_datadir}/systemtap/tapset/qemu-system-ppc*.stp
%{_mandir}/man1/qemu-system-ppc.1*
%{_mandir}/man1/qemu-system-ppc64.1*
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/canyonlands.dtb
%{_datadir}/%{name}/qemu_vga.ndrv
%{_datadir}/%{name}/skiboot.lid
%{_datadir}/%{name}/u-boot.e500
%{_datadir}/%{name}/u-boot-sam460-20100605.bin
%ifarch %{power64}
%{_sysconfdir}/security/limits.d/95-kvm-ppc64-memlock.conf
%endif


%files system-riscv
%files system-riscv-core
%{_bindir}/qemu-system-riscv32
%{_bindir}/qemu-system-riscv64
%{_datadir}/systemtap/tapset/qemu-system-riscv*.stp
%{_datadir}/qemu/opensbi-riscv*.*
%{_mandir}/man1/qemu-system-riscv*.1*


%files system-s390x
%files system-s390x-core
%{_bindir}/qemu-system-s390x
%{_datadir}/systemtap/tapset/qemu-system-s390x*.stp
%{_mandir}/man1/qemu-system-s390x.1*
%{_libdir}/qemu/hw-s390x-virtio-gpu-ccw.so
%{_datadir}/%{name}/s390-ccw.img
%{_datadir}/%{name}/s390-netboot.img


%files system-sh4
%files system-sh4-core
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb
%{_datadir}/systemtap/tapset/qemu-system-sh4*.stp
%{_mandir}/man1/qemu-system-sh4.1*
%{_mandir}/man1/qemu-system-sh4eb.1*


%files system-sparc
%files system-sparc-core
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-sparc64
%{_datadir}/systemtap/tapset/qemu-system-sparc*.stp
%{_mandir}/man1/qemu-system-sparc.1*
%{_mandir}/man1/qemu-system-sparc64.1*
%{_datadir}/%{name}/QEMU,tcx.bin
%{_datadir}/%{name}/QEMU,cgthree.bin


%files system-tricore
%files system-tricore-core
%{_bindir}/qemu-system-tricore
%{_datadir}/systemtap/tapset/qemu-system-tricore*.stp
%{_mandir}/man1/qemu-system-tricore.1*


%files system-x86
%files system-x86-core
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_datadir}/systemtap/tapset/qemu-system-i386*.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64*.stp
%{_mandir}/man1/qemu-system-i386.1*
%{_mandir}/man1/qemu-system-x86_64.1*
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/bios-256k.bin
%{_datadir}/%{name}/kvmvapic.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/linuxboot_dma.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/qemu/openbios-sparc32
%{_datadir}/qemu/openbios-sparc64
%{_datadir}/qemu/openbios-ppc
%{_datadir}/%{name}/qboot.rom
%{_datadir}/%{name}/slof.bin
%{_datadir}/qemu/vgabios-bochs-display.bin
%{_datadir}/qemu/vgabios-ramfb.bin

%{_datadir}/%{name}/pvh.bin
%{_datadir}/%{name}/sgabios.bin
%if 0%{?need_qemu_kvm}
%{_bindir}/qemu-kvm
%{_mandir}/man1/qemu-kvm.1*
%config(noreplace) %{_sysconfdir}/modprobe.d/kvm.conf
%endif


%files system-xtensa
%files system-xtensa-core
%{_bindir}/qemu-system-xtensa
%{_bindir}/qemu-system-xtensaeb
%{_datadir}/systemtap/tapset/qemu-system-xtensa*.stp
%{_mandir}/man1/qemu-system-xtensa.1*
%{_mandir}/man1/qemu-system-xtensaeb.1*

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

%files system-rx
%{_bindir}/qemu-system-rx
%{_datadir}/man/man1/qemu-system-rx.1*
%{_datadir}/systemtap/tapset/qemu-system-rx-log.stp
%{_datadir}/systemtap/tapset/qemu-system-rx-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-system-rx.stp

%files system-avr
%files system-avr-core
%{_bindir}/qemu-system-avr
%{_datadir}/systemtap/tapset/qemu-system-avr*.stp
%{_mandir}/man1/qemu-system-avr.1*
