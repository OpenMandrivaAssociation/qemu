%define qemu_version	2.3.0
#define qemu_snapshot	0

%ifarch %{ix86} x86_64
%bcond_without	firmwares # build firmwares from source
%endif

%bcond_without rbd              # enabled
%bcond_without gtk              # enabled
%bcond_without usbredir         # enabled
%bcond_without xfsprogs         # enabled
%bcond_without spice            # enabled
%ifarch %{ix86} x86_64
%bcond_without seccomp          # enabled
%else
%bcond_with seccomp             # disabled
%endif
# libfdt is only needed to build ARM, Microblaze or PPC emulators
%bcond_without fdt



Summary:	QEMU CPU Emulator
Name:		qemu
Version:	%{qemu_version}%{?qemu_snapshot:~%{qemu_snapshot}}
Release:	2
License:	GPLv2+
Group:		Emulators
Url:		http://wiki.qemu.org/Main_Page
Source0:	http://wiki.qemu-project.org/download/%{name}-%{qemu_version}%{?qemu_snapshot:-%{qemu_snapshot}}.tar.bz2
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
Source14:	qemu-wrapper.c
#cb - from mageia http://lists.gnu.org/archive/html/qemu-devel/2014-01/msg01035.html
Patch0:		qemu-2.0.0-mga-compile-fix.patch

# CVE-2015-3456: (VENOM) fdc: out-of-bounds fifo buffer memory access
Patch1:		0001-fdc-force-the-fifo-access-to-be-in-bounds-of-the-all.patch

BuildRequires:	gettext
BuildRequires:	libtool
BuildRequires:	rsync
BuildRequires:	texinfo
BuildRequires:	texi2html
BuildRequires:	alsa-oss-devel
BuildRequires:	attr-devel
BuildRequires:	brlapi-devel
BuildRequires:	cap-devel
BuildRequires:	glibc-static-devel
BuildRequires:	jpeg-devel
BuildRequires:	libaio-devel
BuildRequires:	librdmacm-devel
BuildRequires:	nss-devel
BuildRequires:	numa-devel
BuildRequires:	sasl-devel
BuildRequires:	snappy-devel
# We need both because the 'stap' binary is probed for by configure
BuildRequires:	systemtap
BuildRequires:	systemtap-devel
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(glusterfs-api)
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
%if 1
# reverting back to SDL 1.2 untill SDL 2.0 support is working properly
BuildRequires:	pkgconfig(sdl)
%define	sdlabi	1.2
%else
BuildRequires:	pkgconfig(sdl2)
%define	sdlabi	2.0
%endif
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(vdehist)
BuildRequires:	pkgconfig(zlib)
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
BuildRequires:	%{_lib}ceph-devel
%endif
# For XFS discard support in raw-posix.c
%if %{with xfsprogs}
BuildRequires:	xfsprogs-devel
%endif
%if %{with fdt}
# For FDT device tree support
BuildRequires:	fdt-devel
%endif
%ifnarch %arm
# xen
BuildRequires:	xen-devel
%endif
# For virtfs
%if %{with gtk}
# GTK frontend
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(vte)
%endif
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
%prep
%setup -q -n %{name}-%{qemu_version}%{?qemu_snapshot:-%{qemu_snapshot}}
%apply_patches

%build
export CC=gcc
export CXX=g++
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

mkdir -p qemu-static
pushd qemu-static
cp %{SOURCE14} qemu-wrapper.c
../configure	--python=%{__python2} \
		--target-list=aarch64-linux-user,arm-linux-user,mips-linux-user,mipsel-linux-user \
		--enable-tcg-interpreter \
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
		--disable-vnc-tls \
		--disable-vnc-sasl \
		--disable-vnc-jpeg \
		--disable-vnc-png \
		--disable-vnc-ws \
		--disable-curses \
		--disable-curl \
		--disable-fdt \
		--disable-bluez \
		--disable-slirp \
		--disable-rdma \
		--disable-system \
		--disable-bsd-user \
		--disable-guest-base \
		--disable-uuid \
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
		--disable-smartcard-nss \
		--disable-libusb \
		--disable-usb-redir \
		--disable-guest-agent \
		--disable-seccomp \
		--with-coroutine=ucontext \
		--enable-coroutine-pool \
		--disable-glusterfs \
		--disable-archipelago \
		--disable-tpm \
		--disable-libssh2 \
		--disable-vhdx \
		--disable-quorum \
		--disable-numa \
		--disable-lzo \
		--disable-rbd \
		--enable-kvm \
		--extra-ldflags="-static -Wl,-z,relro -Wl,-z,now" \
		--extra-cflags="%{optflags}"
