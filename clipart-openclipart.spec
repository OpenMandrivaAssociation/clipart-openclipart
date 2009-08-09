%define clip_dir %{_datadir}/images/openclipart

Name: clipart-openclipart
Version: 0.18
Release: %mkrel 10
Summary: Open Clip Art Library
License: Public Domain
Group: Graphics
Url: http://www.openclipart.org/
Source: http://www.openclipart.org/downloads/%version/openclipart-%{version}-svgonly.tar.bz2
Source1: clean-up-sources.sh
Buildarch: noarch
BuildRequires: inkscape
BuildRequires: urw-fonts
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
This is a collection of 100% license-free, royalty-free, and
restriction-free art that you can use for whatever purpose you see fit.

Most of the art in this package is in the Scalable Vector Graphic (SVG)
format, which is an XML format approved by the W3C and used in a wide
range of software applications, including Inkscape, Adobe Illustrator,
Batik, and more.

The goal of the Open Clip Art Library is to provide the public with a
huge collection of reusable art for any purpose.

For more information, including how you can contribute to this growing
library, please see http://www.openclipart.org/

%prep
%setup -q -n openclipart-%{version}-svgonly

# clean ugly/broken
(cd clipart
 rm -rf ./unsorted
 rm -f	./computer/icons/lemon-theme/devices/automatic \
	./computer/icons/lemon-theme/actions/automatic \
	./computer/icons/lemon-theme/filesystems/automatic \
	./computer/icons/lemon-theme/apps/automatic \
	./computer/icons/lemon-theme/mimetypes/automatic \
	./buildings/perspectival_house_01.* \
	./signs_and_symbols/flags/america/united_states/.usa_hawaii.svg.swp
)

%build
(cd clipart
# build png files (for OOo galleries), taken from OOo's "build-galleries" script
 for pict_svg in `find ./ -name "*.svg" -type f`; do
    pict_dir=${pict_svg#./}
    pict_dir=${pict_dir%/*}
    pict_png=${pict_svg##*/}
    pict_png=${pict_png%.svg}.png
    mkdir -p build/$pict_dir
    echo "Converting $pict_svg to $pict_dir/$pict_png..."
    inkscape -f $pict_svg -e $pict_dir/$pict_png
done
)

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%clip_dir
(cd ./clipart
 tar c ./ | tar x -C $RPM_BUILD_ROOT%{clip_dir}
)

rm -f $RPM_BUILD_ROOT%{clip_dir}/{PASSFAIL,README,TODO}

# remove empty dirs
rm -rf $RPM_BUILD_ROOT%{clip_dir}/build

find $RPM_BUILD_ROOT%{clip_dir} -name '*bat' -type f -exec rm '{}' \;
find $RPM_BUILD_ROOT%{clip_dir} -type f -exec chmod 644 '{}' \;

# clean broken files
install %{SOURCE1} .
chmod +x ./clean-up-sources.sh
DESTDIR=$RPM_BUILD_ROOT ./clean-up-sources.sh %{clip_dir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%clip_dir
%doc README AUTHORS ChangeLog INSTALL LICENSE NEWS


