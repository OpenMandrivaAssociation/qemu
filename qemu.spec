%bcond_with    x86only          # disabled
%bcond_with    exclusive_x86_64 # disabled
%bcond_without rbd              # enabled
%bcond_without fdt              # enabled

%define _udevdir /lib/udev/rules.d
%define qemudocdir %{_docdir}/%{name}

Summary:	QEMU CPU Emulator
Name:		qemu
Version:	1.2.0
Release:	2
Source0:	http://wiki.qemu.org/download/%{name}-%{version}.tar.bz2

%define qemu_snapshot	0
#Release:	%{?qemu_snapshot:0.%{qemu_snapshot}.}1
#Source0:	http://wiki.qemu.org/download/%{name}-%{version}%{?qemu_snapshot:-%{qemu_snapshot}}.tar.bz2

Source1: qemu.binfmt

# Loads kvm kernel modules at boot
Source2: kvm.modules

# Creates /dev/kvm
Source3: 80-kvm.rules

# KSM control scripts
Source4: ksm.service
Source5: ksm.sysconfig
Source6: ksmctl.c
Source7: ksmtuned.service
Source8: ksmtuned
Source9: ksmtuned.conf

Source10: qemu-guest-agent.service
Source11: 99-qemu-guest-agent.rules

# Non upstream build fix
#Patch1: 0001-mips-Fix-link-error-with-piix4_pm_init.patch

# Add ./configure --disable-kvm-options
# keep: Carrying locally until qemu-kvm is fully merged into qemu.git
Patch2: 0002-configure-Add-disable-kvm-options.patch

# The infamous chardev flow control patches
Patch101: 0101-char-Split-out-tcp-socket-close-code-in-a-separate-f.patch
Patch102: 0102-char-Add-a-QemuChrHandlers-struct-to-initialise-char.patch
Patch103: 0103-iohandlers-Add-enable-disable_write_fd_handler-funct.patch
Patch104: 0104-char-Add-framework-for-a-write-unblocked-callback.patch
Patch105: 0105-char-Update-send_all-to-handle-nonblocking-chardev-w.patch
Patch106: 0106-char-Equip-the-unix-tcp-backend-to-handle-nonblockin.patch
Patch107: 0107-char-Throttle-when-host-connection-is-down.patch
Patch108: 0108-virtio-console-Enable-port-throttling-when-chardev-i.patch
Patch109: 0109-spice-qemu-char.c-add-throttling.patch
Patch110: 0110-spice-qemu-char.c-remove-intermediate-buffer.patch
Patch111: 0111-usb-redir-Add-flow-control-support.patch
Patch112: 0112-virtio-serial-bus-replay-guest_open-on-migration.patch
Patch113: 0113-char-Disable-write-callback-if-throttled-chardev-is-.patch

# Spice features from upstream master: seamless migration & dynamic monitors
Patch201: 0201-spice-abort-on-invalid-streaming-cmdline-params.patch
Patch202: 0202-spice-notify-spice-server-on-vm-start-stop.patch
Patch203: 0203-spice-notify-on-vm-state-change-only-via-spice_serve.patch
Patch204: 0204-spice-migration-add-QEVENT_SPICE_MIGRATE_COMPLETED.patch
Patch205: 0205-spice-add-migrated-flag-to-spice-info.patch
Patch206: 0206-spice-adding-seamless-migration-option-to-the-comman.patch
Patch207: 0207-spice-increase-the-verbosity-of-spice-section-in-qem.patch
Patch208: 0208-qxl-update_area_io-guest_bug-on-invalid-parameters.patch
Patch209: 0209-qxl-disallow-unknown-revisions.patch
Patch210: 0210-qxl-add-QXL_IO_MONITORS_CONFIG_ASYNC.patch
Patch211: 0211-configure-print-spice-protocol-and-spice-server-vers.patch
Patch212: 0212-spice-make-number-of-surfaces-runtime-configurable.patch
Patch213: 0213-qxl-Add-set_client_capabilities-interface-to-QXLInte.patch
Patch214: 0214-Remove-ifdef-QXL_COMMAND_FLAG_COMPAT_16BPP.patch
Patch215: 0215-spice-switch-to-queue-for-vga-mode-updates.patch
Patch216: 0216-spice-split-qemu_spice_create_update.patch
Patch217: 0217-spice-add-screen-mirror.patch
Patch218: 0218-spice-send-updates-only-for-changed-screen-content.patch
Patch219: 0219-qxl-dont-update-invalid-area.patch
Patch220: 0220-qxl-Ignore-set_client_capabilities-pre-post-migrate.patch
Patch221: 0221-qxl-better-cleanup-for-surface-destroy.patch
Patch222: 0222-hw-qxl-tracing-fixes.patch
Patch223: 0223-qxl-add-trace-event-for-QXL_IO_LOG.patch
Patch224: 0224-hw-qxl-support-client-monitor-configuration-via-devi.patch
Patch225: 0225-qxl-always-update-displaysurface-on-resize.patch
Patch226: 0226-qxl-update_area_io-cleanup-invalid-parameters-handli.patch
Patch227: 0227-qxl-fix-range-check-for-rev3-io-commands.patch

