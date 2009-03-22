%define qemu_name	qemu
%define qemu_version	0.10.1
%define qemu_rel	3
#define qemu_snapshot	r6685
%define qemu_release	%mkrel %{?qemu_snapshot:0.%{qemu_snapshot}.}%{qemu_rel}

# XXX add service
%define kqemu_name	kqemu
%define kqemu_version	1.4.0
%define kqemu_reldelta	1
%define kqemu_rel	%(perl -e 'print %{qemu_rel} + %{kqemu_reldelta}')
%define kqemu_snapshot	pre1
%define kqemu_fullver	%{kqemu_version}%{?kqemu_snapshot:%{kqemu_snapshot}}
%define kqemu_dkmsver	%{kqemu_fullver}-%{kqemu_rel}
%define kqemu_release	%mkrel %{?kqemu_snapshot:0.%{kqemu_snapshot}.}%{kqemu_rel}
%define kqemu_arches	%{ix86} x86_64
%ifarch %{ix86}
%define kqemu_program	qemu
%endif
%ifarch x86_64
%define kqemu_program	qemu-system-x86_64
%endif

# Additionnal packaging notes
# XXX defined as macros so that to avoid extraneous empty lines
%ifarch %{kqemu_arches}
%define kqemu_note \
This QEMU package provides support for KQEMU, the QEMU Accelerator\
module.
%else
%define kqemu_note %{nil}
%endif

%define __find_requires %{_builddir}/%{qemu_name}-%{qemu_version}/find_requires.sh

Summary:	QEMU CPU Emulator
Name:		%{qemu_name}
Version:	%{qemu_version}
Release:	%{qemu_release}
Source0:	http://bellard.org/qemu/%{name}-%{version}%{?qemu_snapshot:-%{qemu_snapshot}}.tar.gz
Source1:	http://bellard.org/qemu/kqemu-%{kqemu_fullver}.tar.gz
Source2:	qemu.init
Patch11:	qemu-kernel-option-vga.patch

License:	GPL
URL:		http://bellard.org/qemu/
Group:		Emulators
Requires:	qemu-img = %{version}-%{release}
BuildRequires:	libSDL-devel, tetex-texi2html
# XXXX: -luuid
BuildRequires:	e2fsprogs-devel
BuildRequires:  kernel-headers	
BuildRequires:	pulseaudio-devel
BuildRequires:	zlib-devel
ExclusiveArch:	%{ix86} ppc x86_64 amd64 %{sunsparc}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%ifarch %{kqemu_arches}
# XXX: move up if some qemu-bridge is implemented for networking
Requires(post):   rpm-helper
Requires(preun):  rpm-helper
Suggests:	  dkms-%{kqemu_name} >= %{kqemu_version}-%{kqemu_release}
%endif

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
%kqemu_note

%package -n dkms-%{kqemu_name}
Summary:	QEMU Accelerator Module
Group:		System/Kernel and hardware
Version:	%{kqemu_version}
Release:	%{kqemu_release}
Requires(post):	 dkms
Requires(preun): dkms

%description -n dkms-%{kqemu_name}
QEMU Accelerator (KQEMU) is a driver allowing the QEMU PC emulator to
run much faster when emulating a PC on an x86 host.

Full virtualization mode can also be enabled (with -kernel-kqemu) for
best performance. This mode only works with the following guest OSes:
Linux 2.4, Linux 2.6, Windows 2000 and Windows XP. WARNING: for
Windows 2000/XP, you cannot use it during installation.

Use "%{kqemu_program}" to benefit from the QEMU Accelerator Module.

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
%setup -q -a 1 
%patch11 -p1 -b .kernel-option-vga

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
#	--enable-bsd-user \
./configure --cc=%{__cc} \
	--audio-drv-list="pa alsa sdl oss" \
	--prefix=%_prefix \
	--enable-system \
	--enable-linux-user
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

# make sure to use the right accelerator-capable qemu binary on x86_64
cd $RPM_BUILD_ROOT%{_bindir}
mv qemu qemu-system-i386
%ifarch x86_64
ln -s qemu-system-x86_64 qemu
%else
ln -s qemu-system-i386 qemu
%endif
cd -

%ifarch %{kqemu_arches}
# install kqemu sources
mkdir -p $RPM_BUILD_ROOT%{_usr}/src/%{kqemu_name}-%{kqemu_dkmsver}
(cd kqemu-%{kqemu_fullver} && tar cf - .) | \
(cd $RPM_BUILD_ROOT%{_usr}/src/%{kqemu_name}-%{kqemu_dkmsver} && tar xf -)
cat > $RPM_BUILD_ROOT%{_usr}/src/%{kqemu_name}-%{kqemu_dkmsver}/dkms.conf << EOF
PACKAGE_NAME=%{kqemu_name}
PACKAGE_VERSION=%{kqemu_dkmsver}
MAKE[0]="./configure --kernel-path=/lib/modules/\${kernelver}/source && make"
DEST_MODULE_LOCATION[0]=/kernel/3rdparty/%{kqemu_name}
BUILT_MODULE_NAME[0]=%{kqemu_name}
AUTOINSTALL=yes
EOF

# install service
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/%{name}

# install udev rules
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/65-%{kqemu_name}.rules << EOF
KERNEL=="%{kqemu_name}", MODE="0666"
EOF
%endif

# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_docdir}/qemu

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

%post -n dkms-%{kqemu_name}
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m %{kqemu_name} -v %{kqemu_dkmsver}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{kqemu_name} -v %{kqemu_dkmsver}
/usr/sbin/dkms --rpm_safe_upgrade install -m %{kqemu_name} -v %{kqemu_dkmsver}
/sbin/modprobe %{kqemu_name} >/dev/null 2>&1 || :

%preun -n dkms-%{kqemu_name}
# rmmod can fail
/sbin/rmmod %{kqemu_name} >/dev/null 2>&1
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{kqemu_name} -v %{kqemu_dkmsver} --all || :

%files
%defattr(-,root,root)
%doc README qemu-doc.html qemu-tech.html
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
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_mandir}/man1/qemu.1*
%{_mandir}/man8/qemu-nbd.8.*
%dir %{_datadir}/qemu
%{_datadir}/qemu/*.bin
%{_datadir}/qemu/keymaps
%{_datadir}/qemu/video.x
%{_datadir}/qemu/openbios-sparc32
%{_datadir}/qemu/openbios-sparc64
%{_datadir}/qemu/openbios-ppc
%{_datadir}/qemu/bamboo.dtb
%{_initrddir}/%{name}

%files img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*

%ifarch %{kqemu_arches}
%files -n dkms-%{kqemu_name}
%defattr(-,root,root)
%doc kqemu-%{kqemu_fullver}/README
%doc kqemu-%{kqemu_fullver}/kqemu-doc.html
%doc kqemu-%{kqemu_fullver}/kqemu-tech.html
%dir %{_usr}/src/%{kqemu_name}-%{kqemu_dkmsver}
%{_usr}/src/%{kqemu_name}-%{kqemu_dkmsver}/*
%_sysconfdir/udev/rules.d/65-%{kqemu_name}.rules
%endif
