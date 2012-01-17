%define qemu_name	qemu-kvm
%define qemu_version	1.0
%define qemu_rel	1
#define qemu_snapshot	0
%define qemu_release	%mkrel %{?qemu_snapshot:0.%{qemu_snapshot}.}%{qemu_rel}

%define __find_requires %{_builddir}/%{qemu_name}-%{qemu_version}%{?qemu_snapshot:-%{qemu_snapshot}}/find_requires.sh

Summary:	QEMU CPU Emulator
Name:		qemu
Version:	%{qemu_version}
Release:	%{qemu_release}
Source0:	http://downloads.sourceforge.net/project/kvm/%{qemu_name}/%{version}/%{qemu_name}-%{version}%{?qemu_snapshot:-%{qemu_snapshot}}.tar.gz
Source1:	kvm.modules
Patch0:		qemu-kvm-1.0-unbreak-i8259-migration.patch
Patch1:		qemu-kvm-1.0-deprecate-time-drift-fix.patch

# KSM control scripts
Source4: ksm.init
Source5: ksm.sysconfig
Source6: ksmtuned.init
Source7: ksmtuned
Source8: ksmtuned.conf

License:	GPL
URL:		http://wiki.qemu.org/Main_Page
Group:		Emulators
Provides:	kvm
Obsoletes:	kvm < 86
Requires:	qemu-img = %{version}-%{release}
# for %%{_sysconfdir}/sasl2
Requires:	cyrus-sasl
BuildRequires:	libSDL-devel
BuildRequires:	texi2html
# XXXX: -luuid
BuildRequires:	e2fsprogs-devel
BuildRequires:	kernel-headers	
BuildRequires:	pulseaudio-devel
BuildRequires:	zlib-devel
BuildRequires:	brlapi-devel
BuildRequires:	gnutls-devel
BuildRequires:	libsasl2-devel
BuildRequires:	%{_lib}pci-devel
BuildRequires:	%{_lib}png-devel
BuildRequires:	texinfo
# not in main
#BuildRequires:	vde-devel
BuildRequires:	dev86
BuildRequires:	iasl
# glibc-devel with fixed preadv/pwritev prototypes
BuildRequires:	glibc-devel >= 6:2.10.1-7mnb2
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
%setup -q -n %{qemu_name}-%{qemu_version}%{?qemu_snapshot:-%{qemu_snapshot}}
%patch0 -p1 -b .i8259~
%patch1 -p1 -b .notdf~

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
./configure \
	--target-list=x86_64-softmmu \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--audio-drv-list=pa,sdl,alsa,oss \
	--extra-ldflags=$extraldflags \
	--extra-cflags="$CFLAGS" \
	--enable-vnc-png

%make V=1 $buildldflags
cp -a x86_64-softmmu/qemu-system-x86_64 qemu-kvm
make clean

#pushd kvm
#./configure \
#	--prefix=%{_prefix} \
#	--kerneldir="`pwd`/../kernel/" \
#	--with-kvm-trace
##make kvmtrace
#make
#popd
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
	--sysconfdir=%{_sysconfdir} \
	--interp-prefix=%{_prefix}/qemu-%%M \
	--audio-drv-list=pa,sdl,alsa,oss \
	--disable-kvm \
	--extra-ldflags=$extraldflags \
	--extra-cflags="$CFLAGS" \
	--enable-vnc-png

%make V=1 $buildldflags

%install
rm -rf %{buildroot}

install -D -p -m 0755 %{SOURCE4} %{buildroot}%{_initrddir}/ksm
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/ksm

install -D -p -m 0755 %{SOURCE6} %{buildroot}%{_initrddir}/ksmtuned
install -D -p -m 0755 %{SOURCE7} %{buildroot}%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE8} %{buildroot}%{_sysconfdir}/ksmtuned.conf

%ifarch %{ix86} x86_64
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/modules
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/%{name}

install -m 0755 %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 kvm/kvm_stat %{buildroot}%{_bindir}/
install -m 0755 qemu-kvm %{buildroot}%{_bindir}/
%endif

%makeinstall_std BUILD_DOCS="yes"

install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

#QPM
install -m 0755 QMP/qmp-shell %{buildroot}/%{_bindir}/qmp-shell
install -d %{buildroot}/%{py_platsitedir}
install -m 0755 QMP/qmp.py %{buildroot}/%{py_platsitedir}/qmp.py

# remove unpackaged files
rm -rf %{buildroot}%{_docdir}/qemu

%clean
rm -rf %{buildroot}

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

%triggerpostun -- qemu < 0.10.4-6
rm -f /etc/rc.d/*/{K,S}??qemu

%files
%defattr(-,root,root)
%doc README qemu-doc.html qemu-tech.html
%config(noreplace)%{_sysconfdir}/sasl2/qemu.conf
%{_initrddir}/ksm
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%{_initrddir}/ksmtuned
%{_sbindir}/ksmtuned
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%{_sysconfdir}/sysconfig/modules/kvm.modules
%{_sysconfdir}/qemu/target-x86_64.conf
%{_bindir}/kvm_stat
%{_bindir}/qemu-io
%{_bindir}/qemu-kvm
%{_bindir}/qemu
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
%{_bindir}/qemu-system-m68k
%{_bindir}/qemu-system-sh4*
%{_bindir}/qemu-system-ppc*
%{_bindir}/qemu-system-mips*
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-x86_64
%{_bindir}/qmp-shell
%{_mandir}/man1/qemu.1*
%{_mandir}/man8/qemu-nbd.8*
%dir %{_datadir}/qemu
%{_datadir}/qemu/*.bin
%{_datadir}/qemu/*.rom
%{_datadir}/qemu/keymaps
%{_datadir}/qemu/openbios-sparc32
%{_datadir}/qemu/openbios-sparc64
%{_datadir}/qemu/openbios-ppc
%{_datadir}/qemu/bamboo.dtb
%{_datadir}/qemu/mpc8544ds.dtb
%{_datadir}/qemu/petalogix-ml605.dtb
%{_datadir}/qemu/petalogix-s3adsp1800.dtb
%{py_platsitedir}/qmp.py
%files img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*
