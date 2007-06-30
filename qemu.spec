%define qemu_name	qemu
%define qemu_version	0.9.0
%define qemu_rel	7
#define qemu_release	%mkrel %{?qemu_snapshot:0.%{qemu_snapshot}.}%{qemu_rel}
%define qemu_release	%mkrel %{qemu_rel}
%define qemu_snapshot	20070214

# XXX add service
%define kqemu_name	kqemu
%define kqemu_version	1.3.0
%define kqemu_reldelta	3
%define kqemu_rel	%(perl -e 'print %{qemu_rel} - %{kqemu_reldelta}')
%define kqemu_snapshot	pre11
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

%define kvm_arches	%{ix86} x86_64

# Additionnal packaging notes
# XXX defined as macros so that to avoid extraneous empty lines
%ifarch %{kqemu_arches}
%define kqemu_note \
This QEMU package provides support for KQEMU, the QEMU Accelerator\
module.
%else
%define kqemu_note %{nil}
%endif
%ifarch %{kvm_arches}
%define kvm_note \
This QEMU package provides support for KVM (Kernel-based Virtual \
Machine), a full virtualization solution for Linux on x86 hardware \
containing virtualization extensions (AMD-v or Intel VT).
%else
%define kvm_note %{nil}
%endif

# Define targets to enable, allow redefinition from rpm build
%define all_targets i386-linux-user arm-linux-user armeb-linux-user arm-softmmu sparc-linux-user ppc-linux-user i386-softmmu ppc-softmmu sparc-softmmu x86_64-softmmu mips-softmmu
%{expand: %{!?targets: %%global targets %{all_targets}}}

%define __find_requires %{_builddir}/%{name}-%{version}/find_requires.sh

Summary:	QEMU CPU Emulator
Name:		%{qemu_name}
Version:	%{qemu_version}
Release:	%{qemu_release}
Source0:	%{name}-%{version}%{?qemu_snapshot:-%{qemu_snapshot}}.tar.bz2
Source1:	kqemu-%{kqemu_fullver}.tar.bz2
Source2:	qemu.init
Source3:	qemu.completion
Patch1:		qemu-0.9.0-gcc4.patch
Patch2:		qemu-0.7.0-gcc4-dot-syms.patch
Patch3:		qemu-0.8.3-enforce-16byte-boundaries.patch
Patch4:		qemu-0.9.0-osx-intel-port.patch
Patch10:	qemu-0.7.0-cross64-mingw32-fixes.patch
Patch11:	qemu-0.9.0-kernel-option-vga.patch
Patch12:	qemu-0.7.2-no-nptl.patch
Patch13:	qemu-0.8.1-fix-errno-tls.patch
Patch14:	qemu-0.8.3-dont-strip.patch
Patch15:	qemu-0.8.3-x86_64-opts.patch
Patch16:	qemu-0.9.0-ppc.patch
Patch17:	qemu-0.9.0-fix-cpus-chaining.patch
Patch18:	qemu-0.9.0-migration.patch
Patch19:	qemu-0.9.0-not-rh-toolchain.patch
Patch20:	qemu-0.9.0-increase-initrd-load-addr.patch
Patch21:	qemu-0.9.0-fix-x86-fprem.patch
Patch22:	qemu-0.9.0-qcow2-fixes.patch
Patch23:	qemu-0.9.0-fix-pgtable-calculation.patch
Patch200:	qemu-0.9.0-kvm.patch
Source201:	kvm_bios.bin
Patch201:	qemu-0.9.0-kvm-bios.patch
Patch202:	qemu-0.9.0-kvm-kqemu-window-caption.patch

License:	GPL
URL:		http://fabrice.bellard.free.fr/qemu/
Group:		Emulators
Requires:	qemu-img = %{version}-%{release}
BuildRequires:	libSDL-devel, tetex-texi2html
# XXXX: -luuid
BuildRequires:	e2fsprogs-devel
ExclusiveArch:	%{ix86} ppc x86_64 amd64 sparc
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%ifarch %{kqemu_arches}
# XXX: move up if some qemu-bridge is implemented for networking
Requires(post):   rpm-helper
Requires(preun):  rpm-helper
Requires:	  dkms-%{kqemu_name} >= %{kqemu_version}-%{kqemu_release}
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
%kvm_note

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
%patch1 -p1 -b .gcc4
%patch2 -p1 -b .gcc4-dot-syms
%patch3 -p1 -b .enforce-16byte-boundaries
%patch4 -p1 -b .osx-intel-port
%patch10 -p1 -b .cross64-mingw32-fixes
%patch11 -p1 -b .kernel-option-vga
%if %{mdkversion} < 200700
%patch12 -p1 -b .no-nptl
%endif
%patch13 -p1 -b .fix-errno-tls
%patch14 -p1 -b .dont-strip
%patch15 -p1 -b .x86_64-opts
%patch16 -p1 -b .ppc
%patch17 -p1 -b .fix-cpus-chaining
%patch18 -p1 -b .migration
%patch19 -p1 -b .not-rh-toolchain
%patch20 -p1 -b .increase-initrd-load-addr
%patch21 -p1 -b .fix-x86-fprem
%patch22 -p1 -b .qcow2-fixes
%patch23 -p1 -b .fix-pgtable-calculation

# kvm patches
%patch200 -p1 -b .kvm
cp %{SOURCE201} pc-bios/kvm_bios.bin
%patch201 -p1 -b .kvm-bios
%patch202 -p1 -b .kvm-kqemu-window-caption

# nuke explicit dependencies on GLIBC_PRIVATE
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
%configure2_5x --cc=%{__cc} --disable-gcc-check --target-list="%{targets}" --disable-gcc-check
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

%ifarch %{kvm_arches}
# install udev rules
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/65-kvm.rules << EOF
KERNEL=="kvm", MODE="0666"
EOF
%endif

# bash completion
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

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
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-i386
%{_bindir}/qemu-ppc
%{_bindir}/qemu-sparc
%{_bindir}/qemu-system-arm
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_mandir}/man1/qemu.1*
%dir %{_datadir}/qemu
%{_datadir}/qemu/*.bin
%{_datadir}/qemu/keymaps
%{_datadir}/qemu/video.x
%{_datadir}/qemu/openbios-sparc32
%{_initrddir}/%{name}
%ifarch %{kvm_arches}
%_sysconfdir/udev/rules.d/65-kvm.rules
%endif

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
