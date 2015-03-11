%global gem_name fog

Summary: Brings clouds to you
Name: rubygem-%{gem_name}
Version: 1.23.0
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/geemus/fog
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0: rubygem-fog-1.27.0-support-ruby-2.2.patch
Patch1: rubygem-fog-1.27.0-require-version.patch

BuildRequires: rubygems-devel
BuildRequires: rubygem(fog-brightbox)
BuildRequires: rubygem(fog-core)
BuildRequires: rubygem(fog-json)
BuildRequires: rubygem(fog-softlayer)
BuildRequires: rubygem(ipaddress)
BuildRequires: rubygem(nokogiri)
BuildRequires: rubygem(rbovirt)
BuildRequires: rubygem(rbvmomi)
BuildRequires: rubygem(ruby-libvirt)
BuildRequires: rubygem(shindo)

BuildArch: noarch

%description
The Ruby cloud services library.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description doc
Documentation for %{name}


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
%patch1 -p1

# Fix duplicate key warning, the key is not used anyway and it shows up when using Vagrant
# https://github.com/fog/fog/commit/189ab1c677e88f670f9269b0857efeb1e18f64ea
sed -i 's/"name" => "Ubuntu",/#"name" => "Ubuntu",/' lib/fog/rackspace/mock_data.rb

popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}/%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Fix anything executable that does not have a shebang
for file in `find %{buildroot}/%{gem_instdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}/%{gem_instdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

%check
pushd .%{gem_instdir}
# Disable coverage.
sed -i "/require 'simplecov'/ s/^/#/" tests/helper.rb

# The test fails without network connection.
# https://github.com/fog/fog/issues/2986
mv tests/hp/block_storage_tests.rb{,.bak}

# 1 failure: Newer fog-core puts itself to user agent
# See https://github.com/fog/fog-core/blob/v1.27.0/lib/fog/core/connection.rb#L37
COVERAGE=false FOG_MOCK=true shindo | grep '1 failed'
popd


%files
%doc %{gem_instdir}/LICENSE.md
%{_bindir}/fog
%exclude %{gem_cache}
%{gem_spec}
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/Gemfile

%files doc
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUT*
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/RELEASE.md
%{gem_instdir}/benchs
%{gem_instdir}/gemfiles
%{gem_instdir}/spec
%{gem_instdir}/tests
# remove 0 length files
%exclude %{gem_instdir}/tests/aws/models/auto_scaling/helper.rb
%exclude %{gem_instdir}/tests/go_grid/requests/compute/image_tests.rb
%{gem_instdir}/fog.gemspec
%{gem_instdir}/Rakefile
%doc %{gem_docdir}

%changelog
* Wed Mar 11 2015 Josef Stribny <jstribny@redhat.com> - 1.23.0-3
- Fix duplicate key warning

* Tue Mar 10 2015 Josef Stribny <jstribny@redhat.com> - 1.23.0-2
- Patch for Ruby 2.2 support

* Tue Jul 29 2014 Brett Lentz <blentz@redhat.com> - 1.23.0-1
- Update to Fog 1.23.0.

* Mon Jun 09 2014 Vít Ondruch <vondruch@redhat.com> - 1.22.1-1
- Update to Fog 1.22.1.

* Mon Jun 09 2014 Vít Ondruch <vondruch@redhat.com> - 1.22.0-1
- Update to Fog 1.22.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 09 2013 Josef Stribny <jstribny@redhat.com> - 1.15.0-1
- Update to Fog 1.15.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Josef Stribny <jstribny@redhat.com> - 1.11.1-1
- Update to Fog 1.11.1

* Thu Mar 14 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.7.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.7.0-1
- Update to Fog 1.7.0.

* Tue Jul 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.5.0-2
- Fix handling of failing tests.

* Mon Jul 30 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.5.0-1
- Update to Fog 1.5.0.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.2-1
- Updated to version 1.1.2
- Introduced doc subpackage
- Added check section
- Adjusted dependencies for the new version

* Tue Sep 06 2011 Chris Lalancette <clalance@redhat.com> - 0.9.0-5
- Bump the release version to make upgrades from F-16 work

* Mon Aug 01 2011 Chris Lalancette <clalance@redhat.com> - 0.9.0-4
- Remove the net-ssh version; any version should work

* Fri Jul 22 2011 Chris Lalancette <clalance@redhat.com> - 0.9.0-3
- Fix the hmac dependency

* Fri Jul 08 2011 Chris Lalancette <clalance@redhat.com> - 0.9.0-2
- Use global macro instead of define

* Tue Jul 05 2011 Chris Lalancette <clalance@redhat.com> - 0.9.0-1
- Initial package
