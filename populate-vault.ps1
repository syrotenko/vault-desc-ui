$CREDENTIALS = Get-Content .\.credentials.json | ConvertFrom-Json
$env:VAULT_ADDR = $CREDENTIALS.VAULT_ADDR
$env:VAULT_TOKEN = $CREDENTIALS.VAULT_TOKEN
$SCRIPT_PATH = "json-data-to-vault-commands.py"
$SCRIPT_ARGUMENT = "-d .\\vault-test-data.json"

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

$commands = & $VENV_PATH $SCRIPT_PATH $SCRIPT_ARGUMENT
foreach ($cmd in $commands) {
    $patch_command = GET_COMMAND -command_name 'patch' -data $cmd
    EXECUTE_COMMAND -command $patch_command
    if($LASTEXITCODE -ne 0) {
        $put_command = GET_COMMAND -command_name 'put' -data $cmd
        EXECUTE_COMMAND -command $put_command
    }
}
