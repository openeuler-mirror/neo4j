%global debug_package %{nil}
Name:                neo4j
Version:             4.3.0
Release:             2
Summary:             Graphs for Everyone
License:             GPLv3
URL:                 https://neo4j.com/
Source0:             https://github.com/neo4j/neo4j/archive/%{version}.tar.gz
Patch0:              fix-cypher-shell-pom.patch
BuildRequires:       java-11-openjdk-devel maven gradle-local maven-local
Requires:            java-11-openjdk-devel
BuildArch:           noarch
%description
Neo4j is the world’s leading Graph Database. It is a high performance graph
store with all the features expected of a mature and robust database, like
a friendly query language and ACID transactions.

%prep
%setup -qn %{name}-%{version}
%patch0 -p1

%build
export LC_ALL=en_US.UTF-8
java11_version=`rpm -qa | grep java-11-openjdk-11`
export JAVA_HOME=/usr/lib/jvm/$java11_version
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
mvn  clean install  -DskipTests

%install
install -d -m 0755 %{buildroot}/%{_bindir}
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/bin
install -d -m 0755 %{buildroot}/%{_sysconfdir}/%{name}/
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/data
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/import
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/plugins
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/labs
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/certificates
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/run
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/logs
install -d -m 0755 %{buildroot}%{_datadir}/doc/%{name}
install -d -m 0755 %{buildroot}%{_datadir}/java/%{name}
install -d -m 0755 %{buildroot}%{_mavenpomdir}/%{name}
tar  xf ./packaging/standalone/target/%{name}-community-%{version}-SNAPSHOT-unix.tar.gz
pushd %{name}-community-%{version}-SNAPSHOT
   cp -arf bin/* %{buildroot}%{_datadir}/%{name}/bin
   cp -arf conf/* %{buildroot}%{_sysconfdir}/%{name}/
   cp -arf lib/* %{buildroot}%{_datadir}/%{name}/lib
   cp -arf data/* %{buildroot}%{_datadir}/%{name}/data
   cp -arf labs/* %{buildroot}%{_datadir}/%{name}/labs
   cp -arf plugins/* %{buildroot}%{_datadir}/%{name}/plugins
   for f in LICENSES.txt LICENSE.txt NOTICE.txt README.txt UPGRADE.txt ;do
   cp -f ${f} %{buildroot}%{_datadir}/doc/%{name}
   done
popd
pushd %{buildroot}/%{_datadir}/%{name}/
   %{__ln_s} %{_sysconfdir}/%{name} conf
popd
pushd %{buildroot}%{_datadir}/%{name}/bin
    ln -s %{_datadir}/%{name}/bin/%{name} %{buildroot}%{_bindir}/%{name}
popd
pushd community
  for  z in `ls | grep -v community| grep -v pom |grep -v cypher |grep -v neo4j |grep -v compiler  \
     | grep -v server-api | grep -v target | grep -v zstd | grep -v test ` ;do
    install -pm 0644 $z/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}-$z.pom
    install -pm 0644 $z/target/%{name}-$z-%{version}-SNAPSHOT.jar %{buildroot}%{_javadir}/%{name}/%{name}-$z.jar
    %add_maven_depmap %{name}/%{name}-$z.pom  %{name}/%{name}-$z.jar
  done
  for a in %{name}-harness %{name}  %{name}-exceptions ;do
    install -pm 0644 $a/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/$a.pom
    install -pm 0644 $a/target/$a-%{version}-SNAPSHOT.jar %{buildroot}%{_javadir}/%{name}/$a.jar
    %add_maven_depmap %{name}/$a.pom  %{name}/$a.jar
  done
popd
pushd community/cypher/front-end
    for b  in ast  expressions parser util rewriting  cypher-macros ;do
        install -pm 0644 $b/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}-$b.pom
        install -pm 0644 $b/target/%{name}-$b-%{version}-SNAPSHOT.jar %{buildroot}%{_javadir}/%{name}/%{name}-$b.jar
        %add_maven_depmap %{name}/%{name}-$b.pom  %{name}/%{name}-$b.jar
    done
    install -pm 0644 frontend/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}-front-end.pom
    install -pm 0644 frontend/target/%{name}-front-end-%{version}-SNAPSHOT.jar \
    %{buildroot}%{_javadir}/%{name}/%{name}-front-end.jar
    %add_maven_depmap %{name}/%{name}-front-end.pom  %{name}/%{name}-front-end.jar
popd
pushd community/cypher/front-end
    install -pm 0644 javacc-parser/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}-cypher-javacc-parser.pom
    install -pm 0644 javacc-parser/target/%{name}-cypher-javacc-parser-%{version}-SNAPSHOT.jar \
    %{buildroot}%{_javadir}/%{name}/%{name}-cypher-javacc-parser.jar
    %add_maven_depmap %{name}/%{name}-cypher-javacc-parser.pom  %{name}/%{name}-cypher-javacc-parser.jar
    install -pm 0644 %{name}-ast-factory/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}-cypher-ast-factory.pom
    install -pm 0644 %{name}-ast-factory/target/%{name}-cypher-ast-factory-%{version}-SNAPSHOT.jar \
    %{buildroot}%{_javadir}/%{name}/%{name}-cypher-ast-factory.jar
    %add_maven_depmap %{name}/%{name}-cypher-ast-factory.pom  %{name}/%{name}-cypher-ast-factory.jar
popd
pushd community/cypher
    for c in interpreted-runtime expression-evaluator  acceptance-spec-suite logical-plan-generator planner-spi ir \
      runtime-util  spec-suite-tools compatibility-spec-suite logical-plan-builder runtime-spec-suite ;do
      install -pm 0644 $c/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}-cypher-$c.pom
      install -pm 0644 $c/target/%{name}-cypher-$c-%{version}-SNAPSHOT.jar \
      %{buildroot}%{_javadir}/%{name}/%{name}-cypher-$c.jar
      %add_maven_depmap %{name}/%{name}-cypher-$c.pom  %{name}/%{name}-cypher-$c.jar
    done
popd
pushd community/cypher
    for d  in cypher  cypher-planner  cypher-config  cypher-logical-plans  ;do
        install -pm 0644 $d/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}-$d.pom
        install -pm 0644 $d/target/%{name}-$d-%{version}-SNAPSHOT.jar %{buildroot}%{_javadir}/%{name}/%{name}-$d.jar
        %add_maven_depmap %{name}/%{name}-$d.pom  %{name}/%{name}-$d.jar
    done
popd

%files
%doc %{_datadir}/doc/%{name}/*
%{_bindir}/*
%{_sysconfdir}/%{name}/*
%{_datadir}/%{name}/*
%{_datadir}/java/%{name}/*
%{_mavenpomdir}/%{name}/*
%{_datadir}/maven-metadata/%{name}.xml

%changelog
* Tue Dec 14 2021 wangkai <wangkai385@huawei.com> - 4.3.0-2
- fix cypher-shell pom

* Wed Jul 14 2021 liyanan <liyanan32@huawei.com> - 4.3.0-1
- package init
