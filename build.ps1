param (
    [switch]$test,
    [switch]$clean
)
if ($clean) {
    Remove-Item -Recurse -Force dist
    Remove-Item -Recurse -Force build
}
pip install -r requirements.txt
Get-ChildItem -Filter "*.spec" -Recurse | Remove-Item -Force
Get-ChildItem -Path dist -Filter "*.exe" | Remove-Item -Force
pyinstaller --onefile -n mc-utils src\main.py
if ($test) {
    .\dist\mc-utils.exe
}