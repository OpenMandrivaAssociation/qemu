%define qemu_name	qemu
%define qemu_version	1.6.1
%define qemu_rel	1
#define qemu_snapshot	0
%define qemu_release	%mkrel %{?qemu_snapshot:0.%{qemu_snapshot}.}%{qemu_rel}

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
Version:	%{qemu_version}
Release:	%{qemu_release}
Source0:	http://wiki.qemu-project.org/download/%{qemu_name}-%{version}%{?qemu_snapshot:-%{qemu_snapshot}}.tar.bz2
Source1:	kvm.modules
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

Patch000:	qemu-1.6.1-fix-ar.patch
# This patch queue is auto-generated from https://github.com/openSUSE/qemu
Patch0001:      0001-XXX-dont-dump-core-on-sigabort.patc.patch
Patch0002:      0002-XXX-work-around-SA_RESTART-race-wit.patch
Patch0003:      0003-qemu-0.9.0.cvs-binfmt.patch.patch
Patch0004:      0004-qemu-cvs-alsa_bitfield.patch.patch
Patch0005:      0005-qemu-cvs-alsa_ioctl.patch.patch
Patch0006:      0006-qemu-cvs-alsa_mmap.patch.patch
Patch0007:      0007-qemu-cvs-gettimeofday.patch.patch
Patch0008:      0008-qemu-cvs-ioctl_debug.patch.patch
Patch0009:      0009-qemu-cvs-ioctl_nodirection.patch.patch
Patch0010:      0010-block-vmdk-Support-creation-of-SCSI.patch
Patch0011:      0011-linux-user-add-binfmt-wrapper-for-a.patch
Patch0012:      0012-linux-user-Ignore-timer_create-sysc.patch
Patch0013:      0013-linux-user-be-silent-about-capget-f.patch
Patch0014:      0014-PPC-KVM-Disable-mmu-notifier-check..patch
Patch0015:      0015-linux-user-fix-segfault-deadlock.pa.patch
Patch0016:      0016-linux-user-binfmt-support-host-bina.patch
Patch0017:      0017-linux-user-arm-no-tb_flush-on-reset.patch
Patch0018:      0018-linux-user-Ignore-broken-loop-ioctl.patch
Patch0019:      0019-linux-user-lock-tcg.patch.patch
Patch0020:      0020-linux-user-Run-multi-threaded-code-.patch
Patch0021:      0021-linux-user-lock-tb-flushing-too.pat.patch
Patch0022:      0022-linux-user-Fake-proc-cpuinfo.patch.patch
Patch0023:      0023-linux-user-implement-FS_IOC_GETFLAG.patch
Patch0024:      0024-linux-user-implement-FS_IOC_SETFLAG.patch
Patch0025:      0025-linux-user-XXX-disable-fiemap.patch.patch
Patch0026:      0026-slirp-nooutgoing.patch.patch
Patch0027:      0027-vnc-password-file-and-incoming-conn.patch
Patch0028:      0028-linux-user-add-more-blk-ioctls.patc.patch
Patch0029:      0029-linux-user-use-target_ulong.patch.patch
Patch0030:      0030-Add-support-for-DictZip-enabled-gzi.patch
Patch0031:      0031-Add-tar-container-format.patch.patch
Patch0032:      0032-Legacy-Patch-kvm-qemu-preXX-dictzip.patch
Patch0033:      0033-Legacy-Patch-kvm-qemu-preXX-report-.patch
Patch0034:      0034-console-add-question-mark-escape-op.patch
Patch0035:      0035-Make-char-muxer-more-robust-wrt-sma.patch
Patch0036:      0036-linux-user-lseek-explicitly-cast-no.patch
Patch0037:      0037-virtfs-proxy-helper-Provide-__u64-f.patch
Patch0039:      0039-roms-Build-vgabios.bin.patch.patch
Patch0040:      0040-configure-Enable-PIE-for-ppc-and-pp.patch

# roms/ipxe patches
Patch1000:      ipxe-build-Work-around-bug-in-gcc-4.8.patch
Patch1001:      ipxe-zbin-Fix-size-used-for-memset-in-al.patch
Patch1002:      ipxe-build-Avoid-strict-aliasing-warning.patch
# end roms/ipxe patches


License:	GPLv2+
URL:		http://wiki.qemu.org/Main_Page
Group:		Emulators
Provides:	kvm
Requires:	qemu-img = %{version}-%{release}
Requires:	sgabios
Requires:	vgabios
Requires:	ipxe
Requires:	seabios