%make V=1 $buildldflags
gcc -static qemu-wrapper.c %{optflags} %{ldflags} -O3 -o qemu-wrapper
popd

dobuild() {
    ../configure \
	--enable-system \
	--enable-user \
	--enable-linux-user \
	--python=%{__python2} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir} \
	--audio-drv-list=pa,sdl,alsa,oss \
	--localstatedir=%{_localstatedir} \
	--libexecdir=%{_libexecdir} \
	--disable-strip \
	--extra-ldflags="$extraldflags -pie -Wl,-z,relro -Wl,-z,now" \
	--extra-cflags="%{optflags} -fPIE -DPIE" \
	--enable-trace-backend=dtrace \
	--disable-werror \
	--enable-kvm \
	--enable-tcg-interpreter \
	--enable-tpm \
%ifarch %{ix86} x86_64
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
%endif
%if %{with fdt}
	--enable-fdt \
%else
	--disable-fdt \
%endif
%if %{with gtk}
	--with-gtkabi="3.0" \
%endif
	--enable-sdl \
	--with-sdlabi="%{sdlabi}" \
%if %{with usbredir}
	--enable-usb-redir \
%else
	--disable-usb-redir \
%endif
	--enable-snappy \
	--enable-glusterfs \
	--enable-libnfs \
	--enable-guest-agent \
	--enable-modules \
	--enable-numa \
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

%ifarch %{ix86} x86_64 %{arm}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/modules
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/%{name}
%endif

%makeinstall_std -C system BUILD_DOCS="yes"

install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

# remove unpackaged files
rm -rf %{buildroot}%{_docdir}/qemu %{buildroot}%{_bindir}/vscclient
rm -f %{buildroot}%{_libdir}/libcacard*
rm -f %{buildroot}/usr/lib/libcacard*
rm -f %{buildroot}%{_libdir}/pkgconfig/libcacard.pc
rm -f %{buildroot}/usr/lib/pkgconfig/libcacard.pc
rm -rf %{buildroot}%{_includedir}/cacard

install -d -m 755 %{buildroot}%{_sbindir}
install -m 755 scripts/qemu-binfmt-conf.sh %{buildroot}%{_sbindir}
%ifnarch %ix86 x86_64
ln -sf ../../../emul/ia32-linux %{buildroot}/usr/share/qemu/qemu-i386
%endif
%ifnarch ia64
mkdir -p %{buildroot}/emul/ia32-linux
%endif
rm -rf %{buildroot}%{_datadir}/%{name}/QEMU,tcx.bin

install -d %{buildroot}%{_binfmtdir}
install -m755 qemu-static/aarch64-linux-user/qemu-aarch64 -D %{buildroot}%{_bindir}/qemu-static-aarch64
install -m755 qemu-static/arm-linux-user/qemu-arm -D %{buildroot}%{_bindir}/qemu-static-arm
install -m755 qemu-static/qemu-wrapper -D %{buildroot}%{_bindir}/qemu-static-armv7hl
install -m755 qemu-static/mips-linux-user/qemu-mips -D %{buildroot}%{_bindir}/qemu-static-mips
install -m755 qemu-static/mipsel-linux-user/qemu-mipsel -D %{buildroot}%{_bindir}/qemu-static-mipsel
echo ':aarch64:M::\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\xb7:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff:/usr/bin/qemu-static-aarch64:' > %{buildroot}%{_binfmtdir}/aarch64.conf
echo ':arm:M::\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x28\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff:/usr/bin/qemu-static-armv7hl:' > %{buildroot}%{_binfmtdir}/arm.conf
echo ':mips:M::\x7fELF\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x08:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff:/usr/bin/qemu-static-mips:' > %{buildroot}%{_binfmtdir}/mips.conf
echo ':mipsel:M::\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x08\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff:/usr/bin/qemu-static-mipsel:' > %{buildroot}%{_binfmtdir}/mipsel.conf

