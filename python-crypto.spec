%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from 
distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	Cryptography library for Python
Name:		python-crypto
Version:	2.0.1
Release:	22%{?dist}
License:	Public Domain
Group:		Development/Libraries
# FIXME: In the near future, new releases will be at http://www.dlitz.net/software/pycrypto/
URL:		http://www.amk.ca/python/code/crypto.html

# The original tarball:
#  http://www.amk.ca/files/python/crypto/pycrypto-2.0.1.tar.gz
# contains support for IDEA and RC5.
# 
# We remove it in the tarball we ship, using a "hobble-python-crypto" script.
Source:		pycrypto-2.0.1-hobbled.tar.gz

# patch taken from 
# http://gitweb2.dlitz.net/?p=crypto/pycrypto-2.x.git;a=commitdiff;h=d1c4875e1f220652fe7ff8358f56dee3b2aba31b
Patch0: 	%{name}-fix_buffer_overflow.patch
# Python 2.6 compatibility: Use Hash.MD5 instead of Python "md5" module in the HMAC...
# http://gitweb.pycrypto.org/?p=crypto/pycrypto-2.x.git;a=commitdiff;h=84b793416b52311643bfd456a4544444afbfb5da
Patch1:         python-crypto-hmac_md5.patch
# Python 2.6 compatibility: When possible, use hashlib instead of the deprecated 'md5...
# http://gitweb.pycrypto.org/?p=crypto/pycrypto-2.x.git;a=commitdiff;h=d2311689910240e425741a546576129f4c9735e2
Patch2:         python-crypto-use_hashlib_when_possible.patch

# Remove references to IDEA and RC5:
Patch3:         python-crypto-hobble.patch

Provides:	pycrypto = %{version}-%{release}
BuildRequires:	python >= 2.2
BuildRequires:	python-devel >= 2.2
BuildRequires:	gmp-devel >= 4.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot-%(%{__id_u} -n)

%description
Python-crypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).


%prep
%setup -n pycrypto-%{version} -q
sed -i s:/lib:/%_lib:g setup.py
%patch0 -b .patch0 -p1
%patch1 -b .patch1 -p1
%patch2 -b .patch2 -p1
%patch3 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find -name "*.py"|xargs %{__perl} -pi -e "s:/usr/local/bin/python:%{__python}:"

%check
%{__python} test.py


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README TODO ACKS ChangeLog LICENSE Doc
%{python_sitearch}/*.egg-info
%{python_sitearch}/Crypto/*.py*
%{python_sitearch}/Crypto/Cipher/*.so
%{python_sitearch}/Crypto/Cipher/*.py*
%{python_sitearch}/Crypto/Hash/*.so
%{python_sitearch}/Crypto/Hash/*.py*
%{python_sitearch}/Crypto/Protocol/*.py*
%{python_sitearch}/Crypto/PublicKey/*.so
%{python_sitearch}/Crypto/PublicKey/*.py*
%{python_sitearch}/Crypto/Util/*.py*
%dir %{python_sitearch}/Crypto
%dir %{python_sitearch}/Crypto/Cipher/
%dir %{python_sitearch}/Crypto/Hash/
%dir %{python_sitearch}/Crypto/Protocol/
%dir %{python_sitearch}/Crypto/PublicKey/
%dir %{python_sitearch}/Crypto/Util/


%changelog
* Wed Sep 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.1-22
- fix %%description
Related: rhbz#636268

* Wed Sep 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.1-21
- remove IDEA and RC5 implementations
Resolves: rhbz#636268
- add %%check section

* Thu Jan 28 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.1-20
- use a dist tag

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Stewart Adam <s.adam at diffingo.com> - 2.0.1-17
- Use patches in upstream git to fix #484473

* Fri Feb 13 2009 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.0.1-16.1
- add patch to fix #485298 / CVE-2009-0544

* Sat Feb 7 2009 Stewart Adam <s.adam at diffingo.com> - 2.0.1-15.1
- Oops, actually apply the patch
- Modify patch so modules remain compatible with PEP 247

* Sat Feb 7 2009 Stewart Adam <s.adam at diffingo.com> - 2.0.1-15
- Add patch to hashlib instead of deprecated md5 and sha modules (#484473)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.1-14.1
- Rebuild for Python 2.6

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.0.1-13
- provide pycrypto

* Sat Feb 09 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.0.1-12
- rebuilt

* Fri Jan 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1-11
- egg-info file in python_sitearch and not in python_sitelib

* Fri Jan 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1-10
- ship egg-file

* Tue Aug 21 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1-9
- Remove the old and outdated python-abi hack

* Fri Aug 03 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info>
- Update License field due to the "Licensing guidelines changes"

* Mon Jun 04 2007 David Woodhouse <dwmw2@infradead.org> - 2.0.1-8
- Fix libdir handling so it works on more arches than x86_64

* Wed Apr 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-7
- Fix typo

* Wed Apr 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-6
- Remove dist
- rebuild, because the older version was much bigger, as it was build when
  distutils was doing static links of libpython

* Sat Dec 09 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-5
- Rebuild for python 2.5

* Thu Sep 07 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-4
- Don't ghost pyo files (#205408)

* Tue Aug 29 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-3
- Rebuild for Fedora Extras 6

* Mon Feb 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-2
- Rebuild for Fedora Extras 5

* Wed Aug 17 2005 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0.1-1
- Update to 2.0.1
- Use Dist
- Drop python-crypto-64bit-unclean.patch, similar patch was applied 
  upstream

* Thu May 05 2005 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0-4
- add python-crypto-64bit-unclean.patch (#156173)

* Mon Mar 21 2005 Seth Vidal <skvidal at phy.duke.edu> - 0:2.0-3
- iterate release for build on python 2.4 based systems

* Sat Dec 18 2004 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0-2
- Fix build on x86_64: use python_sitearch for files and patch source
  to find gmp

* Thu Aug 26 2004 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0-0.fdr.1
- Update to 2.00

* Fri Aug 13 2004 Ville Skytta <ville.skytta at iki.fi> - 0:1.9-0.fdr.6.a6
- Don't use get_python_version(), it's available in Python >= 2.3 only.

* Thu Aug 12 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0:1.9-0.fdr.5.a6
- Own dir python_sitearch/Crypto/

* Wed Aug 11 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0:1.9-0.fdr.4.a6
- Match python spec template more

* Sat Jul 17 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0:1.9-0.fdr.3.a6
- Own _libdir/python/site-packages/Crypto/

* Wed Mar 24 2004 Panu Matilainen <pmatilai@welho.com> 0.3.2-0.fdr.2.a6
- generate .pyo files during install
- require exact version of python used to build the package
- include more docs + demos
- fix dependency on /usr/local/bin/python
- use fedora.us style buildroot
- buildrequires gmp-devel
- use description from README

* Sun Jan 11 2004 Ryan Boder <icanoop@bitwiser.org>  0.3.2-0.fdr.1.a6
- Initial build.

