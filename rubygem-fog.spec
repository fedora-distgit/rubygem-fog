%global gem_name fog

# Remove as soon as the macros are available in rubygems-devel package:
# https://lists.fedoraproject.org/archives/list/ruby-sig@lists.fedoraproject.org/thread/ZSGFXCMPGNLLWWXSJH6WPG4TUNOU3JBT/

# The 'read' command not essential, but it is usefull to make the sript
# appear in build log.

# Add dependency named gem with requirements to .gemspec. It adds runtime
# dependency by default.
# -g<gem>            Specifies name of the gem dependency.
# -s<gemspec_file>   Overrides the default .gemspec location.
# -d                 Add development dependecy.
#
# The remaining arguments are expected to by requirements and should be
# valid Ruby code.
%define gemspec_add_dep(g:s:d) \
read -d '' gemspec_add_dep_script << 'EOR' || : \
  gemspec_file = '%{-s*}%{!?-s:./%{gem_name}.spec}' \
  \
  name = '%{-g*}' \
  requirements = %{*}%{!?1:nil} \
  \
  type = :%{!?-d:runtime}%{?-d:development} \
  \
  spec = Gem::Specification.load(gemspec_file) \
  abort("#{gemspec_file} is not accessible.") unless spec \
  \
  dep = spec.dependencies.detect { |d| d.type == type && d.name == name } \
  if dep \
    dep.requirement.concat requirements \
  else \
    spec.public_send "add_#{type}_dependency", name, requirements \
  end \
  File.write gemspec_file, spec.to_ruby \
EOR\
echo "$gemspec_add_dep_script" | ruby \
unset -v gemspec_add_dep_script \
%{nil}

# Remove  dependency named gem with requirements to .gemspec. It adds runtime
# dependency by default.
# -g<gem>            Specifies name of the gem dependency.
# -s<gemspec_file>   Overrides the default .gemspec location.
# -d                 Remove development dependecy.
#
# If remaing arguments specify some version requirements, the macro fails if
# these specific requirements can't be removed.
%define gemspec_remove_dep(g:s:d) \
read -d '' gemspec_remove_dep_script << 'EOR' || : \
  gemspec_file = '%{-s*}%{!?-s:./%{gem_name}.spec}' \
  \
  name = '%{-g*}' \
  requirements = %{*}%{!?1:nil} \
  \
  type = :%{!?-d:runtime}%{?-d:development} \
  \
  spec = Gem::Specification.load(gemspec_file) \
  abort("#{gemspec_file} is not accessible.") unless spec \
  \
  dep = spec.dependencies.detect { |d| d.type == type && d.name == name } \
  if dep \
    if requirements \
      requirements = Gem::Requirement.create(requirements).requirements \
      requirements.each do |r| \
        unless dep.requirement.requirements.reject! { |dependency_requirements| dependency_requirements == r } \
          abort("Requirement '#{r.first} #{r.last}' was not possible to remove for dependency '#{dep}'!") \
        end \
      end \
      spec.dependencies.delete dep if dep.requirement.requirements.empty? \
    else \
      spec.dependencies.delete dep \
    end \
  else \
    abort("Dependency '#{name}' was not found!") \
  end \
  File.write '.%{gem_spec}', spec.to_ruby \
EOR\
echo "$gemspec_remove_dep_script" | ruby \
unset -v gemspec_remove_dep_script \
%{nil}

Name: rubygem-%{gem_name}
Version: 1.38.0
Release: 1%{?dist}
Summary: Brings clouds to you
Group: Development/Languages
# ASL 2.0: lib/fog/opennebula/requests/compute/OpenNebulaVNC.rb
License: MIT or ASL 2.0
URL: http://github.com/fog/fog
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Drop deprecated HPCloud support from test suite.
# https://github.com/fog/fog/pull/3912
Patch0: rubygem-fog-1.38.0-Drop-hp-from-compute-tests.patch
Patch1: rubygem-fog-1.38.0-Drop-hp-from-storage-tests.patch
Patch2: rubygem-fog-1.38.0-Drop-hp-test-cases.patch
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
BuildRequires: rubygem(opennebula)
BuildRequires: rubygem(rbovirt)
BuildRequires: %{_bindir}/shindo
BuildArch: noarch