# Ugh, ton of USB bugfixes / preparation patches for usb-redir
# live-migration which did not make 1.2.0 :|
# All are in upstream master so can be dropped next qemu release
Patch0301: 0301-usb-controllers-do-not-need-to-check-for-babble-them.patch
Patch0302: 0302-usb-core-Don-t-set-packet-state-to-complete-on-a-nak.patch
Patch0303: 0303-usb-core-Add-a-usb_ep_find_packet_by_id-helper-funct.patch
Patch0304: 0304-usb-core-Allow-the-first-packet-of-a-pipelined-ep-to.patch
Patch0305: 0305-Revert-ehci-don-t-flush-cache-on-doorbell-rings.patch
Patch0306: 0306-ehci-Validate-qh-is-not-changed-unexpectedly-by-the-.patch
Patch0307: 0307-ehci-Update-copyright-headers-to-reflect-recent-work.patch
Patch0308: 0308-ehci-Properly-cleanup-packets-on-cancel.patch
Patch0309: 0309-ehci-Properly-report-completed-but-not-yet-processed.patch
Patch0310: 0310-ehci-check-for-EHCI_ASYNC_FINISHED-first-in-ehci_fre.patch
Patch0311: 0311-ehci-trace-guest-bugs.patch
Patch0312: 0312-ehci-add-doorbell-trace-events.patch
Patch0313: 0313-ehci-Add-some-additional-ehci_trace_guest_bug-calls.patch
Patch0314: 0314-ehci-Fix-memory-leak-in-handling-of-NAK-ed-packets.patch
Patch0315: 0315-ehci-Handle-USB_RET_PROCERR-in-ehci_fill_queue.patch
Patch0316: 0316-ehci-Correct-a-comment-in-fetchqtd-packet-processing.patch
Patch0317: 0317-usb-redir-Never-return-USB_RET_NAK-for-async-handled.patch
Patch0318: 0318-usb-redir-Don-t-delay-handling-of-open-events-to-a-b.patch
Patch0319: 0319-usb-redir-Get-rid-of-async-struct-get-member.patch
Patch0320: 0320-usb-redir-Get-rid-of-local-shadow-copy-of-packet-hea.patch
Patch0321: 0321-usb-redir-Get-rid-of-unused-async-struct-dev-member.patch
Patch0322: 0322-usb-redir-Move-to-core-packet-id-and-queue-handling.patch
Patch0323: 0323-usb-redir-Return-babble-when-getting-more-bulk-data-.patch
Patch0324: 0324-usb-redir-Convert-to-new-libusbredirparser-0.5-API.patch
Patch0325: 0325-usb-redir-Set-ep-max_packet_size-if-available.patch
Patch0326: 0326-usb-redir-Add-a-usbredir_reject_device-helper-functi.patch
Patch0327: 0327-usb-redir-Ensure-our-peer-has-the-necessary-caps-whe.patch
Patch0328: 0328-usb-redir-Enable-pipelining-for-bulk-endpoints.patch
Patch0329: 0329-Better-name-usb-braille-device.patch
Patch0330: 0330-usb-audio-fix-usb-version.patch
Patch0331: 0331-xhci-rip-out-background-transfer-code.patch
Patch0332: 0332-xhci-drop-buffering.patch
Patch0333: 0333-xhci-move-device-lookup-into-xhci_setup_packet.patch
Patch0334: 0334-xhci-implement-mfindex.patch
Patch0335: 0335-xhci-iso-xfer-support.patch
Patch0336: 0336-xhci-trace-cc-codes-in-cleartext.patch
Patch0337: 0337-xhci-add-trace_usb_xhci_ep_set_dequeue.patch
Patch0338: 0338-xhci-fix-runtime-write-tracepoint.patch
Patch0339: 0339-xhci-update-register-layout.patch
Patch0340: 0340-xhci-update-port-handling.patch
Patch0341: 0341-usb3-superspeed-descriptors.patch
Patch0342: 0342-usb3-superspeed-endpoint-companion.patch
Patch0343: 0343-usb3-bos-decriptor.patch
Patch0344: 0344-usb-storage-usb3-support.patch
Patch0345: 0345-xhci-fix-cleanup-msi.patch
Patch0346: 0346-xhci-rework-interrupt-handling.patch
Patch0347: 0347-xhci-add-msix-support.patch
Patch0348: 0348-xhci-move-register-update-into-xhci_intr_raise.patch
Patch0349: 0349-xhci-add-XHCIInterrupter.patch
Patch0350: 0350-xhci-prepare-xhci_runtime_-read-write-for-multiple-i.patch
Patch0351: 0351-xhci-pick-target-interrupter.patch
Patch0352: 0352-xhci-support-multiple-interrupters.patch
Patch0353: 0353-xhci-kill-xhci_mem_-read-write-dispatcher-functions.patch
Patch0354: 0354-xhci-allow-bytewise-capability-register-reads.patch
Patch0355: 0355-usb-host-allow-emulated-non-async-control-requests-w.patch
Patch0356: 0356-ehci-switch-to-new-style-memory-ops.patch
Patch0357: 0357-ehci-Fix-interrupts-stopping-when-Interrupt-Threshol.patch
Patch0358: 0358-ehci-Don-t-process-too-much-frames-in-1-timer-tick-v.patch
Patch0359: 0359-configure-usbredir-fixes.patch
Patch0360: 0360-ehci-Don-t-set-seen-to-0-when-removing-unseen-queue-.patch
Patch0361: 0361-ehci-Walk-async-schedule-before-and-after-migration.patch
Patch0362: 0362-usb-redir-Change-cancelled-packet-code-into-a-generi.patch
Patch0363: 0363-usb-redir-Add-an-already_in_flight-packet-id-queue.patch
Patch0364: 0364-usb-redir-Store-max_packet_size-in-endp_data.patch
Patch0365: 0365-usb-redir-Add-support-for-migration.patch
Patch0366: 0366-usb-redir-Add-chardev-open-close-debug-logging.patch
Patch0367: 0367-usb-redir-Revert-usb-redir-part-of-commit-93bfef4c.patch
Patch0368: 0368-uhci-Don-t-queue-up-packets-after-one-with-the-SPD-f.patch
# And the last few ehci fixes + the actual usb-redir live migration code
# Not yet upstream but should get there real soon
Patch0369: 0369-ehci-Fix-interrupt-packet-MULT-handling.patch
Patch0370: 0370-usb-redir-Adjust-pkg-config-check-for-usbredirparser.patch
Patch0371: 0371-usb-redir-Change-usbredir_open_chardev-into-usbredir.patch
Patch0372: 0372-usb-redir-Don-t-make-migration-fail-in-none-seamless.patch