%find_lang %{name}

%files -f %{name}.lang
%doc README system/qemu-doc.html system/qemu-tech.html
%config(noreplace)%{_sysconfdir}/sasl2/qemu.conf
%{_unitdir}/ksm.service
/lib/systemd/ksmctl
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%{_udevrulesdir}/80-kvm.rules
%{_unitdir}/ksmtuned.service
%{_sbindir}/ksmtuned
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%config(noreplace) %{_sysconfdir}/qemu/bridge.conf
%{_sysconfdir}/qemu/target-x86_64.conf
%{_bindir}/qemu-system-*
%{_bindir}/virtfs-proxy-helper
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/virtfs-proxy-helper.*
%dir %{_datadir}/qemu
%{_datadir}/qemu/keymaps
%{_datadir}/qemu/trace-events
%{_datadir}/qemu/openbios-sparc32
%{_datadir}/qemu/openbios-sparc64
%{_datadir}/qemu/openbios-ppc
%{_datadir}/qemu/*.dtb
%{_datadir}/qemu/qemu-icon.bmp
%{_libexecdir}/qemu-bridge-helper
%{_datadir}/qemu/*.svg
%{_datadir}/systemtap/tapset/*
%{_datadir}/%{name}/efi-rtl8139.rom
%{_datadir}/%{name}/efi-ne2k_pci.rom
%{_datadir}/%{name}/efi-pcnet.rom
%{_datadir}/%{name}/efi-e1000.rom
%{_datadir}/%{name}/efi-virtio.rom
%{_datadir}/%{name}/efi-eepro100.rom
%{_datadir}/%{name}/kvmvapic.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/QEMU,cgthree.bin
%{_datadir}/%{name}/bios-256k.bin
%{_datadir}/%{name}/u-boot.e500
%dir %{_libdir}/qemu
%{_libdir}/qemu/block-curl.so
%{_libdir}/qemu/block-gluster.so
%{_libdir}/qemu/block-iscsi.so
%{_libdir}/qemu/block-rbd.so
%{_libdir}/qemu/block-ssh.so

%files linux-user
%{_datadir}/%{name}/ppc_rom.bin
%{_datadir}/%{name}/s390-zipl.rom
%{_datadir}/%{name}/spapr-rtas.bin
%{_datadir}/%{name}/slof.bin
%{_datadir}/%{name}/palcode-clipper
%{_datadir}/%{name}/s390-ccw.img
%{_bindir}/qemu-aarch64
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
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
%{_bindir}/qemu-or32
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64abi32
%{_bindir}/qemu-ppc64le
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-sparc
%{_bindir}/qemu-unicore32
%{_bindir}/qemu-x86_64
%{_sbindir}/qemu-binfmt-conf.sh
%ifnarch %ix86 x86_64 ia64
%dir /emul/ia32-linux
%endif
%ifnarch %ix86 x86_64
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/qemu-i386
%endif

%files img
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_mandir}/man8/qemu-nbd.8*
%{_mandir}/man1/qemu-img.1*

%files -n seabios
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/acpi-dsdt.aml
%{_datadir}/%{name}/q35-acpi-dsdt.aml

%files -n vgabios
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/vgabios-stdvga.bin
%{_datadir}/%{name}/vgabios-vmware.bin

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
%{_unitdir}/qemu-guest-agent.service
%{_udevrulesdir}/99-qemu-guest-agent.rules

%files -n qemu-static-aarch64
%{_bindir}/qemu-static-aarch64
%{_binfmtdir}/aarch64.conf

%files -n qemu-static-arm
%{_bindir}/qemu-static-armv7hl
%{_bindir}/qemu-static-arm
%{_binfmtdir}/arm.conf

%files -n qemu-static-mips
%{_bindir}/qemu-static-mips
%{_binfmtdir}/mips.conf

%files -n qemu-static-mipsel
%{_bindir}/qemu-static-mipsel
%{_binfmtdir}/mipsel.conf
