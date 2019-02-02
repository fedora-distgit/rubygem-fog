%global gem_name fog

Name: rubygem-%{gem_name}
Version: 2.0.0
Release: 3%{?dist}
Summary: Brings clouds to you
# ASL 2.0: lib/fog/opennebula/requests/compute/OpenNebulaVNC.rb
License: MIT or ASL 2.0
URL: http://github.com/fog/fog
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fix "Fog::Compute[:cloudsigma] | volume requests (cloudsigma)" test.
# https://github.com/fog/fog/pull/3997/commits/74d6977b5ac9957bf7a48c390eeb816faf87186a
Patch0: rubygem-fog-2.0.0-Tweak-CloudSigma-testing-schema.patch
# Avoid CloudSigma test issues due to bugs in it mocking interface.
# https://github.com/fog/fog/pull/3997/commits/4fb6da70e12ae5dc1205ab40b3fdf135ce364ad0
Patch1: rubygem-fog-2.0.0-Make-CloudSigma-snapshot-tests-pending.patch
# Remove tests for deprecated binary `#[]`
# https://github.com/fog/fog/commit/0bda54cff981dee7392bbcaa3a553cd4f298437b
Patch2: rubygem-fog-2.0.0-Remove-tests-for-deprecated-binary.patch
# BlueBox is not offered anymore and the tests has issues with fog-core 2.x+.
# https://github.com/fog/fog/pull/4010
Patch3: rubygem-fog-2.0.0-Remove-BlueBox-Blocks.patch
# Fix (remove) some failing tests incompatible with fog-core 2.x+.
# https://github.com/fog/fog/commit/676ccd810f2b677510b438fd3ae2ba94c1897706
Patch4: rubygem-fog-2.0.0-remove-tests-around-deprecated-usage.patch
# Fix namespaces for fog-brightbox 1.0.0+ compatibility.
# https://github.com/fog/fog/pull/4018
Patch5: rubygem-fog-2.0.0-Fix-compatibility-with-fog-brightbox-1.0.0.patch
Requires: ruby(irb)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(bigdecimal)
BuildRequires: rubygem(fog-atmos)
BuildRequires: rubygem(fog-aws)
BuildRequires: rubygem(fog-brightbox)
BuildRequires: rubygem(fog-core)
BuildRequires: rubygem(fog-ecloud)
BuildRequires: rubygem(fog-json)
BuildRequires: rubygem(fog-profitbricks)
BuildRequires: rubygem(fog-riakcs)
BuildRequires: rubygem(fog-sakuracloud)
BuildRequires: rubygem(fog-serverlove)
BuildRequires: rubygem(fog-softlayer)
BuildRequires: rubygem(fog-storm_on_demand)
BuildRequires: rubygem(fog-terremark)
BuildRequires: rubygem(fog-vmfusion)
BuildRequires: rubygem(fog-voxel)
BuildRequires: rubygem(fog-xml)
BuildRequires: rubygem(mime-types)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(minitest-stub-const)
BuildRequires: rubygem(opennebula)
BuildRequires: %{_bindir}/shindo
BuildArch: noarch

%description
The Ruby cloud services library. Supports all major cloud providers including
AWS, Rackspace, Linode, Blue Box, StormOnDemand, and many others. Full support
for most AWS services including EC2, S3, CloudWatch, SimpleDB, ELB, and RDS.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch5 -p1

%gemspec_remove_file -t Dir["spec/fog/bin/bluebox_spec.rb", "tests/bluebox/**/*.rb"]
%gemspec_remove_file Dir["lib/fog/bin/bluebox.rb", "lib/fog/bluebox.rb", "lib/fog/bluebox/**/*.rb", "spec/fog/bin/bluebox_spec.rb", "tests/bluebox/**/*.rb"]
%patch3 -p1

%gemspec_remove_file -t ["spec/fog/compute_spec.rb", "spec/fog/dns_spec.rb"]
%gemspec_remove_file ["spec/fog/compute_spec.rb", "spec/fog/dns_spec.rb"]
%patch4 -p1

# Relax fog-core dependency. All tests are passing with older fog-core. Will
# see soon how fog-core 2.0.0+ works.
%gemspec_remove_dep -g fog-core '~> 1.45'
%gemspec_add_dep -g fog-core '>= 1.43'