%description
The Ruby cloud services library. Supports all major cloud providers including
AWS, Rackspace, Linode, Blue Box, StormOnDemand, and many others. Full support
for most AWS services including EC2, S3, CloudWatch, SimpleDB, ELB, and RDS.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
%patch1 -p1
%patch2 -p1
popd


# Remove dependencies not in Fedora yet.
# TODO: Aliyun, Local and Vsphere seems to be in default set, anybody wants
# to package them?
%gemspec_remove_dep -g fog-aliyun -s .%{gem_spec} '>= 0.1.0'
%gemspec_remove_dep -g fog-cloudatcost -s .%{gem_spec} '~> 0.1.0'
%gemspec_remove_dep -g fog-dynect -s .%{gem_spec} '~> 0.0.2'
%gemspec_remove_dep -g fog-google -s .%{gem_spec} '<= 0.1.0'
%gemspec_remove_dep -g fog-local -s .%{gem_spec} '>= 0'
%gemspec_remove_dep -g fog-openstack -s .%{gem_spec} '>= 0'
%gemspec_remove_dep -g fog-powerdns -s .%{gem_spec} '>= 0.1.1'
%gemspec_remove_dep -g fog-rackspace -s .%{gem_spec} '>= 0'
%gemspec_remove_dep -g fog-vsphere -s .%{gem_spec} '>= 0.4.0'
%gemspec_remove_dep -g fog-xenserver -s .%{gem_spec} '>= 0'

pushd .%{gem_instdir}
sed -i '/dynect/ s/^/#/' ./lib/fog.rb
sed -i '/google/ s/^/#/' ./lib/fog.rb
sed -i '/local/ s/^/#/' ./lib/fog.rb
sed -i '/rackspace/ s/^/#/' ./lib/fog.rb
sed -i '/openstack/ s/^/#/' ./lib/fog.rb
sed -i '/powerdns/ s/^/#/' ./lib/fog.rb
sed -i '/vsphere/ s/^/#/' ./lib/fog.rb
sed -i '/xenserver/ s/^/#/' ./lib/fog.rb
sed -i '/aliyun/ s/^/#/' ./lib/fog.rb

sed -i '/dynect/ s/^/#/' ./lib/fog/bin.rb
sed -i '/google/ s/^/#/' ./lib/fog/bin.rb
sed -i '/local/ s/^/#/' ./lib/fog/bin.rb
sed -i '/rackspace/ s/^/#/' ./lib/fog/bin.rb
sed -i '/openstack/ s/^/#/' ./lib/fog/bin.rb
sed -i '/powerdns/ s/^/#/' ./lib/fog/bin.rb
sed -i '/vsphere/ s/^/#/' ./lib/fog/bin.rb
sed -i '/xenserver/ s/^/#/' ./lib/fog/bin.rb
sed -i '/aliyun/ s/^/#/' ./lib/fog/bin.rb
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Drop the executable bit.
# https://github.com/fog/fog/commit/9c8316bb9e3a1e839577b616ae37aac577dbb6af
chmod a-x %{buildroot}%{gem_libdir}/fog/opennebula/README.md


%check
pushd .%{gem_instdir}
# Ignore dependencies not in Fedora yet.
sed -i '/openstack/,/},/ s/^/#/' tests/compute/helper.rb
sed -i '/rackspace/,/}$/ s/^/#/' tests/compute/helper.rb

sed -i '/dynect/,/},/ s/^/#/' tests/dns/helper.rb
sed -i '/rackspace/,/},/ s/^/#/' tests/dns/helper.rb

FOG_MOCK=true shindo
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