# Revert c3767ed0eb5d0.
# NOT upstream (hopefully will be soon).
# See: https://bugzilla.redhat.com/show_bug.cgi?id=853408
# and: https://lists.gnu.org/archive/html/qemu-devel/2012-09/msg00526.html
# plus followups.
Patch0900: 0001-Revert-qemu-char-Re-connect-for-tcp_chr_write-unconn.patch


Source100:	qemu.rpmlintrc

License:	GPLv2+ and LGPLv2+ and BSD
URL:		http://wiki.qemu.org/Main_Page
Group:		Emulators
%rename		kvm
Requires:	qemu-img = %{EVRD}
Requires:	libcacard-tools
# for %%{_sysconfdir}/sasl2
Requires:	cyrus-sasl
Requires:	vgabios >= 0.6c
Requires:	seabios-bin >= 0.6.0-1
Requires:	sgabios-bin
Requires:	ipxe-roms-qemu

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
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libcap-ng)
BuildRequires:	pkgconfig(spice-server)
BuildRequires:	pkgconfig(spice-protocol)
#BuildRequires:	pkgconfig(libcacard)
BuildRequires:	pkgconfig(libseccomp)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(libusbredirhost) >=0.5.2
BuildRequires:	usbredir-devel >= 0.5.2
BuildRequires:	libtool
BuildRequires:	xfsprogs-devel
BuildRequires:	texinfo
BuildRequires:	systemtap
# not in main
#BuildRequires:	vde-devel
BuildRequires:	dev86
BuildRequires:	iasl

