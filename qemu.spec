Summary:	QEMU CPU Emulator
Name:		qemu
Version:	1.2.0
Release:	1
Source0:	http://wiki.qemu.org/download/%{name}-%{version}.tar.bz2

%define qemu_snapshot	0
#Release:	%{?qemu_snapshot:0.%{qemu_snapshot}.}1
#Source0:	http://wiki.qemu.org/download/%{name}-%{version}%{?qemu_snapshot:-%{qemu_snapshot}}.tar.bz2

Source1:	kvm.modules

# KSM control scripts
Source4:	ksm.init
Source5:	ksm.sysconfig
Source6:	ksmtuned.init
Source7:	ksmtuned
Source8:	ksmtuned.conf

Source100:	qemu.rpmlintrc

License:	GPLv2+ and LGPLv2+ and BSD
URL:		http://wiki.qemu.org/Main_Page
Group:		Emulators
%rename		kvm
Requires:	qemu-img = %{EVRD}
# for %%{_sysconfdir}/sasl2
Requires:	cyrus-sasl
BuildRequires:	pkgconfig(sdl)
BuildRequires:	texi2html
# XXXX: -luuid
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	kernel-headers
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig
BuildRequires:	brlapi-devel
BuildRequires:	pkgconfig(gnutls) >= 3.0
BuildRequires:	libsasl2-devel
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(libpng15)
BuildRequires:	texinfo
# not in main
#BuildRequires:	vde-devel
BuildRequires:	dev86
BuildRequires:	iasl
# glibc-devel with fixed preadv/pwritev prototypes
BuildRequires:	glibc-devel >= 6:2.10.1-7mnb2
ExclusiveArch:	%{ix86} ppc x86_64 amd64 %{sparcx}

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

%build
#(proyvind): binutils upstream bug #10862, linking with gold fails if doing parallel build
mkdir -p bfd
ln -s %{_bindir}/ld.bfd bfd/ld
export PATH=$PWD/bfd:$PATH

%ifarch %{ix86} x86_64
# sdl outputs to alsa or pulseaudio depending on system config, but it's broken (RH bug #495964)
# alsa works, but causes huge CPU load due to bugs
# oss works, but is very problematic because it grabs exclusive control of the device causing other apps to go haywire
./configure \
	--target-list=x86_64-softmmu \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--audio-drv-list=pa,sdl,alsa,oss \
	--disable-strip \
	--extra-ldflags="%{ldflags}" \
	--extra-cflags="%{optflags}" \
	--enable-vnc-png

%make V=1
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
	--disable-strip \
	--extra-ldflags="%{ldflags}" \
	--extra-cflags="%{optflags}" \
	--enable-vnc-png

%make V=1

%install
install -D -p -m 0755 %{SOURCE4} %{buildroot}%{_initrddir}/ksm
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/ksm

install -D -p -m 0755 %{SOURCE6} %{buildroot}%{_initrddir}/ksmtuned
install -D -p -m 0755 %{SOURCE7} %{buildroot}%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE8} %{buildroot}%{_sysconfdir}/ksmtuned.conf

%ifarch %{ix86} x86_64
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/modules
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}

install -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 scripts/kvm/kvm_stat %{buildroot}%{_bindir}
install -m 0755 qemu-kvm %{buildroot}%{_bindir}
%endif

%makeinstall_std BUILD_DOCS="yes"

install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

#QPM
install -m 0755 QMP/qmp-shell %{buildroot}%{_bindir}/qmp-shell
install -d %{buildroot}%{py_platsitedir}
install -m 0755 QMP/qmp.py %{buildroot}%{py_platsitedir}/qmp.py

# remove unpackaged files
rm -rf %{buildroot}%{_docdir}/qemu

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
%{_bindir}/qemu-system-x86_64
%{_bindir}/qmp-shell
%{_bindir}/virtfs-proxy-helper
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/virtfs-proxy-helper.1*
%{_mandir}/man8/qemu-nbd.8*
%{_prefix}/libexec/qemu-bridge-helper
%dir %{_datadir}/qemu
%{_datadir}/qemu/*.bin
%{_datadir}/qemu/*.rom
%{_datadir}/qemu/cpus-x86_64.conf
%{_datadir}/qemu/keymaps
%{_datadir}/qemu/openbios-sparc32
%{_datadir}/qemu/openbios-sparc64
%{_datadir}/qemu/openbios-ppc
%{_datadir}/qemu/bamboo.dtb
%{_datadir}/qemu/mpc8544ds.dtb
%{_datadir}/qemu/palcode-clipper
%{_datadir}/qemu/petalogix-ml605.dtb
%{_datadir}/qemu/petalogix-s3adsp1800.dtb
%{_datadir}/qemu/qemu-icon.bmp
%{py_platsitedir}/qmp.py

%files img
%{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*