# Remove dependencies not in Fedora yet.
# TODO: Aliyun, Local and Vsphere seems to be in default set, anybody wants
# to package them?
%gemspec_remove_dep -g fog-aliyun '>= 0.1.0'
%gemspec_remove_dep -g fog-cloudatcost '~> 0.1.0'
%gemspec_remove_dep -g fog-digitalocean '>= 0.3.0'
%gemspec_remove_dep -g fog-dnsimple '~> 1.0.0'
%gemspec_remove_dep -g fog-dynect '~> 0.0.2'
%gemspec_remove_dep -g fog-google '<= 0.1.0'
%gemspec_remove_dep -g fog-internet-archive '>= 0'
%gemspec_remove_dep -g fog-joyent '>= 0'
%gemspec_remove_dep -g fog-local '>= 0'
%gemspec_remove_dep -g fog-openstack '>= 0'
%gemspec_remove_dep -g fog-ovirt '>= 0'
%gemspec_remove_dep -g fog-powerdns '>= 0.1.1'
%gemspec_remove_dep -g fog-rackspace '>= 0'
%gemspec_remove_dep -g fog-vsphere '>= 0.4.0'
%gemspec_remove_dep -g fog-xenserver '>= 0'

for p in \
  aliyun \
  digitalocean \
  dnsimple \
  dynect \
  google \
  internet_archive \
  joyent \
  local \
  openstack \
  ovirt \
  powerdns \
  rackspace \
  vsphere \
  xenserver
do
  sed -i "/${p}/ s/^/#/" ./lib/fog{.rb,/bin.rb}
  sed -i "/${p}/I s/^/#/" spec/fog/bin_spec.rb
done

sed -i '/openstack/,/},$/ s/^/#/' tests/compute/helper.rb
sed -i '/rackspace/,/}$/ s/^/#/' tests/compute/helper.rb

sed -i '/dnsimple/,/},$/ s/^/#/' tests/dns/helper.rb
sed -i '/dynect/,/},$/ s/^/#/' tests/dns/helper.rb
sed -i '/rackspace/,/},$/ s/^/#/' tests/dns/helper.rb

sed -i "/internetarchive/I s/^/#/" spec/fog/bin_spec.rb

# Fix "Cloudstack | escape (cloudstack)" compatibility with Ruby 2.5.
# https://github.com/fog/fog/issues/4016
sed -i 's/%7E/~/' tests/cloudstack/signed_params_tests.rb

%build
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}

# Status is not processed correctly for ibm provider,
# therefore the tests gets stuck every time :/
rm -rf tests/ibm
sed -i '/for/a\  next if provider == :ibm\n' tests/compute/models/server{,s}_tests.rb

# 'stack level too deep' probably due to fog-core 2.x and namespaces.
mv tests/vcloud_director/models/compute/vdcs_tests.rb{,.disabled}

FOG_MOCK=true shindont

for p in \
  dnsimple \
  dynect \
  google \
  joyent \
  local \
  openstack \
  powerdns \
  rackspace \
  vsphere \
  xenserver
do
  rm spec/fog/bin/${p}_spec.rb
done

# fog-google providing this contant is not available.
sed -i '/it "responds to collections" do/,/^    end$/ s/^/#/' spec/helpers/bin.rb

# These two does not run properly together in single test run.
# This might be fix:
# https://github.com/fog/fog/pull/3997/commits/69e28fe870cedc6d9e54c626f922760c47178404
FOG_MOCK=true ruby -Ispec -rspec_helper -e 'Dir.glob "./spec/fog/**/*_spec.rb", &method(:require)'
FOG_MOCK=true ruby -Ispec -rspec_helper -e 'Dir.glob "./spec/vcloud_director/**/*_spec.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{_bindir}/fog
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE.md
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUT*
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/RELEASE.md
%{gem_instdir}/benchs
%{gem_instdir}/gemfiles
%{gem_instdir}/Rakefile
%{gem_instdir}/fog.gemspec
%{gem_instdir}/spec
%{gem_instdir}/tests
# remove 0 length files
%exclude %{gem_instdir}/tests/go_grid/requests/compute/image_tests.rb

%changelog
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 08 2018 Vít Ondruch <vondruch@redhat.com> - 2.0.0-2
- Fix fog-core 2.x+ compatibility.

* Wed Oct 10 2018 Vít Ondruch <vondruch@redhat.com> - 2.0.0-1
- Update to fog 2.0.0.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.38.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.38.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.38.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 23 2017 Vít Ondruch <vondruch@redhat.com> - 1.38.0-3
- Fix FTBFS in Rawhide (rhbz#1424311).

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.38.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 13 2016 Vít Ondruch <vondruch@redhat.com> - 1.38.0-1
- Update to fog 1.38.0.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Vít Ondruch <vondruch@redhat.com> - 1.28.0-1
- Update to fog 1.28.0.

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
