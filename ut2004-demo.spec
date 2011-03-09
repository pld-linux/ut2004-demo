Summary:	Demo for the critically-acclaimed first-person shooter
Name:		ut2004-demo
Version:	3334
Release:	1
License:	as-is
Group:		Applications/Games
Source0:	http://dev.gentoo.org/~tupone/ut2004-lnx-demo%{version}.run
# Source0-md5:	bf9f483902c6006b94c327fb7b585086
Source1:	%{name}.desktop
URL:		http://www.unrealtournament2004.com/
ExclusiveArch:	%{ix86} %{x8664}
%ifarch %{x8664}
Requires:	libSDL-1.2.so.0()(64bit)
Requires:	libopenal.so.1()(64bit)
%else
Requires:	libSDL-1.2.so.0
Requires:	libopenal.so.1
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# ut2004-bin sym versions are rather odd-skip them
# "./libSDL-1.2.so.0" used in linkage, but our deps do are without pathname
%define		_noautoreq		./libSDL-1.2.so.0 ./openal.so
%define		_noautoprov		ut2004-bin %{_noautoreq}
%define		_enable_debug_packages	0

%define		gamelibdir		%{_libdir}/games/%{name}

%description
Unreal Tournament - futuristic FPS game.

%description -l pl.UTF-8
Unreal Tournament - futurystyczna gra FPS.

%prep
%setup -qcT
# simplified version of unpack_makeself
src=%{SOURCE0}
skip=$(grep -a offset=.*head.*wc "$src" | awk '{print $3}' | head -n 1)
skip=$(head -n "$skip" "$src" | wc -c)
dd ibs="$skip" skip=1 if="$src" | tar -xf -

tar xzf setupstuff.tar.gz

install -d lib
tar xjf ut2004demo.tar.bz2 -C lib
%ifarch %{ix86}
tar xjf linux-x86.tar.bz2 -C lib
%endif
%ifarch %{x8664}
tar xjf linux-amd64.tar.bz2 -C lib
%endif

# wrong os
rm lib/System/RunServer.bat

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{gamelibdir},%{_pixmapsdir},%{_desktopdir},%{_bindir}}

cp -a lib/* $RPM_BUILD_ROOT%{gamelibdir}

install -p bin/ut2004-demo $RPM_BUILD_ROOT%{gamelibdir}
ln -s %{gamelibdir}/ut2004-demo $RPM_BUILD_ROOT%{_bindir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -p ut2004.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.xpm

ln -sf %{_libdir}/libopenal.so.1 $RPM_BUILD_ROOT%{gamelibdir}/System/openal.so
ln -sf %{_libdir}/libSDL-1.2.so.0 $RPM_BUILD_ROOT%{gamelibdir}/System/libSDL-1.2.so.0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.linux
%attr(755,root,root) %{_bindir}/ut2004-demo
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.xpm
%dir %{gamelibdir}
%attr(755,root,root) %{gamelibdir}/ut2004-demo
%{gamelibdir}/Animations
%{gamelibdir}/ForceFeedback
%{gamelibdir}/Help
%{gamelibdir}/KarmaData
%{gamelibdir}/Maps
%{gamelibdir}/Music
%{gamelibdir}/Sounds
%{gamelibdir}/Speech
%{gamelibdir}/StaticMeshes
%{gamelibdir}/Textures
%dir %{gamelibdir}/System
%attr(755,root,root) %{gamelibdir}/System/libSDL-1.2.so.0
%attr(755,root,root) %{gamelibdir}/System/openal.so
%attr(755,root,root) %{gamelibdir}/System/ucc-bin
%attr(755,root,root) %{gamelibdir}/System/ut2004-bin
%{gamelibdir}/System/*.dat
%{gamelibdir}/System/*.upl
%{gamelibdir}/System/*.ini
%{gamelibdir}/System/*.u
%{gamelibdir}/System/*.ucl
# maybe drop?
%{gamelibdir}/System/Manifest.smt
%{gamelibdir}/System/Manifest.tmt
%{gamelibdir}/System/Packages.md5
%{gamelibdir}/System/UnrealTournament2004Web.url

# lang resources
%{gamelibdir}/System/*.int
%lang(de) %{gamelibdir}/System/*.det
%lang(ko) %{gamelibdir}/System/*.kot
%lang(es) %{gamelibdir}/System/*.est
%lang(fr) %{gamelibdir}/System/*.frt
%lang(it) %{gamelibdir}/System/*.itt

# web subpackage?
%{gamelibdir}/Web
# drop?
%{gamelibdir}/Benchmark
