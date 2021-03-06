Name:           acpid
Version:        2.0.22
Release:        0
License:        GPL-2.0+
Summary:        Executes Actions at ACPI Events
Url:            http://sourceforge.net/projects/acpid2
Group:          Base/Hardware Adaptation
Source:         http://sourceforge.net/projects/acpid2/files/%{name}-%{version}.tar.gz
Source4:        thinkpad_acpi.modprobe
Source5:        events.power_button
Source9:        events.thinkpad
Source6:        thinkpad_handler
Source7:        power_button
Source8:        acpid.service
Source1001:     acpid.manifest
BuildRequires:  systemd
ExclusiveArch:  %ix86 x86_64 ia64

%description
ACPID is a completely flexible, totally extensible daemon for
delivering ACPI events. It listens to a file (/proc/acpi/event) and,
when an event occurs, executes programs to handle the event. The start
script loads all needed modules.

Configure it in /etc/sysconfig/powermanagement.

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE9} .

%build
export LDFLAGS="-Wl,-z,relro,-z,now"
%configure 
%__make OPT="%{optflags}" %{?_smp_mflags}

%install
%make_install SBINDIR=%{_sbindir}
install -Dm 644 thinkpad_acpi.modprobe %{buildroot}%{_sysconfdir}/modprobe.d/50-thinkpad_acpi.conf
install -Dm 744 thinkpad_handler %{buildroot}%{_prefix}/lib/acpid/thinkpad_handler
install -Dm 744 power_button %{buildroot}%{_prefix}/lib/acpid/power_button
install -Dm 644 events.power_button %{buildroot}%{_sysconfdir}/acpi/events/power_button
install -Dm 644 events.thinkpad %{buildroot}%{_sysconfdir}/acpi/events/thinkpad
mkdir -p %{buildroot}/%{_unitdir}
install -m 644 %{SOURCE8} %{buildroot}/%{_unitdir}

# keep the logfile
install -dm 755 %{buildroot}%{_localstatedir}/log
touch %{buildroot}%{_localstatedir}/log/acpid


%docs_package

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%dir %{_sysconfdir}/modprobe.d
%dir %{_sysconfdir}/acpi
%dir %{_sysconfdir}/acpi/events
%{_sysconfdir}/acpi/events/thinkpad
%{_sysconfdir}/acpi/events/power_button
%{_prefix}/lib/acpid
%{_sysconfdir}/modprobe.d/50-thinkpad_acpi.conf
%_unitdir/%{name}.service
%{_sbindir}/kacpimon
%{_sbindir}/acpid
%{_bindir}/acpi_listen
%ghost %config(noreplace,missingok) %{_localstatedir}/log/acpid