BuildRequires:      pkgconfig(sdl)
BuildRequires:      pkgconfig(zlib)
BuildRequires:      texi2html
BuildRequires:      pkgconfig(gnutls)
BuildRequires:      sasl-devel
BuildRequires:      libtool
BuildRequires:      libaio-devel
BuildRequires:      rsync
BuildRequires:      pkgconfig(libpci)
BuildRequires:      pkgconfig(libpulse)
BuildRequires:      pkgconfig(libiscsi)
BuildRequires:      alsa-oss-devel
BuildRequires:      ncurses-devel
BuildRequires:      attr-devel
%if %{with usbredir}
BuildRequires: usbredir-devel >= 0.5.2
%endif
BuildRequires: texinfo
%if %{with spice}
BuildRequires:      pkgconfig(spice-server)
BuildRequires:      pkgconfig(spice-protocol)
%endif
%if %{with seccomp}
BuildRequires:      pkgconfig(libseccomp)
%endif
# For network block driver
BuildRequires:      pkgconfig(libcurl)
%if %{with rbd}
# For rbd block driver
BuildRequires:      %{_lib}ceph-devel
%endif
# We need both because the 'stap' binary is probed for by configure
BuildRequires:      systemtap
BuildRequires:      systemtap-devel
# For smartcard NSS support
BuildRequires:      nss-devel
# For XFS discard support in raw-posix.c
%if %{with xfsprogs}
BuildRequires:      xfsprogs-devel
%endif
# For VNC JPEG support
BuildRequires:      jpeg-devel
# For VNC PNG support
BuildRequires:      pkgconfig(libpng)
# For uuid generation
BuildRequires:      pkgconfig(uuid)
# For BlueZ device support
BuildRequires:      pkgconfig(bluez)
# For Braille device support
BuildRequires:      brlapi-devel
%if %{with fdt}
# For FDT device tree support
BuildRequires:      fdt-devel
%endif
# xen
BuildRequires:		xen-devel
# For virtfs
BuildRequires:      pkgconfig(libcap-ng)
BuildRequires:      cap-devel
# Hard requirement for version >= 1.3
BuildRequires:      pkgconfig(pixman-1)
# Needed for usb passthrough for qemu >= 1.5
BuildRequires:      pkgconfig(libusb-1.0) 
# SSH block driver
BuildRequires:      pkgconfig(libssh)
%if %{with gtk}
# GTK frontend
BuildRequires:      pkgconfig(gtk+-3.0)
BuildRequires:      pkgconfig(vte)
%endif
# GTK translations
BuildRequires:      gettext
# RDMA migration
BuildRequires:		librdmacm-devel
BuildRequires:		pkgconfig(vdehist)


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
Version:	%{qemu_version}
Release:	%{qemu_release}

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
Provides:       qemu:%_bindir/qemu-ga

%description guest-agent
QEMU is an extremely well-performing CPU emulator that allows you to
choose between simulating an entire system and running userspace
binaries for different architectures under your native operating
system. It currently emulates x86, ARM, PowerPC and SPARC CPUs as well
as PC and PowerMac systems.

This sub-package contains the guest agent.

%prep
%setup -q -n %{qemu_name}-%{qemu_version}%{?qemu_snapshot:-%{qemu_snapshot}}
%apply_patches

%build
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

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

dobuild() {
    ./configure \
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --sysconfdir=%{_sysconfdir} \
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
%ifarch %ix86 x86_64
	--enable-xen \
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
        --enable-tpm \
        "$@"

    echo "config-host.mak contents:"
    echo "==="
    cat config-host.mak
    echo "==="

    %make V=1 $buildldflags
}


dobuild --target-list="$buildarch"
%{__cc} %{SOURCE9} -O2 -g -o ksmctl


%install
install -D -p -m 0644 %{SOURCE4} %{buildroot}/%{_unitdir}/ksm.service
install -D -p -m 0644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl %{buildroot}/lib/systemd/ksmctl

install -D -p -m 0644 %{SOURCE6} %{buildroot}/%{_unitdir}/ksmtuned.service
install -D -p -m 0755 %{SOURCE7} %{buildroot}/%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE8} %{buildroot}/%{_sysconfdir}/ksmtuned.conf

install -D -p -m 0644 %{SOURCE10} %{buildroot}/%{_unitdir}/qemu-guest-agent.service

mkdir -p %{buildroot}%{_udevrulesdir}
install -D -p -m 0644 %{SOURCE11} %{buildroot}%{_udevrulesdir}
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_udevrulesdir}

# Install rules to use the bridge helper with libvirt's virbr0
mkdir -p %{buildroot}%{_sysconfdir}/qemu/
install -D -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/qemu/


%ifarch %{ix86} x86_64
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/modules
mkdir -p %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_datadir}/%{name}

install -m 0755 %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/modules/kvm.modules
%endif

