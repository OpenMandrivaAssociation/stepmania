%define	distname	StepMania

%define build_mp3 1
%{?_with_mp3: %global build_mp3 1}
%{?_without_mp3: %global build_mp3 0}

Summary:	A rythm game
Name:		stepmania
Version:	3.9
Release:	15
License:	MIT
Url:		http://www.stepmania.com/wiki/Downloads
Group:		Games/Arcade
Source0:	%{distname}-%{version}-src.tar.bz2
Patch0:         StepMania-3.9-x86_64-build.patch
Patch1:		StepMania-3.9-build_crypto.patch
Patch3:		StepMania-3.9-home.patch
Patch4:		StepMania-3.9-pkgdir.patch
Patch5:		StepMania-3.9-eventmask.patch
Patch6:		StepMania-3.9-extraqual.patch
Patch7:		StepMania-3.9-replace-this.patch
Patch8:		StepMania-3.9-src-gettid.patch
Patch9:		stepmania-3.9-ffmpeg-all-4.patch
Patch10:	stepmania-3.9-ffmpeg-headers.patch
Patch11:	stepmania-3.9-ffmpeg-pixfmt.patch
Patch12:	stepmania-3.9-select_style.patch
Patch13:	stepmania-3.9-gcc43.patch
Patch14:	stepmania-3.9-fix-str-fmt.patch
Patch15:	stepmania-3.9-libpng15.patch
Patch16:	stepmania-gcc46.patch
Patch17:	stepmania-gcc47.patch

BuildRequires:  ffmpeg-devel
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  jpeg-devel
BuildRequires:  pkgconfig(sdl)
BuildRequires:  lua5.0-devel
BuildRequires:	pkgconfig(glu)
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
%patch3 -p1 -b .home
%patch4 -p1 -b .pkgdir
%patch5 -p1 -b .eventmask
%patch6 -p1 -b .extraqual
%patch7 -p1 -b .replace
%patch8 -p1 -b .gettid
%patch9 -p1 -b .ffmpeg-4
%patch10 -p1 -b .ffmpeg-headers
%patch11 -p1 -b .ffmpeg-pixfmt
%patch12 -p1 -b .select-style
%patch13 -p1 -b .gcc
%patch14 -p1 -b .str
%patch15 -p0 -b .libpng
%patch16 -p1 -b .gcc
%patch17 -p1 -b .gcc

%build
export CFLAGS="%{optflags} -O1"
export CXXFLAGS="%{optflags} -O1 -fpermissive"
%configure2_5x \
  --disable-dependency-tracking \
  --bindir=%{_gamesbindir} \
  --datadir=%{_gamesdatadir} \
  --disable-gtktest --disable-gtk2 \
%if %build_mp3
  --with-mp3
%else
  --without-mp3
%endif

%make

%install
%makeinstall_std
install -d -m 0755 -p %{buildroot}%{_iconsdir}
install -m 0644 %{_topdir}/BUILD/%{distname}-%{version}-src/src/%{distname}.xpm %{buildroot}%{_iconsdir}/

install -d -m 0755 -p %{buildroot}%{_datadir}/applications
cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_gamesbindir}/stepmania
Name=StepMania
Comment=A rythm game
Icon=%{distname}
Categories=Game;ArcadeGame;
EOF

%clean

%files
%doc README-FIRST.html NEWS
%{_gamesbindir}/%{name}
%{_iconsdir}/%{distname}.xpm
%{_datadir}/applications/mandriva-*.desktop
