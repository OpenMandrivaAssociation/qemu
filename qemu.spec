%define qemu_name	qemu-kvm
%define qemu_version	0.10.5
%define qemu_rel	1
#define qemu_snapshot	r6685
%define qemu_release	%mkrel %{?qemu_snapshot:0.%{qemu_snapshot}.}%{qemu_rel}

%define __find_requires %{_builddir}/%{qemu_name}-%{qemu_version}/find_requires.sh

Summary:	QEMU CPU Emulator
Name:		qemu
Version:	%{qemu_version}
Release:	%{qemu_release}
Source0:	http://kent.dl.sourceforge.net/sourceforge/kvm/%{qemu_name}-%{version}%{?qemu_snapshot:-%{qemu_snapshot}}.tar.gz
Source1:	kvm.modules
Source2:	README.install.urpmi
Patch0:		qemu-kernel-option-vga.patch
Patch1:		01-tls-handshake-fix.patch
Patch2:		02-vnc-monitor-info.patch
Patch3:		03-display-keymaps.patch
Patch4:		04-vnc-struct.patch
Patch5:		05-vnc-tls-vencrypt.patch
Patch6:		06-vnc-sasl.patch
Patch7:		07-vnc-monitor-authinfo.patch
Patch8:		08-vnc-acl-mgmt.patch

Patch9:		kvm-upstream-ppc.patch
Patch10:	qemu-fix-debuginfo.patch
Patch12:	qemu-roms-more-room.patch
Patch13:	qemu-roms-more-room-fix-vga-align.patch
Patch14:	qemu-bios-bigger-roms.patch
Patch15:	qemu-kvm-fix-kerneldir-includes.patch
Patch21:	qemu-make-x86-cpuid-feature-names-available-in-file-scope.patch
Patch22:	qemu-fix-x86-feature-modifications-for-features-that-set.patch
Patch23:	qemu-trim-cpu-features-not-supported-by-kvm.patch

Patch24:	qemu-kvm-allow-kqemu.patch

License:	GPL
URL:		http://bellard.org/qemu/
Group:		Emulators
Provides:	kvm
Obsoletes:	kvm < 86
Requires:	qemu-img = %{version}-%{release}
# for %%{_sysconfdir}/sasl2
Requires:	cyrus-sasl
BuildRequires:	libSDL-devel
BuildRequires:	tetex-texi2html
# XXXX: -luuid
BuildRequires:	e2fsprogs-devel
BuildRequires:  kernel-headers	
BuildRequires:	pulseaudio-devel
BuildRequires:	zlib-devel
BuildRequires:	brlapi-devel
BuildRequires:	gnutls-devel
BuildRequires:	libsasl2-devel
# not in main
#BuildRequires:	vde-devel
BuildRequires:	dev86
BuildRequires:	iasl
ExclusiveArch:	%{ix86} ppc x86_64 amd64 %{sunsparc}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package img
Summary:	QEMU disk image utility
Group:		Emulators
Version:	%{qemu_version}
Release:	%{qemu_release}
Conflicts:	qemu < 0.9.0-%{mkrel 3}

%description img
This package contains the QEMU disk image utility that is used to
create, commit, convert and get information from a disk image.

%prep
%setup -q -n %{qemu_name}-%{qemu_version}
%patch0 -p1 -b .kernel-option-vga

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
#%patch21 -p1
#%patch22 -p1
#%patch23 -p1
%patch24 -p1 -b .kqemu

# nuke explicit dependencies on GLIBC_PRIVATE
# (Anssi 03/2008) FIXME: use _requires_exceptions
cat >find_requires.sh << EOF
#!/bin/sh
%{_prefix}/lib/rpm/find-requires %{buildroot} %{_target_cpu} | grep -v GLIBC_PRIVATE
EOF
chmod +x find_requires.sh

%build
# don't use -mtune=generic if it is not supported
if ! echo | %{__cc} -mtune=generic -xc -c - -o /dev/null 2> /dev/null; then
  CFLAGS=`echo "$RPM_OPT_FLAGS" | sed -e "s/-mtune=generic/-mtune=pentiumpro/g"`
fi
 
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