%makeinstall_std BUILD_DOCS="yes"

install -D -p -m 0644 qemu.sasl %{buildroot}/%{_sysconfdir}/sasl2/qemu.conf

# remove unpackaged files
rm -rf %{buildroot}/%{_docdir}/qemu %{buildroot}%{_bindir}/vscclient
rm -f %{buildroot}/%{_libdir}/libcacard*
rm -f %{buildroot}/usr/lib/libcacard*
rm -f %{buildroot}/%{_libdir}/pkgconfig/libcacard.pc
rm -f %{buildroot}/usr/lib/pkgconfig/libcacard.pc
rm -rf %{buildroot}/%{_includedir}/cacard

install -d -m 755 %{buildroot}/%_sbindir
install -m 755 scripts/qemu-binfmt-conf.sh %{buildroot}/%_sbindir
%ifnarch %ix86 x86_64
ln -sf ../../../emul/ia32-linux %{buildroot}/usr/share/qemu/qemu-i386
%endif
%ifnarch ia64
mkdir -p %{buildroot}/emul/ia32-linux
%endif


%post 
%ifarch %{ix86} x86_64
# load kvm modules now, so we can make sure no reboot is needed.
# If there's already a kvm module installed, we don't mess with it
sh /%{_sysconfdir}/sysconfig/modules/kvm.modules
%endif
%_post_service ksmtuned
%_post_service ksm

%preun
%_preun_service ksm
%_preun_service ksmtuned

%files
%doc README qemu-doc.html qemu-tech.html
%config(noreplace)%{_sysconfdir}/sasl2/qemu.conf
%{_unitdir}/ksm.service
/lib/systemd/ksmctl
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%{_udevrulesdir}/80-kvm.rules
%{_unitdir}/ksmtuned.service
%{_sbindir}/ksmtuned
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%config(noreplace) %{_sysconfdir}/qemu/bridge.conf
%{_sysconfdir}/sysconfig/modules/kvm.modules
%{_sysconfdir}/qemu/target-x86_64.conf
%{_bindir}/qemu-system-*
%{_bindir}/virtfs-proxy-helper
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/virtfs-proxy-helper.*
%dir %{_datadir}/qemu
%{_datadir}/qemu/keymaps
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

%files linux-user
%{_datadir}/%{name}/ppc_rom.bin
%{_datadir}/%{name}/s390-zipl.rom
%{_datadir}/%{name}/spapr-rtas.bin
%{_datadir}/%{name}/slof.bin
%{_datadir}/%{name}/palcode-clipper
%{_datadir}/%{name}/s390-ccw.img
%_bindir/qemu-alpha
%_bindir/qemu-arm
%_bindir/qemu-armeb
%_bindir/qemu-cris
%_bindir/qemu-i386
%_bindir/qemu-m68k
%_bindir/qemu-microblaze
%_bindir/qemu-microblazeel
%_bindir/qemu-mips
%_bindir/qemu-mipsel
%_bindir/qemu-mipsn32
%_bindir/qemu-mipsn32el
%_bindir/qemu-mips64
%_bindir/qemu-mips64el
%_bindir/qemu-or32
%_bindir/qemu-ppc64abi32
%_bindir/qemu-ppc64
%_bindir/qemu-ppc
%_bindir/qemu-s390x
%_bindir/qemu-sh4
%_bindir/qemu-sh4eb
%_bindir/qemu-sparc32plus
%_bindir/qemu-sparc64
%_bindir/qemu-sparc
%_bindir/qemu-unicore32
%_bindir/qemu-x86_64
%_bindir/qemu-*-binfmt
%_sbindir/qemu-binfmt-conf.sh
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
%_datadir/%name/bios.bin
%_datadir/%name/acpi-dsdt.aml
%_datadir/%name/q35-acpi-dsdt.aml

%files -n vgabios
%_datadir/%name/vgabios.bin
%_datadir/%name/vgabios-cirrus.bin
%_datadir/%name/vgabios-qxl.bin
%_datadir/%name/vgabios-stdvga.bin
%_datadir/%name/vgabios-vmware.bin

%files -n sgabios
%_datadir/%name/sgabios.bin

%files -n ipxe
%_datadir/%name/pxe-e1000.rom
%_datadir/%name/pxe-eepro100.rom
%_datadir/%name/pxe-pcnet.rom
%_datadir/%name/pxe-ne2k_pci.rom
%_datadir/%name/pxe-rtl8139.rom
%_datadir/%name/pxe-virtio.rom

%files guest-agent
%_bindir/qemu-ga
%{_unitdir}/qemu-guest-agent.service
%{_udevrulesdir}/99-qemu-guest-agent.rules
