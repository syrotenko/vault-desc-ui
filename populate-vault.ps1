$env:VAULT_ADDR = "http://127.0.0.1:8200"
$env:VAULT_TOKEN = "hvs.wa94spdg9rBYRJa5vHlDqYS5"
$VENV_PATH = "D:\projects\own\vault-desc-ui\venv\venv\Scripts\python.exe"
$SCRIPT_PATH = "json-data-to-vault-commands.py"

function GET_COMMAND {
    param(
        $command_name,
        $data
    )
    return "vault kv $command_name $data"
}

function EXECUTE_COMMAND{
    param(
        $command
    )
    echo $command
    Invoke-Expression $command
}

$commands = & $VENV_PATH $SCRIPT_PATH
foreach ($cmd in $commands) {
    $patch_command = GET_COMMAND -command_name 'patch' -data $cmd
    EXECUTE_COMMAND -command $patch_command
    if($LASTEXITCODE -ne 0) {
        $put_command = GET_COMMAND -command_name 'put' -data $cmd
        EXECUTE_COMMAND -command $put_command
    }
}
