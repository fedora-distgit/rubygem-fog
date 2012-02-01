%global gem_name fog

Summary: Brings clouds to you
Name: rubygem-%{gem_name}
Version: 1.1.2
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/geemus/fog
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires: ruby(abi) = 1.9.1
Requires: ruby(rubygems)
Requires: rubygem(builder)
Requires: rubygem(excon) >= 0.9.0
Requires: rubygem(formatador) >= 0.2.0
Requires: rubygem(mime-types)
Requires: rubygem(multi_json) >= 1.0.3
Requires: rubygem(net-scp) >= 1.0.4
Requires: rubygem(net-ssh) >= 2.1.3
Requires: rubygem(nokogiri) >= 1.5.0
Requires: rubygem(hmac)

BuildRequires: rubygems-devel
BuildRequires: rubygem(builder)
BuildRequires: rubygem(excon) >= 0.9.0
BuildRequires: rubygem(formatador)
BuildRequires: rubygem(mime-types)
BuildRequires: rubygem(multi_json) >= 1.0.3
BuildRequires: rubygem(nokogiri) >= 1.5.0
BuildRequires: rubygem(rbvmomi)
#BuildRequires: rubygem(rspec-core)
BuildRequires: rubygem(shindo)

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
mkdir -p .%{gem_dir}
gem install --local --install-dir .%{gem_dir} \
            --force --rdoc %{SOURCE0}


%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gem_dir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gem_dir}/bin
find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# fix permissions
pushd %{buildroot}%{gem_instdir}/docs
find -type f -print | xargs chmod a-x
popd
pushd %{buildroot}%{gem_instdir}/examples
find -type f -print | xargs chmod a-x
popd

%check
pushd .%{gem_instdir}
# specs currently require rspec ~> 1.3.1
#FOG_MOCK=true rspec spec/
# remove the lines requiring spec (not needed for shindo)
find -type f -print | xargs sed -i "/require 'spec/d"
FOG_MOCK=true shindo
popd


%files
%{_bindir}/fog
%exclude %{gem_cache}
%{gem_spec}
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%doc %{gem_instdir}/README.rdoc
%exclude %{gem_instdir}/.document
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/docs/public/images/.gitignore
%exclude %{gem_instdir}/docs/public/js/mylibs/.gitignore
%exclude %{gem_instdir}/Gemfile

%files doc
%{gem_instdir}/benchs
%{gem_instdir}/examples
%{gem_instdir}/spec
%{gem_instdir}/tests
# remove 0 length files
%exclude %{gem_instdir}/tests/aws/models/auto_scaling/helper.rb
%exclude %{gem_instdir}/tests/go_grid/requests/compute/image_tests.rb
%{gem_instdir}/fog.gemspec
%{gem_instdir}/Rakefile
%doc %{gem_docdir}
%doc %{gem_instdir}/changelog.txt
%doc %{gem_instdir}/docs


%changelog
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