#not ready yet
#%if %{with fdt}
# For FDT device tree support
#BuildRequires: libfdt-devel
#%endif
#%if %{with rbd}
## For rbd block driver
#BuildRequires: ceph-devel
#%endif

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
%apply_patches

%build
#(proyvind): binutils upstream bug #10862, linking with gold fails if doing parallel build
mkdir -p bfd
ln -s %{_bindir}/ld.bfd bfd/ld
export PATH=$PWD/bfd:$PATH
buildarch="i386-softmmu x86_64-softmmu arm-softmmu cris-softmmu \
    m68k-softmmu mips-softmmu mipsel-softmmu mips64-softmmu \
    mips64el-softmmu sh4-softmmu sh4eb-softmmu sparc-softmmu sparc64-softmmu \
    ppc-softmmu ppcemb-softmmu ppc64-softmmu \
    i386-linux-user x86_64-linux-user alpha-linux-user arm-linux-user \
    armeb-linux-user cris-linux-user m68k-linux-user mips-linux-user \
    mipsel-linux-user ppc-linux-user ppc64-linux-user \
    ppc64abi32-linux-user sh4-linux-user sh4eb-linux-user \
    sparc-linux-user sparc64-linux-user sparc32plus-linux-user"
%if %{with x86only}
    buildarch="i386-softmmu x86_64-softmmu i386-linux-user x86_64-linux-user"
%endif

# Targets we don't build as of qemu 1.1.50
# alpha-softmmu lm32-softmmu microblaze-softmmu microblazeel-softmmu
# or32-softmmu s390x-softmmu xtensa-softmmu xtensaeb-softmmu unicore32-softmmu
# alpha-linux-user microblaze-linux-user microblazeel-linux-user
# or32-linux-user unicore32-linux-user s390x-linux-user


# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

%ifarch s390
# drop -g flag to prevent memory exhaustion by linker
%global optflags %(echo %{optflags} | sed 's/-g//')
sed -i.debug 's/"-g $CFLAGS"/"$CFLAGS"/g' configure
%endif


dobuild() {
    ./configure \
        --prefix=%{_prefix} \
        --sysconfdir=%{_sysconfdir} \
        --interp-prefix=%{_prefix}/qemu-%%M \
        --audio-drv-list=pa,sdl,alsa,oss \
        --disable-strip \
        --extra-ldflags="$extraldflags -pie -Wl,-z,relro -Wl,-z,now" \
        --extra-cflags="%{optflags} -fPIE -DPIE" \
%ifarch %{ix86} x86_64
        --enable-spice \
        --enable-mixemu \
        --enable-seccomp \
%endif
%if %{without rbd}
        --disable-rbd \
%endif
%if %{without fdt}
        --disable-fdt \
%endif
        --enable-trace-backend=dtrace \
        --disable-werror \
        --disable-xen \
        --enable-kvm \
	--disable-smartcard \
        "$@"

    echo "config-host.mak contents:"
    echo "==="
    cat config-host.mak
    echo "==="

    make V=1 %{?_smp_mflags} $buildldflags
}

# This is kind of confusing. We run ./configure + make twice here to
# preserve some back compat: if on x86, we want to provide a qemu-kvm
# binary that defaults to KVM=on. All other qemu-system* should be
# able to use KVM, but default to KVM=off (upstream qemu semantics).
#
# Once qemu-kvm and qemu fully merge, and we base off qemu releases,
# all qemu-system-* will default to KVM=off, so we hopefully won't need
# to do these double builds. But then I'm not sure how we are going to
# generate a back compat qemu-kvm binary...

%ifarch %{ix86} x86_64
# Build qemu-kvm back compat binary
dobuild --target-list=x86_64-softmmu

# Setup back compat qemu-kvm binary which defaults to KVM=on
./scripts/tracetool.py --backend dtrace --format stap \
  --binary %{_bindir}/qemu-kvm --target-arch x86_64 --target-type system \
  --probe-prefix qemu.kvm < ./trace-events > qemu-kvm.stp
cp -a x86_64-softmmu/qemu-system-x86_64 qemu-kvm
make clean
%endif

# Build qemu-system-* with consistent default of kvm=off
dobuild --target-list="$buildarch" --disable-kvm-options
gcc %{SOURCE6} -O2 -g -o ksmctl

%install

