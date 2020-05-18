# TODO: Linux 2.6 port of drivers (some work started somewhere by vapier?)
Summary:	Linux drivers for Creative Labs DXR2 devices
Summary(pl.UTF-8):	Sterowniki linuksowe do urządzeń Creative Labs DXR2
Name:		dxr2-driver
Version:	1.0.4
Release:	4
License:	GPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/dxr2/%{name}-%{version}.tar.gz
# Source0-md5:	d31c9513bf1e6901ab459f08c2c14424
# from dxr2install-0.5
Patch0:		%{name}-subtitles.patch
URL:		http://dxr2.sourceforge.net/
BuildRequires:	libdvdread-devel
BuildRequires:	ncurses-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# needs on external print_info() function
%define		skip_post_check_so	libdxr2css.so.*

%description
Linux drivers for Creative Labs DXR2 devices.

%description -l pl.UTF-8
Sterowniki linuksowe do urządzeń Creative Labs DXR2.

%package devel
Summary:	Header files for Creative Labs DXR2 devices
Summary(pl.UTF-8):	Pliki nagłówkowe dla urządzeń Creative Labs DXR2
Group:		Development/Libraries

%description devel
Header files for Creative Labs DXR2 devices.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla urządzeń Creative Labs DXR2.

%package -n dxr2-player
Summary:	DXR2-powered DVD player
Summary(pl.UTF-8):	Odtwarzacz DVD dla kart DXR2
Group:		Applications/Multimedia

%description -n dxr2-player
DXR2-powered DVD player.

%description -n dxr2-player -l pl.UTF-8
Odtwarzacz DVD dla kart DXR2.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{__make} \
	DIRS="player" \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -D__DVD_DEBUG -D_LARGEFILE64_SOURCE -D_REENTRANT -I../sysinclude -DNEED_SYS_TYPES_H -I/usr/include/ncurses" \
	X_LIBS="-lXmu -lXt -lX11 -lXext -lXxf86vm"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/dxr2,%{_bindir},%{_libdir}}

cp -p sysinclude/*.h $RPM_BUILD_ROOT%{_includedir}/dxr2
cp -dp player/libdxr2css.so.* $RPM_BUILD_ROOT%{_libdir}
install player/{dvdplay*,driveauth,dvd-sum,*dvd} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n dxr2-player -p /sbin/ldconfig
%postun	-n dxr2-player -p /sbin/ldconfig

%files devel
%defattr(644,root,root,755)
%doc CONTRIBUTORS ChangeLog ReadMe TODO api.html
%attr(755,root,root) %{_includedir}/dxr2

%files -n dxr2-player
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/driveauth
%attr(755,root,root) %{_bindir}/dvd
%attr(755,root,root) %{_bindir}/dvd-sum
%attr(755,root,root) %{_bindir}/dvdplay
%attr(755,root,root) %{_bindir}/dvdplay-curses
%attr(755,root,root) %{_bindir}/dvdplay-wrapper
%attr(755,root,root) %{_bindir}/undvd
%attr(755,root,root) %{_libdir}/libdxr2css.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdxr2css.so.0
