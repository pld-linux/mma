Summary:	MMA - Musical MIDI Accompaniment
Name:		mma
Version:	16.06
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://www.mellowood.ca/mma/%{name}-bin-%{version}.tar.gz
# Source0-md5:	a7e34ec1b9c2ffc36f408314bb184615
URL:		http://www.mellowood.ca/mma/downloads.html
BuildRequires:	python3-modules
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
Requires:	python3-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MMA — Musical MIDI Accompaniment is an accompaniment generator. It
creates MIDI tracks for a soloist to perform over from a user supplied
file containing chords and MMA directives.

MMA is very versatile and generates excellent tracks. It comes with an
extensive user-extendable library with a variety of patterns for
various popular rhythms, detailed user manuals, and several demo
songs.

MMA is a command line driven program. It creates MIDI files which are
then played by a sequencer or MIDI file play program.

%prep
%setup -q -n %{name}-bin-%{version}

# force our Python 3 for scripts
%{__sed} -i -e '1s,^#!.*python,#!%{__python3},' mma.py mma-* util/*.py

# remove files compiled upstream
find . -name '*.py[co]' | xargs rm

%build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_datadir}/mma,%{_bindir},%{_mandir}/man{1,8}/*,%{_examplesdir}}

cp -p mma.py mma-* $RPM_BUILD_ROOT%{_datadir}/mma
cp -a MMA includes lib plugins util $RPM_BUILD_ROOT%{_datadir}/mma

ln -sf %{_datadir}/mma/mma.py $RPM_BUILD_ROOT%{_bindir}/mma
for n in gb libdoc renum splitrec ; do
    ln -sf %{_datadir}/mma/mma-$n $RPM_BUILD_ROOT%{_bindir}
done

cp -a egs $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
ln -s %{_examplesdir}/%{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/mma/egs

cp -a docs/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a docs/man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

rm $RPM_BUILD_ROOT%{_datadir}/mma/util/README.*

%py3_comp $RPM_BUILD_ROOT%{_datadir}/mma/MMA
%py3_comp $RPM_BUILD_ROOT%{_datadir}/mma/plugins

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/mma -G || :

%files
%defattr(644,root,root,755)
%doc docs/html/{chords,lib,logo.png,mma.html,plugins,ref,tut,tut-french}
%doc text/* util/README.*
%attr(755,root,root) %{_bindir}/mma
%attr(755,root,root) %{_bindir}/mma-*
%dir %{_datadir}/mma
%attr(755,root,root) %{_datadir}/mma/mma.py
%attr(755,root,root) %{_datadir}/mma/mma-*
%dir %{_datadir}/mma/util
%attr(755,root,root) %{_datadir}/mma/util/*.py
%{_datadir}/mma/egs
%{_datadir}/mma/includes
%{_datadir}/mma/lib
%{_datadir}/mma/MMA
%{_datadir}/mma/plugins
%{_mandir}/man1/*.1*
%{_mandir}/man8/*.8*
%{_examplesdir}/%{name}-%{version}