install -D -p -m 0755 %{SOURCE4} %{buildroot}/%{_unitdir}/ksm.service
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl %{buildroot}/lib/systemd/ksmctl

install -D -p -m 0755 %{SOURCE7} %{buildroot}/%{_unitdir}/ksmtuned.service
install -D -p -m 0755 %{SOURCE8} %{buildroot}%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE9} %{buildroot}%{_sysconfdir}/ksmtuned.conf

%ifarch %{ix86} x86_64
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/modules
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_udevdir}
mkdir -p %{buildroot}%{_datadir}/systemtap/tapset

install -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 scripts/kvm/kvm_stat %{buildroot}%{_bindir}/
install -m 0755 qemu-kvm %{buildroot}%{_bindir}/
install -m 0644 qemu-kvm.stp %{buildroot}%{_datadir}/systemtap/tapset/
install -m 0644 %{SOURCE3} %{buildroot}%{_udevdir}
%endif

make DESTDIR=%{buildroot} install
chmod -x %{buildroot}%{_mandir}/man1/*
install -D -p -m 0644 -t %{buildroot}%{qemudocdir} Changelog README TODO COPYING COPYING.LIB LICENSE

install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

# Provided by package ipxe
rm -rf %{buildroot}%{_datadir}/%{name}/pxe*rom
# Provided by package vgabios
rm -rf %{buildroot}%{_datadir}/%{name}/vgabios*bin
# Provided by package seabios
rm -rf %{buildroot}%{_datadir}/%{name}/bios.bin
# Provided by package sgabios
rm -rf %{buildroot}%{_datadir}/%{name}/sgabios.bin
# Provided by package openbios
#needed this:
#BuildRequires:  gcc-powerpc64-linux-gnu
#BuildRequires:  gcc-sparc64-linux-gnu
#rm -rf %{buildroot}%{_datadir}/%{name}/openbios-ppc
#rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc32
#rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc64
# Provided by package SLOF
#gcc-powerpc64-linux-gnu needed
#rm -rf % {buildroot} % {_datadir}/% {name}/slof.bin

# remove unpackaged files on x86only:
%if %{with x86only}
rm -f %{buildroot}%{_datadir}/%{name}/bamboo.dtb
rm -f %{buildroot}%{_datadir}/%{name}/ppc_rom.bin
rm -f %{buildroot}%{_datadir}/%{name}/spapr-rtas.bin
%endif

# The following aren't provided by any Fedora package

# Used by target s390/s390x
#rm -rf %{buildroot}%{_datadir}/%{name}/s390-zipl.rom
#rm -rf %{buildroot}%{_datadir}/%{name}/palcode-clipper
# Binary device trees for microblaze target
#rm -rf %{buildroot}%{_datadir}/%{name}/petalogix*.dtb


# the pxe gpxe images will be symlinks to the images on
# /usr/share/ipxe, as QEMU doesn't know how to look
# for other paths, yet.
pxe_link() {
  ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/%{name}/pxe-$1.rom
}

pxe_link e1000 8086100e
pxe_link ne2k_pci 10ec8029
pxe_link pcnet 10222000
pxe_link rtl8139 10ec8139
pxe_link virtio 1af41000

rom_link() {
    ln -s $1 %{buildroot}%{_datadir}/%{name}/$2
}

rom_link ../vgabios/VGABIOS-lgpl-latest.bin vgabios.bin
rom_link ../vgabios/VGABIOS-lgpl-latest.cirrus.bin vgabios-cirrus.bin
rom_link ../vgabios/VGABIOS-lgpl-latest.qxl.bin vgabios-qxl.bin
rom_link ../vgabios/VGABIOS-lgpl-latest.stdvga.bin vgabios-stdvga.bin
rom_link ../vgabios/VGABIOS-lgpl-latest.vmware.bin vgabios-vmware.bin
rom_link ../seabios/bios.bin bios.bin
rom_link ../sgabios/sgabios.bin sgabios.bin

mkdir -p %{buildroot}%{_exec_prefix}/lib/binfmt.d
for i in dummy \
%ifnarch %{ix86} x86_64
    qemu-i386 \
%endif
%if %{without x86only}
%ifnarch alpha
    qemu-alpha \
%endif
%ifnarch arm
    qemu-arm \
%endif
    qemu-armeb \
%ifnarch mips
    qemu-mips qemu-mipsn32 qemu-mips64 \
%endif
%ifnarch mipsel
    qemu-mipsel qemu-mipsn32el qemu-mips64el \
%endif
%ifnarch m68k
    qemu-m68k \
%endif
%ifnarch ppc ppc64
    qemu-ppc \
%endif
%ifnarch sparc sparc64
    qemu-sparc \
%endif
%ifnarch s390 s390x
    qemu-s390x \
%endif
%ifnarch sh4
    qemu-sh4 \
%endif
    qemu-sh4eb \
%endif
; do
  test $i = dummy && continue
  grep /$i:\$ %{SOURCE1} > %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i.conf
  chmod 644 %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i.conf
done < %{SOURCE1}

# For the qemu-guest-agent subpackage install the systemd
# service and udev rules.
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_udevdir}
install -m 0644 %{SOURCE10} %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE11} %{buildroot}%{_udevdir}


%post 
%ifarch %{ix86} x86_64
sh %{_sysconfdir}/sysconfig/modules/kvm.modules || :
udevadm trigger --sysname-match=kvm || :
%endif

%_post_service ksmtuned.service
%_post_service ksm.service
%_post_service qemu-guest-agent.service

%preun
%_preun_service ksm.service
%_preun_service ksmtuned.service
%_preun_service qemu-guest-agent.service

%triggerpostun -- qemu < 0.10.4-6
rm -f /etc/rc.d/*/{K,S}??qemu

