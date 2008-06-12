%define	distname	StepMania
%define	name	stepmania
%define	version	3.9
%define release	%mkrel 9

%define build_mp3 1
%{?_with_mp3: %global build_mp3 1}
%{?_without_mp3: %global build_mp3 0}

Summary:	A rythm game
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Url:		http://www.stepmania.com/wiki/Downloads
Group:		Games/Arcade
Source0:	%{distname}-%{version}-src.tar.bz2
Patch0:         StepMania-3.9-x86_64-build.patch
Patch1:		StepMania-3.9-build_crypto.patch
Patch2:		StepMania-3.9-ffmpeg_4629_4754.patch
Patch3:		StepMania-3.9-home.patch
Patch4:		StepMania-3.9-pkgdir.patch
Patch5:		StepMania-3.9-eventmask.patch
Patch6:		StepMania-3.9-extraqual.patch
Patch7:		StepMania-3.9-replace-this.patch
Patch8:		StepMania-3.9-src-gettid.patch
Patch9:		StepMania-3.9-src-averror.patch
Patch10:	StepMania-3.9-src-int64_c.patch
Patch11:	StepMania-3.9-src-avcodec_namespace.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  ffmpeg-devel	
BuildRequires:  oggvorbis-devel
BuildRequires:  jpeg-devel
BuildRequires:  SDL-devel
BuildRequires:  lua5.0-devel
BuildRequires:	gtk2-devel
BuildRequires:	MesaGLU-devel
%if %{build_mp3}
BuildRequires:	mad-devel
%endif
Requires:	%{name}-data

%description
StepMania is a music/rhythm game. The player presses different buttons in time 
to the music and to note patterns that scroll across the screen. Features 3D 
graphics, visualizations, support for gamepads/dance pads, a step recording 
mode, and more!
To add songs, simply copy the content of your folder containing songs 
to ~/StepMania/Songs as user, or to /usr/share/StepMania/Songs as root.

%prep
%setup -q -n %{distname}-%{version}-src
%patch0 -p1 -b .x86_64
%patch1 -p1 -b .crypto
%patch2 -p1 -b .ffmpeg_4629_4754
%patch3 -p1 -b .home
%patch4 -p1 -b .pkgdir
%patch5 -p1 -b .eventmask
%patch6 -p1 -b .extraqual
%patch7 -p1 -b .replace
%patch8 -p1 -b .gettid
%patch9 -p1 -b .averror
%patch10 -p1 -b .int64_c
%patch11 -p1 -b .avcodec_namespace

%build
%configure \
  --bindir=%{_gamesbindir} \
  --datadir=%{_gamesdatadir} \
%if %build_mp3
  --with-mp3
%else
  --without-mp3
%endif

%make

%install
rm -rf %buildroot
%makeinstall_std
install -d -m 0755 -p $RPM_BUILD_ROOT%{_iconsdir}
install -m 0644 %{_topdir}/BUILD/%{distname}-%{version}-src/src/%{distname}.xpm $RPM_BUILD_ROOT%{_iconsdir}/

install -d -m 0755 -p $RPM_BUILD_ROOT%{_libdir}/%{distname}
mv $RPM_BUILD_ROOT%{_gamesbindir}/GtkModule.so $RPM_BUILD_ROOT%{_libdir}/%{distname}/
chmod 0644 $RPM_BUILD_ROOT%{_libdir}/%{distname}/GtkModule.so

install -d -m 0755 -p $RPM_BUILD_ROOT%{_datadir}/applications
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=soundwrapper %{_gamesbindir}/stepmania
Name=StepMania
Comment=A rythm game
Icon=%{distname}
Categories=Game;ArcadeGame;
EOF

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=StepMania
Comment=A rythm game
Exec=soundwrapper %_gamesbindir/%{name}
Icon=%{distname}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files
%doc README-FIRST.html NEWS
%defattr(-,root,root)
%{_gamesbindir}/%{name}
%{_libdir}/%{distname}/GtkModule.so
%{_iconsdir}/%{distname}.xpm
%{_datadir}/applications/mandriva-*.desktop
%{_datadir}/applications/mandriva-%{name}.desktop


