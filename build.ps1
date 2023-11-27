param (
    [switch]$test,
    [switch]$clean
)
if ($clean) {
    Remove-Item -Recurse -Force dist
}
pyinstaller --onefile -n mc-utils src\main.py
if ($test) {
    .\dist\mc-utils.exe
}