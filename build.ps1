param (
    [switch]$test,
    [switch]$clean
)
if ($clean) {
    Remove-Item -Recurse -Force dist
    Remove-Item -Recurse -Force build
}
pyinstaller --onefile -n mc-utils src\main.py
if ($test) {
    .\dist\mc-utils.exe
}