%ifarch %{ix86} x86_64
# sdl outputs to alsa or pulseaudio depending on system config, but it's broken (RH bug #495964)
# alsa works, but causes huge CPU load due to bugs
# oss works, but is very problematic because it grabs exclusive control of the device causing other apps to go haywire
./configure --target-list=x86_64-softmmu \
            --prefix=%{_prefix} \
            --audio-drv-list=pa,sdl,alsa,oss \
            --extra-ldflags=$extraldflags \
            --extra-cflags="$CFLAGS"

make V=1 %{?_smp_mflags} $buildldflags
cp -a x86_64-softmmu/qemu-system-x86_64 qemu-kvm
make clean

make -C kvm/extboot extboot.bin

cd kvm/user
./configure --prefix=%{_prefix} --kerneldir=$(pwd)/../kernel/
make kvmtrace
cd ../../
%endif

./configure \
    --target-list="i386-softmmu x86_64-softmmu arm-softmmu cris-softmmu m68k-softmmu \
                mips-softmmu mipsel-softmmu mips64-softmmu mips64el-softmmu ppc-softmmu \
                ppcemb-softmmu ppc64-softmmu sh4-softmmu sh4eb-softmmu sparc-softmmu \
                i386-linux-user x86_64-linux-user alpha-linux-user arm-linux-user \
                armeb-linux-user cris-linux-user m68k-linux-user mips-linux-user \
                mipsel-linux-user ppc-linux-user ppc64-linux-user ppc64abi32-linux-user \
                sh4-linux-user sh4eb-linux-user sparc-linux-user sparc64-linux-user \
                sparc32plus-linux-user" \
    --prefix=%{_prefix} \
    --interp-prefix=%{_prefix}/qemu-%%M \
    --audio-drv-list=pa,sdl,alsa,oss \
    --disable-kvm \
    --extra-ldflags=$extraldflags \
    --extra-cflags="$CFLAGS"

%make V=1 $buildldflags

%install
rm -rf $RPM_BUILD_ROOT

%ifarch %{ix86} x86_64
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/modules
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 kvm/extboot/extboot.bin $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m 0755 kvm/user/kvmtrace $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 kvm/user/kvmtrace_format $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 kvm/kvm_stat $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 qemu-kvm $RPM_BUILD_ROOT%{_bindir}/
%endif

%makeinstall_std

chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*

install -D -p -m 0644 qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl2/qemu.conf

mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d/
cat > %{buildroot}%{_sysconfdir}/udev/rules.d/65-kvm.rules << EOF
KERNEL=="kvm", MODE="0666"
EOF

# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_docdir}/qemu

install -m 644 %{SOURCE1} README.install.urpmi

%clean
rm -rf $RPM_BUILD_ROOT

%post 
%ifarch %{ix86} x86_64
# load kvm modules now, so we can make sure no reboot is needed.
# If there's already a kvm module installed, we don't mess with it
sh /%{_sysconfdir}/sysconfig/modules/kvm.modules
%endif

%triggerpostun -- qemu < 0.10.4-6
rm -f /etc/rc.d/*/{K,S}??qemu

%files
%defattr(-,root,root)
%doc README README.install.urpmi qemu-doc.html qemu-tech.html
%config(noreplace)%{_sysconfdir}/udev/rules.d/65-kvm.rules
%config(noreplace)%{_sysconfdir}/sasl2/qemu.conf
%{_sysconfdir}/sysconfig/modules/kvm.modules
%{_bindir}/kvm_stat
%{_bindir}/kvmtrace
%{_bindir}/kvmtrace_format
%{_bindir}/qemu-kvm
%{_bindir}/qemu
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm*
%{_bindir}/qemu-cris
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
%{_bindir}/qemu-system-m68k
%{_bindir}/qemu-system-sh4*
%{_bindir}/qemu-system-ppc*
%{_bindir}/qemu-system-mips*
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-x86_64
%{_mandir}/man1/qemu.1*
%{_mandir}/man8/qemu-nbd.8*
%dir %{_datadir}/qemu
%{_datadir}/qemu/*.bin
%{_datadir}/qemu/keymaps
%{_datadir}/qemu/video.x
%{_datadir}/qemu/openbios-sparc32
%{_datadir}/qemu/openbios-sparc64
%{_datadir}/qemu/openbios-ppc
%{_datadir}/qemu/bamboo.dtb

%files img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*
