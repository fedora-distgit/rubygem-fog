%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname fog
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: brings clouds to you
Name: rubygem-%{gemname}
Version: 0.9.0
Release: 5%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/geemus/fog
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
Requires: ruby(rubygems)
Requires: rubygem(builder)
Requires: rubygem(excon) >= 0.6.1
Requires: rubygem(formatador) >= 0.1.3
Requires: rubygem(json)
Requires: rubygem(mime-types)
Requires: rubygem(net-scp) >= 1.0.4
Requires: rubygem(net-ssh)
Requires: rubygem(nokogiri) >= 1.4.4
Requires: rubygem(hmac)
BuildRequires: ruby(rubygems)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
The Ruby cloud services library.


%prep
%setup -q -c -T
mkdir -p .%{gemdir}
gem install --local --install-dir .%{gemdir} \
            --force --rdoc %{SOURCE0}


%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x


%files
%{_bindir}/fog
%{geminstdir}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
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