%files
%doc README qemu-doc.html qemu-tech.html
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
%{_unitdir}/ksm.service
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%{_unitdir}/ksmtuned.service
%{_sbindir}/ksmtuned
%{_unitdir}/qemu-guest-agent.service
%{_udevdir}/99-qemu-guest-agent.rules
%{_udevdir}/80-kvm.rules
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
%{_bindir}/qemu-system-sparc64
%{_bindir}/qemu-system-x86_64
#% {_bindir}/qmp-shell
#conflicts with cacard-tools
#% {_bindir}/vscclient
%{_bindir}/virtfs-proxy-helper
/lib/systemd/ksmctl
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
#%{_datadir}/qemu/mpc8544ds.dtb
%{_datadir}/qemu/palcode-clipper
%{_datadir}/qemu/petalogix-ml605.dtb
%{_datadir}/qemu/petalogix-s3adsp1800.dtb
%{_datadir}/qemu/qemu-icon.bmp

%{_datadir}/systemtap/tapset/qemu-alpha.stp
%{_datadir}/systemtap/tapset/qemu-arm.stp
%{_datadir}/systemtap/tapset/qemu-armeb.stp
%{_datadir}/systemtap/tapset/qemu-cris.stp
%{_datadir}/systemtap/tapset/qemu-m68k.stp
%{_datadir}/systemtap/tapset/qemu-mips.stp
%{_datadir}/systemtap/tapset/qemu-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-ppc.stp
%{_datadir}/systemtap/tapset/qemu-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-ppc64abi32.stp
%{_datadir}/systemtap/tapset/qemu-sh4.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb.stp
%{_datadir}/systemtap/tapset/qemu-sparc.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus.stp
%{_datadir}/systemtap/tapset/qemu-sparc64.stp
#%{_datadir}/systemtap/tapset/qemu-kvm.stp
%{_datadir}/systemtap/tapset/qemu-system-i386.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64.stp
%{_datadir}/systemtap/tapset/qemu-system-mips.stp
%{_datadir}/systemtap/tapset/qemu-system-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64el.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64.stp
%{_datadir}/systemtap/tapset/qemu-system-m68k.stp
%{_datadir}/systemtap/tapset/qemu-system-cris.stp
%{_datadir}/systemtap/tapset/qemu-system-sh4.stp
%{_datadir}/systemtap/tapset/qemu-system-sh4eb.stp
%{_datadir}/systemtap/tapset/qemu-system-sparc.stp
%{_datadir}/systemtap/tapset/qemu-system-sparc64.stp
%{_datadir}/systemtap/tapset/qemu-system-ppc.stp
%{_datadir}/systemtap/tapset/qemu-system-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-system-ppcemb.stp
%{_datadir}/systemtap/tapset/qemu-system-arm.stp
%{_datadir}/systemtap/tapset/qemu-kvm.stp
%{_datadir}/systemtap/tapset/qemu-x86_64.stp
%{_datadir}/systemtap/tapset/qemu-i386.stp

%{_exec_prefix}/lib/binfmt.d/qemu-*.conf

#% {py_platsitedir}/qmp.py

%files img
%{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*
