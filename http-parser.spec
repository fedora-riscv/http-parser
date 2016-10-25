# we use the upstream version from http_parser.h as the SONAME
%global somajor 2
%global sominor 7
%global sopoint 1

Name:           http-parser
Version:        %{somajor}.%{sominor}.%{sopoint}
Release:        3%{?dist}
Summary:        HTTP request/response parser for C

Group:          System Environment/Libraries
License:        MIT
URL:            http://github.com/joyent/http-parser

Source0:        https://github.com/nodejs/http-parser/archive/v%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Build shared library with SONAME using gyp and remove -O flags so optflags take over
# TODO: do this nicely upstream
Patch1:		http-parser-gyp-sharedlib.patch
Patch2:		http-parser-status.patch

BuildRequires:	gyp

%description
This is a parser for HTTP messages written in C. It parses both requests and
responses. The parser is designed to be used in performance HTTP applications.
It does not make any syscalls nor allocations, it does not buffer data, it can
be interrupted at anytime. Depending on your architecture, it only requires
about 40 bytes of data per message stream (in a web server that is per
connection).


%package devel
Group:          Development/Libraries
Summary:        Development headers and libraries for http-parser
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers and libraries for http-parser.


%prep
%autosetup -n http-parser-%{version}


%build
# TODO: fix -fPIC upstream
export CFLAGS='%{optflags} -fPIC'
gyp -f make --depth=`pwd` http_parser.gyp
make %{?_smp_mflags} BUILDTYPE=Release 


%install
rm -rf %{buildroot}

install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}

install -pm644 http_parser.h %{buildroot}%{_includedir}

#install regular variant
install out/Release/lib.target/libhttp_parser.so.%{somajor} %{buildroot}%{_libdir}/libhttp_parser.so.%{somajor}.%{sominor}
ln -sf libhttp_parser.so.%{somajor}.%{sominor} %{buildroot}%{_libdir}/libhttp_parser.so.%{somajor}
ln -sf libhttp_parser.so.%{somajor}.%{sominor} %{buildroot}%{_libdir}/libhttp_parser.so

#install strict variant
install out/Release/lib.target/libhttp_parser_strict.so.%{somajor} %{buildroot}%{_libdir}/libhttp_parser_strict.so.%{somajor}.%{sominor}
ln -sf libhttp_parser_strict.so.%{somajor}.%{sominor} %{buildroot}%{_libdir}/libhttp_parser_strict.so.%{somajor}
ln -sf libhttp_parser_strict.so.%{somajor}.%{sominor} %{buildroot}%{_libdir}/libhttp_parser_strict.so


%check
export LD_LIBRARY_PATH='./out/Release/lib.target' 
./out/Release/test-nonstrict
./out/Release/test-strict


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/libhttp_parser.so.*
%{_libdir}/libhttp_parser_strict.so.*
%doc AUTHORS README.md
%license LICENSE-MIT


%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libhttp_parser.so
%{_libdir}/libhttp_parser_strict.so


%changelog
* Tue Oct 25 2016 Nathaniel McCallum <npmccallum@redhat.com> - 2.7.1-3
- Add (upstreamed) status code patch

* Tue Aug 16 2016 Stephen Gallagher <sgallagh@redhat.com> - 2.7.1-2
- Upgrade to version 2.7.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 01 2015 Stephen Gallagher <sgallagh@redhat.com> 2.6.0-1
- Upgrade to version 2.6.0
- Change to new upstream at https://github.com/nodejs/http-parser/

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-9.20121128gitcd01361
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.0-8.20121128gitcd01361
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-7.20121128gitcd01361
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-6.20121128gitcd01361
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-5.20121128gitcd01361
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4.20121128gitcd01361
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0-3.20121128gitcd01361
- latest git snapshot
- fixes buffer overflow in tests

* Tue Nov 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0-2.20121110git245f6f0
- latest git snapshot
- fixes tests
- use SMP make flags
- build as Release instead of Debug
- ship new strict variant

* Sat Oct 13 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0-1
- new upstream release 2.0
- migrate to GYP buildsystem

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 22 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0-1
- New upstream release 1.0
- Remove patches, no longer needed for nodejs
- Fix typo in -devel description
- use github tarball instead of checkout

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-6.20100911git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Lubomir Rintel <lkundrak@v3.sk> - 0.3-5.20100911git
- Add support for methods used by node.js

* Thu Nov  4 2010 Dan HorÃ¡k <dan[at]danny.cz> - 0.3-4.20100911git
- build with -fsigned-char

* Wed Sep 29 2010 jkeating - 0.3-3.20100911git
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.3-2.20100911git
- Call ldconfig (Peter Lemenkov)

* Fri Sep 17 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.3-1.20100911git
- Initial packaging

