param(
    [string]$d
)

$env:VAULT_ADDR = "http://127.0.0.1:8200"
$env:VAULT_TOKEN = "hvs.wa94spdg9rBYRJa5vHlDqYS5"
$VENV_PATH = "D:\projects\own\vault-desc-ui\venv\venv\Scripts\python.exe"
$SCRIPT_PATH = "json-data-to-vault-commands.py"
$ARGUMENT_LIST = "-d" + $d

$commands = & $VENV_PATH $SCRIPT_PATH $ARGUMENT_LIST
foreach ($cmd in $commands) {
    echo $cmd
    Invoke-Expression $cmd
}
