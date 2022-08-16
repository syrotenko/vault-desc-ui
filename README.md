# Prepare environment (once)

## Install choco:

Run as admin in PowerShell:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

Make sure it's installed:

```powershell
choco
```

&nbsp;

## Install vault by hashicorp

```powershell
choco install vault
```

Make sure it's installed:

```powershell
vault
```

## Install Python (3.9)

&nbsp;

# Prepare vault (each time)

Dev vault server stores data in memory, so we have to perform these steps every time we run vault server.

## Start vault Dev server:

```powershell
vault server -dev
```

Save `Unseal Key` (I don't know why)

Save `Root Token`

&nbsp;

## Populate vault with test data

Set the following values in the `populate-vault.ps1` script:

-   `POWERSHELL_PATH` - path to the PowerShell
-   `DATA_PATH` - path to the data (e.g. `vault-test-data.json`)

Set the following values in the `populate-vault.ps1` script:

-   `VAULT_ADDR` - value from the previous step
-   `VAULT_TOKEN` - value from the previous step
-   `VENV_PATH` - path to the Python
-   `SCRIPT_PATH` - path to the `json-data-to-vault-commands.py` script

Run as admin in PowerShell

**THIS DOESN'T WORK**
```powershell
populate-vault.ps1
```

&nbsp;

# Helper

## Vault

Set credentials (necessary to interact with vault):

```powershell
$env:VAULT_ADDR="http://127.0.0.1:8200"
$env:VAULT_TOKEN="<Root Token>"
vault status
```

Commands:

```powershell
vault kv list secret
vault kv get secret/d1/d11
vault kv put secret/d1/d11 foo=bar
```
