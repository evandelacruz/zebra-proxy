pip install -r requirements.txt
git clone https://github.com/Microsoft/vcpkg.git
vcpkg\bootstrap-vcpkg.bat
vcpkg\vcpkg integrate install
vcpkg\vcpkg install libusb
echo "libusb is installed here: "
Get-ChildItem -Path C:\vcpkg\installed\ -Recurse -Filter "libusb-1.0.dll"
