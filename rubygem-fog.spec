%global gem_name fog

Summary: Brings clouds to you
Name: rubygem-%{gem_name}
Version: 1.15.0
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/geemus/fog
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(builder)
Requires: rubygem(excon) => 0.20
Requires: rubygem(excon) < 1
Requires: rubygem(formatador) => 0.2.0
Requires: rubygem(formatador) < 0.3
Requires: rubygem(json) => 1.7
Requires: rubygem(json) < 2
Requires: rubygem(mime-types)
Requires: rubygem(nokogiri) => 1.5
Requires: rubygem(nokogiri) < 2.0
Requires: rubygem(net-scp) => 1.1
Requires: rubygem(net-scp) < 2
Requires: rubygem(net-ssh) >= 2.1.3
Requires: rubygem(ruby-hmac)

BuildRequires: rubygems-devel
BuildRequires: rubygem(excon) => 0.20
BuildRequires: rubygem(excon) < 1
BuildRequires: rubygem(mime-types)
BuildRequires: rubygem(multi_json) => 1.0
BuildRequires: rubygem(multi_json) < 2
BuildRequires: rubygem(net-scp) => 1.1
BuildRequires: rubygem(net-scp) < 2
BuildRequires: rubygem(net-ssh) >= 2.1.3
BuildRequires: rubygem(nokogiri) => 1.5
BuildRequires: rubygem(nokogiri) < 2.0
BuildRequires: rubygem(rbovirt)
BuildRequires: rubygem(rbvmomi)
BuildRequires: rubygem(shindo)
BuildRequires: rubygem(simplecov)
BuildRequires: rubygem(rspec)

BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

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


%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}/%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
# rubygem-coveralls is not yet in Fedora
COVERAGE=false FOG_MOCK=true shindo
popd


%files
%{_bindir}/fog
%exclude %{gem_cache}
%{gem_spec}
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%doc %{gem_instdir}/README.md
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/Gemfile.1.8.7

%files doc
%doc %{gem_instdir}/RELEASE.md
%{gem_instdir}/benchs
%{gem_instdir}/tests
# remove 0 length files
%exclude %{gem_instdir}/tests/aws/models/auto_scaling/helper.rb
%exclude %{gem_instdir}/tests/go_grid/requests/compute/image_tests.rb
%{gem_instdir}/fog.gemspec
%{gem_instdir}/Rakefile
%doc %{gem_docdir}
%doc %{gem_instdir}/changelog.txt
%exclude %{gem_instdir}/docs/public/images/.gitignore
%exclude %{gem_instdir}/docs/public/js/mylibs/.gitignore

%changelog
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
